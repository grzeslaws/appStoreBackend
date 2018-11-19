from store_api import app
import os


def image_folder_path(product_uuid):
    return app.config["UPLOAD_FOLDER"] + "/" + product_uuid


def image_path_with_options(file_name, image_size):
    f_name, ext = os.path.splitext(file_name)
    return f_name + "-" + image_size + ext
