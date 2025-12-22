from  app import db
from flask import Blueprint, jsonify
from app.models.whatsapp import WhatsAppMessage
from app.models.user import User

messages_bp = Blueprint(
    "admin_messages",
    __name__,
    url_prefix="/api/admin"
)

@messages_bp.route("/whatsapp-messages", methods=["GET"])
def get_whatsapp_messages():
    messages = WhatsAppMessage.query \
        .order_by(WhatsAppMessage.created_at.desc()) \
        .all()

    return jsonify([m.to_dict() for m in messages])

@messages_bp.route("/profile", methods=["GET"])
def get_admin_profile():


    admin = User.query.filter_by(role="admin").first()

    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    return jsonify({
        "id": admin.id,
        "username": admin.username,
        "phone": admin.phone,
        "role": admin.role
    }), 200
# ===============================
@messages_bp.route("/whatsapp-messages/clear", methods=["DELETE"])
def clear_whatsapp_messages():
    try:
        db.session.query(WhatsAppMessage).delete()
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "WhatsApp message history cleared"
        })

    except Exception:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "Failed to clear WhatsApp messages"
        }), 500
