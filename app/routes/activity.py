from flask import Blueprint, jsonify,session
from app.models.activity import Activity
from app import db
activity_bp = Blueprint("activity", __name__)

@activity_bp.route("/activities", methods=["GET"])
def get_activities():
    activities = Activity.query.order_by(Activity.created_at.desc()).all()

    return jsonify([
        {
            "user_id": a.user_id,
            "user_name": a.user_name,
            "action": a.action,
            "status": a.status,
            "time": a.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for a in activities
    ])


@activity_bp.route("/activities/clear", methods=["DELETE"])
def clear_activities():
    try:
        db.session.query(Activity).delete()
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "All activity logs cleared"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Failed to clear logs"
        }), 500