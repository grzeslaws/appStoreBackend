from store_api import db, generate_uuid
import time
from sqlalchemy import desc


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
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(200), nullable=True, default="default.jpg")
    orderitem = db.relationship("Orderitem", backref="product", lazy=True)
    categories = db.relationship("Category", secondary=cat, backref=db.backref("products", lazy="dynamic"))
    collections = db.relationship("Collection", secondary=col, backref=db.backref("products", lazy="dynamic"))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_uuid = db.Column(
        db.String(100), unique=True, default=generate_uuid)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    street = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    zip_code = db.Column(db.String(50), nullable=True)
    telephone = db.Column(db.String(50), nullable=True)
    order = db.relationship("Order", backref="customer", lazy=True)


class Order(db.Model):
    page = 1
    per_page = 10
    id = db.Column(db.Integer, primary_key=True)
    order_uuid = db.Column(db.String(100), unique=True, default=generate_uuid)
    order_pauy_uuid = db.Column(db.String(100), unique=True, nullable=True)
    total_price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        "customer.id"), nullable=True)
    timestamp = db.Column(db.Integer, nullable=False,
                          default=int(time.time()))
    orderitems = db.relationship("Orderitem", backref="order", lazy=True)

    @classmethod
    def order_by_timestamp(self, page, per_page):
        return self.query.order_by(desc(self.timestamp)).paginate(page=page, per_page=self.per_page)

    @classmethod
    def order_by_status(self, page, per_page):
        return self.query.order_by(desc(self.status)).paginate(page=page, per_page=self.per_page)

    @classmethod
    def order_by_total_price(self, page, per_page):
        return self.query.order_by(desc(self.total_price)).paginate(page=page, per_page=self.per_page)


class Orderitem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=True, default=3)
    order_id = db.Column(db.Integer, db.ForeignKey(
        "order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), nullable=False)


class PaymentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=True)


class PostType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=True)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(100))
    password = db.Column(db.String(200))
