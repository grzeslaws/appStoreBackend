from werkzeug.utils import secure_filename
from store_api import app, db, generate_uuid
from flask import request, jsonify
from store_api.models import Product, Category, Collection
from store_api.serializers import product_item
from sqlalchemy import desc
from store_api.routes import token_required
import time
import os

imagePath = None
productUuid = None


def categories_init():
    for i in range(0, 10):
        t = Category(name="Category " + str(i))
        db.session.add(t)

    db.session.commit()


def save_image():

    if request.files:
        global productUuid
        global imagePath
        productUuid = generate_uuid()
        file = request.files["file"]
        file_name = secure_filename(file.filename)
        imagePath = productUuid + "_" + file_name
        file.save(os.path.join(
            app.config["UPLOAD_FOLDER"], imagePath))


def product_describe():

    if request.json:
        global productUuid
        global imagePath
        p = Product(name=request.json["name"], product_uuid=productUuid, image_path=imagePath)
        db.session.add(p)
        db.session.commit()

        productUuid = generate_uuid()
        imagePath = None


def add_product():
    save_image()
    time.sleep(0.1)
    product_describe()


@app.route("/api/admin/add_product_image", methods=["POST"])
@app.route("/api/admin/products", methods=["POST"])
def add_product_route():
    if request.method == "POST":
        add_product()

        return jsonify({"message": "Product has been added!"}), 201


@app.route("/api/admin/get_all_products/<int:page_number>/<int:per_page>", methods=["GET"])
@token_required
def get_all_products(current_user, page_number, per_page):

    if request.method == "GET":

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


@app.route("/api/admin/edit_product/<product_uuid>", methods=["POST", "PUT", "GET"])
def edit_product(product_uuid):

    if request.method == "PUT":
        p = Product.query.filter_by(product_uuid=product_uuid).first()
        p.name = request.json["name"]
        if request.json["categoryId"] is not None:
            cat = Category.query.filter_by(id=request.json["categoryId"]).first()
            cat.products.append(p)
        if request.json["collectionId"] is not None:
            coll = Collection.query.filter_by(id=request.json["collectionId"]).first()
            coll.products.append(p)
        db.session.commit()
        return jsonify({"message": "Product has been updated!"})

    if request.method == "GET":
        p = Product.query.filter_by(product_uuid=product_uuid).first()
        db.session.delete(p)
        db.commit()


@app.route("/api/admin/delete_product/<product_uuid>", methods=["GET"])
def delete_product(product_uuid):
    if request.method == "GET":
        p = Product.query.filter_by(product_uuid=product_uuid).first()
        db.session.delete(p)
        db.session.commit()

        return jsonify({"message": "Product has been deleted!"})


@app.route("/api/admin/edit_product_image/<product_uuid>", methods=["POST"])
def edit_product_image(product_uuid):
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file_name = secure_filename(file.filename)
            imagePath = product_uuid + "_" + file_name
            file.save(os.path.join(
                app.config["UPLOAD_FOLDER"], imagePath))

            p = Product.query.filter_by(product_uuid=product_uuid).first()
            p.image_path = imagePath
            db.session.commit()
        return jsonify({"message": "Image has been changed!"})
    return jsonify({"message": "Image has been changed!"})
