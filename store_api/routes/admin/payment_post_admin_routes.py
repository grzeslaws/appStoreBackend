from store_api import app, db
from flask import jsonify, request
from store_api.models import PaymentType, PostType


@app.route("/api/admin/add_post_type", methods=["POST"])
def add_post_type():

    if request.method == "POST":
        post_type = PostType(name=request.json["name"], cost=request.json["cost"])
        db.session.add(post_type)
        db.session.commit()
        return jsonify({"messages": "New post type has been added!"})


@app.route("/api/admin/delete_post_type/<int:id>", methods=["GET"])
def delete_post_type(id):
    post_type = PostType.query.filter_by(id=id).first()
    db.session.delete(post_type)
    db.session.commit()
    return jsonify({"messages": "Post type has been deleted!"})


@app.route("/api/admin/add_payment_type", methods=["POST"])
def add_payment_type():

    if request.method == "POST":
        payment_type = PaymentType(name=request.json["name"], cost=request.json["cost"])
        db.session.add(payment_type)
        db.session.commit()
        return jsonify({"messages": "New payment type has been added!"})


@app.route("/api/admin/delete_payment_type/<int:id>", methods=["GET"])
def delete_payment_type(id):
    payment_type = PaymentType.query.filter_by(id=id).first()
    db.session.delete(payment_type)
    db.session.commit()
    return jsonify({"messages": "Payment type has been deleted!"})
