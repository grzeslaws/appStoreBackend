from store_api import app
from flask import jsonify, request
from store_api.models import Admin
from werkzeug.security import check_password_hash
import jwt
import datetime


@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        a = Admin.query.filter_by(admin_name=request.json["name"]).first()
        if check_password_hash(a.password, request.json["password"]):
            data = {
                "id": a.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=280)
            }
            token = jwt.encode(
                data, app.config["SECRET_KEY"], "HS256").decode("utf-8")
            return jsonify({"token": token}), 200
        else:
            return None, 401
