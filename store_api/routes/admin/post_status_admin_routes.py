from store_api import app, db
from flask import jsonify, request
from store_api.models import PostStatus, ColorPostStatus
from store_api.routes import token_required
from store_api.serializers import get_ps


@app.route("/api/admin/add_post_status", methods=["POST"])
@token_required
def add_post_status(current_user):
    if request.method == "POST":
        color = request.json["color"]
        post_status = PostStatus(name=request.json["name"], color=ColorPostStatus(color))
        db.session.add(post_status)
        db.session.commit()

        return jsonify({"message": "Post status has been added!"})


@app.route("/api/admin/delete_post_status/<int:id>")
@token_required
def delete_post_status(current_user, id):
    post_status = PostStatus.query.filter_by(id=id).first()
    db.session.delete(post_status)
    db.session.commit()
    return jsonify({"message": "Post status has been deleted!"})


@app.route("/api/admin/get_post_statuses")
@token_required
def get_post_statuses(current_user):
    post_statuses = PostStatus.query.all()

    return jsonify([get_ps(ps) for ps in post_statuses]), 200
