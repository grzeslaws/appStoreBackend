from store_api import app, db
from flask import jsonify
from store_api.models import Product, Category, Admin, Collection, Customer
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
            p = Product(name="Product " + str(i), price=i*10, quantity=i*2)
            c = Category.query.filter_by(id=i).first()
            c.products.append(p)
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
    new_customer = Customer(name="Tom")
    db.session.add(new_customer)
    db.session.commit()


@app.route("/")
def index():
    db.drop_all()
    db.create_all()
    categories_init()
    collections_init()
    admin_init()
    product_init()
    init_customer()
    return jsonify({"message": "Home"})
