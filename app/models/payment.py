from app import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer)
    amount = db.Column(db.Float)
    payment_date = db.Column(db.DateTime, server_default=db.func.now())
