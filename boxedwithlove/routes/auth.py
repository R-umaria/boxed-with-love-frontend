from flask import Blueprint, redirect, render_template, request, session, url_for

from boxedwithlove.services.auth_service import AuthError, authenticate, create_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        user = authenticate(email)
        if not user:
            return render_template(
                "auth/login.html", error="We couldn't find that email."
            )
        session["user_id"] = user.id
        next_url = request.args.get("next") or url_for("main.home")
        return redirect(next_url)
    return render_template("auth/login.html")


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "")
        name = request.form.get("name", "")
        try:
            user = create_user(email, name)
        except AuthError as exc:
            return render_template("auth/signup.html", error=str(exc))
        session["user_id"] = user.id
        next_url = request.args.get("next") or url_for("main.home")
        return redirect(next_url)
    return render_template("auth/signup.html")


@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main.home"))
