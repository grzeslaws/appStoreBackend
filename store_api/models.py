from store_api import db, generate_uuid
import time


cat = db.Table("categories",
               db.Column("category_id", db.Integer, db.ForeignKey(
                   "category.id"), primary_key=True),
               db.Column("product_id", db.Integer, db.ForeignKey(
                   "product.id"), primary_key=True)
               )

col = db.Table("collections",
               db.Column("collection_id", db.Integer, db.ForeignKey(
                   "collection.id"), primary_key=True),
               db.Column("product_id", db.Integer, db.ForeignKey(
                   "product.id"), primary_key=True)
               )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_uuid = db.Column(
        db.String(100), default=generate_uuid)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    image_path = db.Column(db.String(200), nullable=True, default="default.jpg")
    orderitem = db.relationship("Orderitem", backref="product", lazy=True)
    categories = db.relationship("Category", secondary=cat, backref=db.backref("products", lazy="dynamic"))
    collections = db.relationship("Collection", secondary=col, backref=db.backref("products", lazy="dynamic"))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_uuid = db.Column(
        db.String(100), unique=True, default=generate_uuid)
    name = db.Column(db.String(50), nullable=True)
    order = db.relationship("Order", backref="customer", lazy=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_uuid = db.Column(db.String(100), unique=True, default=generate_uuid)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "customer.id"), nullable=True)
    timastamp = db.Column(db.Integer, nullable=False,
                          default=int(time.time()))
    orderitems = db.relationship("Orderitem", backref="order", lazy=True)


class Orderitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=True, default=3)
    order_id = db.Column(db.Integer, db.ForeignKey(
        "order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), nullable=False)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(100))
    password = db.Column(db.String(200))
