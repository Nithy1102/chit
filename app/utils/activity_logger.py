from flask import session
from app import db
from app.models.activity import Activity

def log_activity(action, status=""):
    if "user_id" not in session or "user_name" not in session:
        return

    activity = Activity(
        user_id=session["user_id"],
        user_name=session["user_name"],
        action=action,
        status=status
    )

    db.session.add(activity)
    db.session.commit()
