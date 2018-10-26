from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from store_api import settings
import uuid
import os


def generate_uuid():
    return str(uuid.uuid4())


app = Flask(__name__, static_folder=settings.STATIC_FOLDER)
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]

db = SQLAlchemy(app)

from store_api.routes.public import product_public_routes  # noqa: E402, F401
from store_api.routes.public import categories_public_routes  # noqa: E402, F401
from store_api.routes.public import collections_public_routes  # noqa: E402, F401
from store_api.routes.public import order_public_routes  # noqa: E402, F401
from store_api.routes.public import home_routes  # noqa: E402, F401
from store_api.routes.public import login_routes  # noqa: E402, F401
from store_api.routes.public import payment_post_public_routes  # noqa: E402, F401

from store_api.routes.admin import product_admin_routes  # noqa: E402, F401
from store_api.routes.admin import order_routes  # noqa: E402, F401
from store_api.routes.admin import profile_routes  # noqa: E402, F401
from store_api.routes.admin import categories_admin_routes  # noqa: E402, F401
from store_api.routes.admin import collections_admin_routes  # noqa: E402, F401
from store_api.routes.admin import payment_post_admin_routes  # noqa: E402, F401
