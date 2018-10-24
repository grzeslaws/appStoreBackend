from functools import wraps
from flask import request, jsonify
import jwt
from store_api import app
from store_api.models import Admin


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        if token == "null" or token is None:
            return jsonify({"message": "Token is missing!"}), 403
        try:
            data = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = Admin.query.filter_by(
                id=data["id"]).first()
        except Exception:  # noqa: E722
            jsonify({"message": "Token is invalid!"}), 403
        try:
            return f(current_user, *args, **kwargs)
        except UnboundLocalError as err:
            return jsonify({"err": str(err) + " - This probably means your credentials are wrong!"}), 403

    return decorated
