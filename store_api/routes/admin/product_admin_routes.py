from werkzeug.utils import secure_filename
from store_api import app, db
from flask import request, jsonify
from store_api.models import Product, Category, Collection
from store_api.serializers import product_item
from sqlalchemy import desc
from store_api.routes import token_required
from store_api.utils import image_folder_path, image_path_with_options
from store_api import settings
import shutil
import os
from PIL import Image
from io import BytesIO


def categories_init():
    for i in range(0, 10):
        t = Category(name="Category " + str(i))
        db.session.add(t)

    db.session.commit()


@app.route("/api/admin/products", methods=["POST"])
def add_product_route():
    if request.method == "POST":
        p = Product(name=request.json["name"])
        db.session.add(p)
        db.session.commit()

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


@app.route("/api/admin/edit_product/<product_uuid>", methods=["PUT", "GET"])
def edit_product(product_uuid):

    if request.method == "PUT":
        p = Product.query.filter_by(product_uuid=product_uuid).first()
        p.name = request.json["name"]
        if "description" in request.json:
            p.description = request.json["description"]
        if request.json["price"] is not 0:
            p.price = request.json["price"]
        if request.json["quantity"] is not 0:
            p.quantity = request.json["quantity"]
        if request.json["categoryId"] is not 0:
            cat = Category.query.filter_by(id=request.json["categoryId"]).first()
            cat.products.append(p)
        if request.json["collectionId"] is not 0:
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
        shutil.rmtree(image_folder_path(product_uuid))

        return jsonify({"message": "Product has been deleted!"})


@app.route("/api/admin/edit_product_image/<product_uuid>", methods=["POST"])
def edit_product_image(product_uuid):
    if request.method == "POST":
        if request.files:

            file = request.files["file"]
            file_name = secure_filename(file.filename)
            product_image_folder = image_folder_path(product_uuid)
            allowed_extensions = file_name.lower().endswith(settings.ALLOWED_EXTENSIONS)

            if allowed_extensions:
                if os.path.exists(product_image_folder):
                    shutil.rmtree(product_image_folder)

                os.makedirs(product_image_folder)

                f = Image.open(BytesIO(file.read()), mode="r")
                for key, size in settings.IMAGE_SIZES.items():
                    f_name, ext = os.path.splitext(file_name)
                    temp_img = f.copy()
                    temp_img.thumbnail(size)
                    temp_img.save(os.path.join(product_image_folder, image_path_with_options(file_name, key)))

                p = Product.query.filter_by(product_uuid=product_uuid).first()
                p.image_path = file_name
                db.session.commit()
                return jsonify({"message": "Image has been changed!"}), 201
            else:
                return jsonify({"message": "Not allowed extension!"}), 400
        else:
            return jsonify({"message": "There is no file!"}), 400
