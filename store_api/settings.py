FLASK_DEBUG = True
PORT = 5000

STATIC_FOLDER = "/static"
UPLOAD_FOLDER = "store_api" + STATIC_FOLDER + "/images"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])
PYTHONHTTPSVERIFY = 0

# payu setting
PAYU_CUSTOMER_IP = "127.0.0.1"
PAYU_MERCHANT_POS_ID = "145227"
PAYU_DESCRIPTION = "App store"
PAYU_CURRENCY_CODE = "PLN"
PAYU_BUYER_LANGUAGE = "pl"

# payu apis
PAYU_AUTHORIZE_ENDPOINT = "https://secure.payu.com/pl/standard/user/oauth/authorize"
PAYU_ORDERS_ENDPOINT = "https://secure.payu.com/api/v2_1/orders/"

APP_NOTIFICATIONS_ENDPOINT = "notify"

