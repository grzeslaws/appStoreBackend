from store_api import app
from flask import jsonify
from store_api.models import PaymentType, PostType
from store_api.serializers import payment_post_type_item


@app.route("/api/public/get_post_payment_types", methods=["GET"])
def get_post_types():
    get_post_types = PostType.query.all()
    get_payment_types = PaymentType.query.all()
    return jsonify({
        "post_types": [payment_post_type_item(pt) for pt in get_post_types],
        "payment_types": [payment_post_type_item(pt) for pt in get_payment_types],
    })
