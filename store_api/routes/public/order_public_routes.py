from store_api import app, db, generate_uuid, settings
from store_api.models import Order, Orderitem, Product, Customer
from store_api.serializers import product_item_in_order, product_item_for_order_payu, customer_item
from flask import jsonify, request
import urllib.parse
import urllib.request
import certifi
import json
import os

import requests


@app.route("/api/public/create_order", methods=["POST"])
def create_order():

    if request.method == "POST":
        customerPayloads = request.json["customerPayloads"]
        customer = Customer(
            customer_uuid=generate_uuid(),
            first_name=customerPayloads["firstName"],
            last_name=customerPayloads["lastName"],
            email=customerPayloads["email"],
            street=customerPayloads["street"],
            city=customerPayloads["city"],
            zip_code=customerPayloads["zipCode"],
            telephone=customerPayloads["telephone"]
        )

        order = Order(total_price=request.json["totalPrice"], customer=customer)

        for oi in request.json["orderItems"]:
            p = Product.query.filter_by(product_uuid=oi["product"]["productUuid"]).first()
            order_item = Orderitem(order=order, product=p, quantity=oi["quantity"])
            db.session.add(order_item)

        db.session.add(order)
        db.session.add(customer)
        db.session.commit()

    return jsonify({"orderUuid": order.order_uuid, "customer": customer_item(customer)}), 200


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

    request_host_url = request.host_url
    data = urllib.parse.urlencode({
        "grant_type": os.environ["CLIENT_CREDENTIALS"],
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"]
    })
    data = data.encode("ascii")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    req = urllib.request.Request(settings.PAYU_AUTHORIZE_ENDPOINT, data, headers)

    with urllib.request.urlopen(req, cafile=certifi.where()) as response:

        return send_order(response.read(), order_uuid, request_host_url)


def send_order(access_token, order_uuid, request_host_url):
    at = json.loads(access_token)["access_token"]
    order = Order.query.filter_by(order_uuid=order_uuid).first()

    customer = order.customer.__dict__

    order_payload = {}
    order_payload["buyer"] = {}
    order_items = []

    for oi in order.orderitems:
        p = Product.query.filter_by(id=oi.product_id).first()
        order_items.append(product_item_for_order_payu(p, oi.quantity))

    order_payload["notifyUrl"] = request_host_url + settings.APP_NOTIFICATIONS_ENDPOINT
    order_payload["customerIp"] = settings.PAYU_CUSTOMER_IP
    order_payload["merchantPosId"] = settings.PAYU_MERCHANT_POS_ID
    order_payload["description"] = settings.PAYU_DESCRIPTION
    order_payload["currencyCode"] = settings.PAYU_CURRENCY_CODE
    order_payload["totalAmount"] = order.__dict__["total_price"]
    order_payload["extOrderId"] = order.__dict__["order_uuid"]
    order_payload["buyer"]["email"] = customer["email"]
    order_payload["buyer"]["phone"] = customer["telephone"]
    order_payload["buyer"]["firstName"] = customer["first_name"]
    order_payload["buyer"]["lastName"] = customer["last_name"]
    order_payload["buyer"]["language"] = settings.PAYU_BUYER_LANGUAGE
    order_payload["products"] = order_items

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + at,
        "Cache-Control": "no-cache"
    }

    response = requests.request("POST", settings.PAYU_ORDERS_ENDPOINT, data=json.dumps(order_payload),
                                headers=headers, allow_redirects=False)

    return jsonify({"linkToPayment": response.json()["redirectUri"]})


@app.route("/notify", methods=["POST"])
def notify():
    if request.method == "POST":
        requestOrder = request.json["order"]

        order = Order.query.filter_by(order_uuid=requestOrder["extOrderId"]).first()
        order.status = requestOrder["status"]
        order.order_pauy_uuid = requestOrder["orderId"]

        db.session.add(order)
        db.session.commit()

        return jsonify({"status": requestOrder})
