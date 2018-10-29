from store_api import app, db
from flask import jsonify
from store_api.models import Product, Category, Admin, Collection, Customer, PaymentType, PostType
from werkzeug.security import generate_password_hash


def categories_init():
    for i in range(0, 12):
        if i == 0:
            t = Category(name="all")
        else:
            t = Category(name="Category " + str(i))
        db.session.add(t)

    db.session.commit()


def collections_init():
    c1 = Collection(name="Home collection")
    c2 = Collection(name="Carousel")
    db.session.add(c1)
    db.session.add(c2)
    db.session.commit()


def product_init():

    for i in range(1, 40):
        if i < 11 and i > 1:
            p = Product(name="Product " + str(i), price=i*10, quantity=i*2, description="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
            c = Category.query.filter_by(id=i).first()
            c.products.append(p)
            col = Collection.query.filter_by(id=1).first()
            col.products.append(p)
            db.session.add(col)
            db.session.add(p)
            db.session.add(c)
        else:
            c = Category.query.filter_by(id=1).first()
            p = Product(name="Product " + str(i), price=i*10, quantity=i*2)
            c.products.append(p)
            db.session.add(p)

    db.session.commit()
    c = Category.query.filter_by(id=1).first()


def admin_init():
    hashed_password = generate_password_hash("admin", method="sha256")
    a = Admin(admin_name="admin", password=hashed_password)
    db.session.add(a)
    db.session.commit()


def init_customer():
    new_customer = Customer(first_name="Tom")
    db.session.add(new_customer)
    db.session.commit()


def init_payment_type():
    cash_on_delivery = PaymentType(name="cash_on_delivery", cost=5)
    transfer = PaymentType(name="transfer", cost=5)

    db.session.add(cash_on_delivery)
    db.session.add(transfer)
    db.session.commit()


def init_post_type():
    normal = PostType(name="normal", cost=15)
    express = PostType(name="express", cost=0)

    db.session.add(normal)
    db.session.add(express)
    db.session.commit()


@app.route("/")
def index():
    db.drop_all()
    db.create_all()
    categories_init()
    collections_init()
    admin_init()
    product_init()
    init_payment_type()
    init_post_type()
    # init_customer()
    return jsonify({"message": "Home"})
