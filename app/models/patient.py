from app import db
import json

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # BASIC
    branch = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.String(200))

    # RIGHT EYE (OD)
    sph_od = db.Column(db.String(20))
    cyl_od = db.Column(db.String(20))
    axis_od = db.Column(db.String(20))
    add_od = db.Column(db.String(20))

    # LEFT EYE (OS)
    sph_os = db.Column(db.String(20))
    cyl_os = db.Column(db.String(20))
    axis_os = db.Column(db.String(20))
    add_os = db.Column(db.String(20))

    # VISION
    vision_od = db.Column(db.String(20))
    vision_os = db.Column(db.String(20))
    pd = db.Column(db.String(20))

    # EYEWEAR
    frameType = db.Column(db.String(50))
    lensType = db.Column(db.String(50))
    contactLens = db.Column(db.String(50))
    coatings = db.Column(db.Text)  # JSON list

    # ADDITIONAL
    systemicHistory = db.Column(db.Text)
    ocularHistory = db.Column(db.Text)
    eyeConditions = db.Column(db.Text)
    notes = db.Column(db.Text)
    nextAppointment = db.Column(db.String(20))

    # PAYMENT
    total = db.Column(db.Float)
    advance = db.Column(db.Float)
    remaining = db.Column(db.Float)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "branch": self.branch,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,

            "sph_od": self.sph_od,
            "cyl_od": self.cyl_od,
            "axis_od": self.axis_od,
            "add_od": self.add_od,

            "sph_os": self.sph_os,
            "cyl_os": self.cyl_os,
            "axis_os": self.axis_os,
            "add_os": self.add_os,

            "vision_od": self.vision_od,
            "vision_os": self.vision_os,
            "pd": self.pd,

            "frameType": self.frameType,
            "lensType": self.lensType,
            "contactLens": self.contactLens,
            "coatings": json.loads(self.coatings) if self.coatings else [],

            "systemicHistory": self.systemicHistory,
            "ocularHistory": self.ocularHistory,
            "eyeConditions": self.eyeConditions,
            "notes": self.notes,
            "nextAppointment": self.nextAppointment,

            "total": self.total,
            "advance": self.advance,
            "remaining": self.remaining
        }
