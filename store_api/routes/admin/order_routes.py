from store_api import app, db
from flask import jsonify
from store_api.models import Order, PostStatus


@app.route("/api/admin/update_post_status_order/<order_uuid>/<int:post_status_id>")
def update_post_status_order(order_uuid, post_status_id):

    order = Order.query.filter_by(order_uuid=order_uuid).first()
    ps = PostStatus.query.filter_by(id=post_status_id).first()
    order.post_status = ps
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Post status has been updated!"})
