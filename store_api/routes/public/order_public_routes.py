from store_api import app, db
from store_api.models import Order, Orderitem, Product
from store_api.serializers import product_item_in_order, product_item_for_order_payu
from flask import jsonify, request
import urllib.parse
import urllib.request
import certifi
import json

import requests


@app.route("/api/public/create_order", methods=["POST"])
def create_order():

    if request.method == "POST":
        order_items = request.json["orderItems"]
        order = Order(total_price=request.json["totalPrice"])
        db.session.add(order)

        for oi in order_items:
            p = Product.query.filter_by(product_uuid=oi["product"]["productUuid"]).first()
            order_item = Orderitem(order=order, product=p, quantity=oi["quantity"])
            db.session.add(order_item)

        db.session.commit()

    return jsonify({"orderUuid": order.order_uuid}), 200


@app.route("/api/public/get_order/<order_uuid>")
def get_order(order_uuid):
    order = Order.query.filter_by(order_uuid=order_uuid).first()

    order_items = []

    for oi in order.orderitems:
        p = Product.query.filter_by(id=oi.product_id).first()
        product = {}
        product["product"] = product_item_in_order(p)
        product["quantity"] = oi.quantity
        order_items.append(product)

    return jsonify({"orderItems": order_items, "orderUuid": order.order_uuid,
                    "timestamp": order.timastamp, "status": order.status, "totalPrice": order.total_price}), 200


@app.route("/api/public/get_access_token/<order_uuid>")
def get_access_token(order_uuid):

    data = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": 145227,
                                   "client_secret": "12f071174cb7eb79d4aac5bc2f07563f"})
    data = data.encode("ascii")
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    req = urllib.request.Request('https://secure.payu.com/pl/standard/user/oauth/authorize', data, headers)

    with urllib.request.urlopen(req, cafile=certifi.where()) as response:

        return send_order(response.read(), order_uuid)


def send_order(access_token, order_uuid):
    at = json.loads(access_token)["access_token"]

    order = Order.query.filter_by(order_uuid=order_uuid).first()

    order_payload = {}
    order_payload["buyer"] = {}
    order_items = []

    for oi in order.orderitems:
        p = Product.query.filter_by(id=oi.product_id).first()
        order_items.append(product_item_for_order_payu(p, oi.quantity))

    order_payload["notifyUrl"] = "https://app-store-backend.herokuapp.com/notify"
    order_payload["customerIp"] = "127.0.0.1"
    order_payload["merchantPosId"] = "145227"
    order_payload["description"] = "RTV market"
    order_payload["currencyCode"] = "PLN"
    order_payload["totalAmount"] = order.__dict__["total_price"]
    order_payload["extOrderId"] = order.__dict__["order_uuid"]
    order_payload["buyer"]["email"] = "grzesiek.supel@example.com"
    order_payload["buyer"]["phone"] = "654111654"
    order_payload["buyer"]["firstName"] = "Grzesiek"
    order_payload["buyer"]["lastName"] = "Supel"
    order_payload["buyer"]["language"] = "pl"
    order_payload["products"] = order_items

    url = "https://secure.payu.com/api/v2_1/orders/"
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + at,
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", url, data=json.dumps(order_payload), headers=headers, allow_redirects=False)

    print(response.json()["redirectUri"])
    return jsonify({"linkToPayment": response.json()["redirectUri"]})


@app.route("/notify", methods=["POST"])
def notify():
    if request.method == "POST":
        requestOrder = request.json["order"]

        print("requestOrder: ", requestOrder)
        print("requestOrder['status']: ", requestOrder["status"])

        order = Order.query.filter_by(order_uuid=requestOrder["extOrderId"]).first()
        order.status = requestOrder["status"]
        order.order_pauy_uuid = requestOrder["orderId"]

        db.session.add(order)
        db.session.commit()

        order_test = Order.query.filter_by(order_uuid=requestOrder["extOrderId"]).first()
        print(order_test.__dict__)
        print("order_test.__dict__['status']: ", order_test.__dict__["status"])

        return jsonify({"status": requestOrder})


# {'orderId': 'F683XDD4ZJ181024GUEST000P01', 'extOrderId': '8af6d4a2-c667-43c2-80e6-ad07d6fb9e9d', 'orderCreateDate': '2018-10-24T11:35:08.067+02:00', 'notifyUrl': 'https://app-store-backend.herokuapp.com/notify', 'customerIp': '127.0.0.1', 'merchantPosId': '145227', 'description': 'RTV market', 'currencyCode': 'PLN', 'totalAmount': '220', 'buyer': {'customerId': 'guest', 'email': 'grzesiek.supel@example.com', 'phone': '654111654', 'firstName': 'Grzesiek', 'lastName': 'Supel', 'language': 'pl'}, 'payMethod': {'amount': '220', 'type': 'PBL'}, 'status': 'COMPLETED', 'products': [{'name': 'Product 11', 'unitPrice': '110', 'quantity': '2'}]}
