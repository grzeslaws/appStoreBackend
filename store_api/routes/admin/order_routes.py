from store_api import app, db
from flask import jsonify
from store_api.models import Order, PostStatus, Product


@app.route("/api/admin/update_post_status_order/<order_uuid>/<int:post_status_id>")
def update_post_status_order(order_uuid, post_status_id):

    order = Order.query.filter_by(order_uuid=order_uuid).first()
    ps = PostStatus.query.filter_by(id=post_status_id).first()
    order.post_status = ps
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Post status has been updated!"})


@app.route("/api/admin/cancel_order/<order_uuid>")
def cancel_order(order_uuid):
    order = Order.query.filter_by(order_uuid=order_uuid).first()
    for oi in order.orderitems:
        p = Product.query.filter_by(id=oi.product_id).first()
        p.quantity = p.quantity + oi.quantity
        db.session.delete(oi)
    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Prodcts has been updated!"}), 200
