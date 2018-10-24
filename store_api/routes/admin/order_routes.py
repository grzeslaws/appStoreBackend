from store_api import app, db
from flask import request, jsonify
from store_api.models import Customer, Product, Order, Category, Orderitem


def init_order():
    for i in range(0, 30):

        c = Customer(name="Customer " + str(i))
        o = Order(customer=c)
        db.session.add(c)
        db.session.add(o)

        p = Product(name="Pen " + str(i))
        t = Category.query.filter_by(id=3).first()
        t.products.append(p)
        oi = Orderitem(order=o, product=p)
        db.session.add(p)
        db.session.add(oi)

    db.session.commit()


@app.route("/api/order_details/<order_id>", methods=["GET"])
def order_details(order_id):
    if request.method == "GET":

        o = Order.query.filter_by(id=order_id).first()
        oi = Orderitem.query.filter_by(order_id=o.id).all()
        oi_items = []

        for oii in oi:
            oii_obj = {}
            oii_obj["quantity"] = oii.quantity
            oii_obj["product_id"] = oii.product_id
            oii_obj["product_name"] = oii.product.name
            oi_items.append(oii_obj)

        return jsonify({
            "order_id": o.id,
            "customer_id": o.customer_id,
            "orderitems": oi_items
        }), 200
