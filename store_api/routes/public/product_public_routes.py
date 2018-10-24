from store_api import app, db
from flask import request, jsonify, send_from_directory
from store_api.models import Product, Category, Collection
from store_api.serializers import product_item
from sqlalchemy import desc
import os


@app.route("/api/public/get_image/<path:filename>")
def download_file(filename):
    return send_from_directory(os.path.abspath(app.config["UPLOAD_FOLDER"]),
                               filename, as_attachment=False)


@app.route("/api/public/get_all_products/<int:category_id>/<int:page_number>/<int:per_page>")
def get_all_public_products(category_id, page_number, per_page):

    if category_id is 0:
        products = Product.query.order_by(desc(Product.id)).paginate(page=page_number, per_page=per_page)
        productList = []
        for p in products.items:
            productList.append(product_item(p))
        return jsonify({"products": productList,
                        "has_next": products.has_next,
                        "has_prev": products.has_prev,
                        "next_num": products.next_num,
                        "prev_num": products.prev_num,
                        "pages": products.pages})

    else:
        category = Category.query.filter_by(id=category_id).first()
        products = category.products.paginate(page=page_number, per_page=per_page)
        productList = []
        for p in products.items:
            productList.append(product_item(p))
        return jsonify({"products": productList,
                        "has_next": products.has_next,
                        "has_prev": products.has_prev,
                        "next_num": products.next_num,
                        "prev_num": products.prev_num,
                        "pages": products.pages})


@app.route("/api/public/get_product/<product_uuid>", methods=["GET"])
def get_product(product_uuid):

    if request.method == "GET":

        product = Product.query.filter_by(product_uuid=product_uuid).first()
        product_item(product)
        return jsonify(product_item(product))


@app.route("/api/public/remove_one_product/<product_uuid>", methods=["GET"])
def remove_one_product(product_uuid):

    if request.method == "GET":
        p = Product.query.filter_by(product_uuid=product_uuid).first()
        if p.quantity > 0:
            p.quantity = p.quantity - 1
            db.session.commit()
            return jsonify({"message": "One product has been removed!"})
        else:
            return jsonify({"err": "You, can't remove product, the number of products is equal to 0"}), 500


@app.route("/api/public/add_one_product/<product_uuid>", methods=["GET"])
def add_one_product(product_uuid):

    if request.method == "GET":
        p = Product.query.filter_by(product_uuid=product_uuid).first()
        p.quantity = p.quantity + 1
        db.session.commit()
        return jsonify({"message": "One product has been added!"})


@app.route("/api/public/get_products_by_collection/<int:collection_id>/<int:page_number>/<int:per_page>")
def get_products_by_collection(collection_id, page_number, per_page):
    collection = Collection.query.filter_by(id=collection_id).first()
    products = collection.products.paginate(page=page_number, per_page=per_page)
    productList = [product_item(p) for p in products.items]

    return jsonify({"products": productList,
                    "has_next": products.has_next,
                    "has_prev": products.has_prev,
                    "next_num": products.next_num,
                    "prev_num": products.prev_num,
                    "pages": products.pages})
