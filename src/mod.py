from . import get_db
from datetime import datetime, timedelta
from collections import defaultdict
from flask import (
    Blueprint, request, jsonify                   
    )

streak = Blueprint('streak', __name__)

def calculate_streaks():
    db = get_db()
    user_orders = db.cursor().execute(
        """
        SELECT PO.UID, O.O_end_time 
        FROM Orders O
        JOIN Process_Order PO ON O.OID = PO.OID
        WHERE O.O_end_time IS NOT NULL
        ORDER BY PO.UID, O.O_end_time
        """).fetchall()
    # conn.close()

    user_order_dates = defaultdict(list)
    for uid, o_end_time in user_orders:
        try:
            date = datetime.strptime(o_end_time, "%Y-%m-%d %H:%M:%S").date()
            user_order_dates[uid].append(date)
        except Exception:
            continue

    user_streaks = {}
    user_vouchers = {}

    for uid, dates in user_order_dates.items():
        unique_dates = sorted(set(dates), reverse=True)
        streak = 0
        today = datetime.today().date()
        for i, d in enumerate(unique_dates):
            if i == 0 and d == today:
                streak += 1
            elif i > 0:
                expected_date = unique_dates[i - 1] - timedelta(days=1)
                if d == expected_date:
                    streak += 1
                else:
                    break
        user_streaks[uid] = streak
        if streak >= 10:
            user_vouchers[uid] = True
        else:
            user_vouchers[uid] = False

    return {"streaks": user_streaks, "vouchers": user_vouchers}

@streak.route("/get-streak", methods=["GET"])
def get_streak():
    uid = int(request.args.get("uid", -1))
    data = calculate_streaks()

    # print(f"Requested UID: {uid}")
    # print("Available streaks:", data["streaks"].keys())

    if uid in data["streaks"]:
        return jsonify({
            "uid": uid,
            "streak": data["streaks"][uid],
            "voucher_awarded": data["vouchers"][uid]
        })
    else:
        return jsonify({"error": "User not found"}), 404
    
@streak.route("/claim-voucher", methods=["POST"])
def claim_voucher():
    uid = int(request.json.get("uid", -1))
    db = get_db()
    claimed = db.cursor().execute(
        " SELECT 1 FROM VoucherClaims WHERE UID = ? ", (uid,)
    ).fetchone()

    # Check Streaks
    streak_data = calculate_streaks()
    if uid not in streak_data["streaks"] or streak_data["streaks"][uid] < 10:
        return jsonify({"success": False, "message": "You don't have a 10-day streak yet."}), 400
    
    # Check Existing Claim
    if claimed:
        return jsonify({"success": False, "message": "Voucher already claimed."}), 400

    # Save Claim
    save_voucher_claim(uid)

    return jsonify({"success": True, "message": "🎉 Voucher Claimed Successfully!!!"})

def save_voucher_claim(uid):
    db = get_db()
    cursor = db.cursor()

    # Check if user already has an unused voucher
    exists = cursor.execute(
        "SELECT 1 FROM Vouchers WHERE UID = ? AND V_used = 0", (uid,)
    ).fetchone()

    if exists:
        return False  # Already has a voucher

    # Insert voucher
    cursor.execute("""
        INSERT INTO Vouchers (UID, V_code, V_discount)
        VALUES (?, ?, ?)
    """, (uid, "CRAVENGERS10", 10.0))  # Or generate unique code
    db.commit()
    return True


def get_user_voucher(uid):
    db = get_db()
    return db.execute("""
        SELECT * FROM Vouchers
        WHERE UID = ? AND V_used = 0
    """, (uid,)).fetchone()


def mark_voucher_used(uid):
    db = get_db()
    db.execute("""
        UPDATE Vouchers
        SET V_used = 1, V_used_date = datetime('now')
        WHERE UID = ? AND V_used = 0
    """, (uid,))
    db.commit()

