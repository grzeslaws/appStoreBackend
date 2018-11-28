from store_api import app
from store_api.models import Order, Product
from flask import jsonify
# from sqlalchemy import desc
from store_api.serializers import get_orderitems, customer_item


@app.route("/api/admin/get_orders/<int:page>/<order_by>")
def get_orders(page, order_by):

    print(order_by)

    orders_data = {}
    orders = []

    if order_by and order_by == "Timestamp":
        orders_data = Order.order_by_timestamp(page, 10)
    elif order_by and order_by == "Status":
        orders_data = Order.order_by_status(page, 10)
    elif order_by and order_by == "Total price":
        orders_data = Order.order_by_total_price(page, 10)
    else:
        orders_data = Order.order_by_timestamp(page, 10)

    for order in orders_data.items:
        order_dict = {}
        order_dict["orderItems"] = get_orderitems(order, Product)
        order_dict["orderUuid"] = order.order_uuid
        order_dict["timestamp"] = order.timestamp
        order_dict["status"] = order.status
        order_dict["totalPrice"] = order.total_price
        order_dict["customer"] = customer_item(order.customer)
        orders.append(order_dict)

    return jsonify({"orders": orders,
                    "has_next": orders_data.has_next,
                    "has_prev": orders_data.has_prev,
                    "next_num": orders_data.next_num,
                    "prev_num": orders_data.prev_num,
                    "pages": orders_data.pages})


@app.route("/api/admin/search_orders/<int:page_number>/", defaults={"query": ""})
@app.route("/api/admin/search_orders/<int:page_number>/<query>")
def search_orders(query, page_number):

    if query is "":
        return get_orders(page_number)

    else:
        orders = Order.query.all()
        search_results = [o for o in orders if o.order_uuid.find(query) != -1]
        orders_result = []

        for order in search_results:
            order_dict = {}
            order_dict["orderItems"] = get_orderitems(order, Product)
            order_dict["orderUuid"] = order.order_uuid
            order_dict["timestamp"] = order.timestamp
            order_dict["status"] = order.status
            order_dict["totalPrice"] = order.total_price
            order_dict["customer"] = customer_item(order.customer)
            orders_result.append(order_dict)

        return jsonify({"orders": orders_result})


# @app.route("/api/admin/get_order/<order_uuid>")
# def get_order(order_uuid):
#     order_data = Order.query.all()

#     orders = []

#     for order in orders_data:
#         order_dict = {}
#         order_dict["orderItems"] = get_orderitems(order, Product)
#         order_dict["orderUuid"] = order.order_uuid
#         order_dict["timestamp"] = order.timestamp
#         order_dict["status"] = order.status
#         order_dict["totalPrice"] = order.total_price
#         order_dict["customer"] = customer_item(order.customer)
#         orders.append(order_dict)

#     return jsonify({"orders": orders})
