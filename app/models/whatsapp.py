from app import db
from datetime import datetime

class WhatsAppMessage(db.Model):
    __tablename__ = "whatsapp_message_logs"

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="sent")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index("idx_whatsapp_created_at", "created_at"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "event": self.event,
            "phone": self.phone,
            "message": self.message,
            "status": self.status,
            "sent_at": self.created_at.isoformat()
        }
