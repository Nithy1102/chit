from flask import Blueprint, request, jsonify, session, redirect, render_template
from app.models.patient import Patient
from app.models.whatsapp import WhatsAppMessage
from app.models.user import User
from app import db
from datetime import datetime
import json

patient_bp = Blueprint("patient", __name__)

def login_required():
    return "user_id" in session


def log_whatsapp(event, message):

    admin = User.query.filter_by(role="admin").first()
    if not admin or not admin.phone:
        return None

    log = WhatsAppMessage(
        event=event,
        phone=admin.phone,
        message=message,
        status="sent",
        created_at=datetime.utcnow()
    )

    db.session.add(log)

  
    return {
        "phone": admin.phone,
        "message": message
    }


@patient_bp.route("/add-patient-page")
def add_patient_page():
    if not login_required():
        return redirect("/login")
    return render_template("Add patient.html")


# -------------------------------
# ADD PATIENT
# -------------------------------
@patient_bp.route("/add-patient", methods=["POST"])
def add_patient():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    try:
        patient = Patient(
            branch=data.get("branch"),
            name=data.get("name"),
            age=data.get("age"),
            gender=data.get("gender"),
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address"),

            sph_od=data.get("sph_od"),
            cyl_od=data.get("cyl_od"),
            axis_od=data.get("axis_od"),
            add_od=data.get("add_od"),

            sph_os=data.get("sph_os"),
            cyl_os=data.get("cyl_os"),
            axis_os=data.get("axis_os"),
            add_os=data.get("add_os"),

            vision_od=data.get("vision_od"),
            vision_os=data.get("vision_os"),
            pd=data.get("pd"),

            frameType=data.get("frameType"),
            lensType=data.get("lensType"),
            contactLens=data.get("contactLens"),
            coatings=json.dumps(data.get("coatings", [])),

            systemicHistory=data.get("systemicHistory"),
            ocularHistory=data.get("ocularHistory"),
            eyeConditions=data.get("eyeConditions"),
            notes=data.get("notes"),
            nextAppointment=data.get("nextAppointment"),

            total=data.get("total"),
            advance=data.get("advance"),
            remaining=data.get("remaining")
        )

        db.session.add(patient)

        # WhatsApp log
        wa=log_whatsapp(
            "new_patient",
            f"🔔 New patient added\n"
            f"Name: {patient.name}\n"
            f"Branch: {patient.branch}\n"
            f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )

        db.session.commit()

        return jsonify({
    "status": "success",
    "id": patient.id,
    "whatsapp": wa   # ✅ VERY IMPORTANT
})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# GET SINGLE PATIENT
# -------------------------------
@patient_bp.route("/patient/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"status": "error", "message": "Patient not found"}), 404
    return jsonify(patient.to_dict())


# -------------------------------
# UPDATE PATIENT
# -------------------------------
@patient_bp.route("/update-patient/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

    try:
        for field, value in data.items():
            if hasattr(patient, field):
                setattr(patient, field, value)

        if "coatings" in data:
            patient.coatings = json.dumps(data["coatings"])

        # WhatsApp log
        wa=log_whatsapp(
            "patient_updated",
            f"✏️ Patient details updated\n"
            f"Name: {patient.name}\n"
            f"Branch: {patient.branch}\n"
            f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )

        db.session.commit()
        return jsonify({"status": "success", "whatsapp": wa})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# GET ALL PATIENTS
# -------------------------------
@patient_bp.route("/api/patients", methods=["GET"])
def get_all_patients():
    patients = Patient.query.order_by(Patient.id.desc()).all()
    return jsonify([p.to_dict() for p in patients])


# -------------------------------
# DELETE PATIENT
# -------------------------------
@patient_bp.route("/delete-patient/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({"status": "error", "message": "Patient not found"}), 404

    try:
        # WhatsApp log BEFORE delete
        wa=log_whatsapp(
            "patient_deleted",
            f"❌ Patient deleted\n"
            f"Name: {patient.name}\n"
            f"Branch: {patient.branch}\n"
            f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        )

        db.session.delete(patient)
        db.session.commit()
        return jsonify({"status": "success", "whatsapp": wa})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------------------
# PAYMENTS VIEW
# -------------------------------
@patient_bp.route("/payments-view", methods=["GET"])
def get_payments():
    patients = Patient.query.order_by(Patient.created_at.desc()).all()
    payments = []

    for p in patients:
        payments.append({
            "name": p.name,
            "branch": p.branch,
            "date": p.created_at.strftime("%Y-%m-%d"),
            "amount": p.total
        })

    return jsonify(payments)
