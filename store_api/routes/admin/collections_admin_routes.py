from store_api import app, db
from flask import jsonify, request
from store_api.models import Collection, Product
from store_api.routes import token_required


@app.route("/api/admin/add_collection", methods=["POST"])
@token_required
def add_collection(current_user):
    if request.method == "POST":
        collection = Collection(name=request.json["collectionName"])
        db.session.add(collection)
        db.session.commit()

        return jsonify({"message": "Collection has been added!"})


@app.route("/api/admin/delete_collection/<int:id>")
@token_required
def delete_collection(current_user, id):
    collection = Collection.query.filter_by(id=id).first()
    db.session.delete(collection)
    db.session.commit()
    return jsonify({"message": "Collection has been deleted!"})


@app.route("/api/admin/delete_collection_for_product/<int:collection_id>/<product_uuid>")
def delete_collection_for_product(collection_id, product_uuid):
    c = Collection.query.filter_by(id=collection_id).first()
    p = Product.query.filter_by(product_uuid=product_uuid).first()
    c.products.remove(p)
    db.session.commit()
    return jsonify({"message": "Collection has been removed from product!"})
