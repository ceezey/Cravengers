from . import get_db
import uuid
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

    print(f"Requested UID: {uid}")
    print("Available streaks:", data["streaks"].keys())

    if uid in data["streaks"]:
        db = get_db()
        user_row = db.execute("SELECT U_reward_shown_day FROM Users WHERE UID = ?", (uid,)).fetchone()

        return jsonify({
            "uid": uid,
            "streak": data["streaks"][uid],
            "voucher_awarded": data["vouchers"][uid],
            "last_reward_shown_day": user_row["U_reward_shown_day"] if user_row else 0
        })
    else:
        return jsonify({"error": "User not found"}), 404
    
@streak.route("/claim-voucher", methods=["POST"])
def claim_voucher():
    uid = int(request.json.get("uid", -1))
    db = get_db()
    claimed = db.cursor().execute(
        " SELECT 1 FROM Vouchers WHERE UID = ? ", (uid,)
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
    
    # Generate unique code and expiry (7 days later)
    code = f"CRAV-{uuid.uuid4().hex[:8].upper()}"
    expiry = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    # Insert voucher
    cursor.execute("""
        INSERT INTO Vouchers (UID, V_code, V_discount, V_expiry_date)
        VALUES (?, ?, ?, ?)
    """, (uid, code, 50.0, expiry))
    db.commit()
    return True


@streak.route("/get-vouchers", methods=["GET"])
def get_vouchers():
    uid = int(request.args.get("uid", -1))
    db = get_db()
    vouchers = db.execute("""
        SELECT VID, V_code, V_discount
        FROM Vouchers
        WHERE UID = ? AND V_used = 0 AND V_expiry_date > datetime('now')
    """, (uid,)).fetchall()

    return jsonify([
        {
            "vid": v["VID"],
            "code": v["V_code"],
            "discount": v["V_discount"]
        }
        for v in vouchers
    ])

@streak.route("/use-voucher", methods=["POST"])
def use_voucher_route():
    data = request.get_json()
    uid = int(data.get("uid", -1))
    vid = int(data.get("vid", -1))

    return use_voucher(uid, vid)  # Call logic function

def use_voucher(uid: int, vid: int):
    if uid == -1 or vid == -1:
        return jsonify({"success": False, "message": "Missing user or voucher ID"}), 400

    db = get_db()
    result = db.execute("""
        UPDATE Vouchers
        SET V_used = 1, V_used_date = datetime('now')
        WHERE VID = ? AND UID = ? AND V_used = 0
    """, (vid, uid))

    db.commit()

    if result.rowcount == 0:
        return jsonify({"success": False, "message": "Voucher not valid or already used."}), 400

    return jsonify({"success": True, "message": "Voucher marked as used."})

@streak.route('/mark-reward-shown', methods=['POST'])
def mark_reward_shown():
    uid = request.args.get('uid')
    day = request.args.get('day')

    if not uid or not day:
        return jsonify({"error": "Missing parameters"}), 400

    try:
        uid = int(uid)
        day = int(day)
    except ValueError:
        return jsonify({"error": "Invalid day or UID"}), 400

    db = get_db()
    current = db.execute("SELECT U_reward_shown_day FROM Users WHERE UID = ?", (uid,)).fetchone()
    if not current:
        return jsonify({"error": "User not found"}), 404

    if day > (current["U_reward_shown_day"] or 0):
        db.execute("UPDATE Users SET U_reward_shown_day = ? WHERE UID = ?", (day, uid))
        db.commit()

    return jsonify({"success": True})

# Getting Voucher for Testing Purposes (Bypasses 10-Day Streak Requirement)
@streak.route("/issue-test-voucher/<int:uid>", methods=["POST"])
def issue_test_voucher(uid):
    """
    For testing only: force-issue a 50% voucher to user <uid>.
    """
    db = get_db()
    cursor = db.cursor()

    # Check if there’s already an unused, unexpired voucher for this user:
    exists = cursor.execute(
        "SELECT 1 FROM Vouchers WHERE UID = ? AND V_used = 0 AND (V_expiry_date IS NULL OR V_expiry_date > datetime('now'))",
        (uid,)
    ).fetchone()
    if exists:
        return jsonify({"success": False, "message": "User already has an active voucher."}), 400

    # Create a “test” voucher code that lasts, say, 7 days from now:

    code = f"DISC-{uuid.uuid4().hex[:6].upper()}"
    expiry = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO Vouchers (UID, V_code, V_discount, V_expiry_date)
        VALUES (?, ?, ?, ?)
    """, (uid, code, 50.0, expiry))
    db.commit()

    return jsonify({
        "success": True,
        "message": f"Test voucher '{code}' issued (50% off, expires {expiry})."
    })
