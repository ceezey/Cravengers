import sqlite3
from . import get_db
from datetime import datetime, timedelta
from collections import defaultdict
from flask import (
    Blueprint, flash, session, 
    request, jsonify                   
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

@streak.route("/streak/<int:uid>", methods=["GET"])
def get_streak(uid):
    data = calculate_streaks()
    streaks = data["streaks"]
    vouchers = data["vouchers"]

    if uid in streaks:
        return jsonify({
            "uid": uid,
            "streak": streaks[uid],
            "voucher_awarded": vouchers[uid]
        })
    else:
        return jsonify({"error": "User not found"}), 404