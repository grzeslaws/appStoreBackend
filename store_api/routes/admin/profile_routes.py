from store_api import app
from flask import jsonify, request
from store_api.models import Admin
from store_api.routes import token_required


@app.route("/api/admin/profile", methods=["GET"])
@token_required
def admin_profile(current_user):
    if request.method == "GET" and current_user:
        p = Admin.query.filter_by(id=current_user.id).first()
        admin_profile = {}
        admin_profile["admin_name"] = p.admin_name
        admin_profile["id"] = p.id
        return jsonify({"admin_profile": admin_profile})
