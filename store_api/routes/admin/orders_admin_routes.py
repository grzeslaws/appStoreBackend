from store_api import app
from store_api.models import Order, Product
from flask import jsonify
from store_api.serializers import get_orderitems, customer_item


@app.route("/api/admin/get_orders")
def get_orders():
    orders_data = Order.query.all()

    orders = []

    for order in orders_data:
        order_dict = {}
        order_dict["orderItems"] = get_orderitems(order, Product)
        order_dict["orderUuid"] = order.order_uuid
        order_dict["timestamp"] = order.timastamp
        order_dict["status"] = order.status
        order_dict["totalPrice"] = order.total_price
        order_dict["customer"] = customer_item(order.customer)
        orders.append(order_dict)

    return jsonify({"orders": orders})


# @app.route("/api/admin/get_order/<order_uuid>")
# def get_order(order_uuid):
#     order_data = Order.query.all()

#     orders = []

#     for order in orders_data:
#         order_dict = {}
#         order_dict["orderItems"] = get_orderitems(order, Product)
#         order_dict["orderUuid"] = order.order_uuid
#         order_dict["timestamp"] = order.timastamp
#         order_dict["status"] = order.status
#         order_dict["totalPrice"] = order.total_price
#         order_dict["customer"] = customer_item(order.customer)
#         orders.append(order_dict)

#     return jsonify({"orders": orders})
