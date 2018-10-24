from store_api import app, db
from flask import jsonify, request
from store_api.models import Category, Product
from store_api.routes import token_required


@app.route("/api/admin/add_category", methods=["POST"])
@token_required
def add_categories(current_user):
    if request.method == "POST":
        category = Category(name=request.json["categoryName"])
        db.session.add(category)
        db.session.commit()

        return jsonify({"message": "Category has been added!"})


@app.route("/api/admin/delete_category/<int:id>")
@token_required
def delete_category(current_user, id):
    category = Category.query.filter_by(id=id).first()
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category has been deleted!"})


@app.route("/api/admin/delete_category_for_product/<int:category_id>/<product_uuid>")
def delete_category_for_product(category_id, product_uuid):
    c = Category.query.filter_by(id=category_id).first()
    p = Product.query.filter_by(product_uuid=product_uuid).first()
    c.products.remove(p)
    db.session.commit()
    return jsonify({"message": "Product has been deleted!"})
