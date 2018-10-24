from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid


def generate_uuid():
    return str(uuid.uuid4())


STATIC_FOLDER = "/static"
UPLOAD_FOLDER = "store_api" + STATIC_FOLDER + "/images"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])
PYTHONHTTPSVERIFY = 0

app = Flask(__name__, static_folder=STATIC_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = "thissecretkey"

db = SQLAlchemy(app)

from store_api.routes.public import product_public_routes  # noqa: E402, F401
from store_api.routes.public import categories_public_routes  # noqa: E402, F401
from store_api.routes.public import collections_public_routes  # noqa: E402, F401
from store_api.routes.public import order_public_routes  # noqa: E402, F401
from store_api.routes.public import home_routes  # noqa: E402, F401
from store_api.routes.public import login_routes  # noqa: E402, F401

from store_api.routes.admin import product_admin_routes  # noqa: E402, F401
from store_api.routes.admin import order_routes  # noqa: E402, F401
from store_api.routes.admin import profile_routes  # noqa: E402, F401
from store_api.routes.admin import categories_admin_routes  # noqa: E402, F401
from store_api.routes.admin import collections_admin_routes  # noqa: E402, F401
