from flask import Blueprint, render_template, redirect, session

pages_bp = Blueprint("pages", __name__)


def login_required():
    return "user_id" in session


@pages_bp.route("/")
def root():
    return redirect("/login")


@pages_bp.route("/login")
def login():
    return render_template("Login.html")


@pages_bp.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect("/login")
    return render_template("Home.html")


@pages_bp.route("/patients")
def patients():
    if not login_required():
        return redirect("/login")
    return render_template("Patient records.html")





@pages_bp.route("/payments")
def payments():
    if not login_required():
        return redirect("/login")
    return render_template("view payment.html")


@pages_bp.route("/active")
def activity():
    if not login_required():
        return redirect("/login")
    return render_template("Activity Log.html")


@pages_bp.route("/settings")
def settings():
    if not login_required():
        return redirect("/login")
    return render_template("settings.html")


@pages_bp.route("/notifications")
def notifications():
    if not login_required():
        return redirect("/login")
    return render_template("Notification.html")

@pages_bp.route("/signup")
def signup():
    if not login_required():
        return redirect("/login")
    return render_template("signup.html")