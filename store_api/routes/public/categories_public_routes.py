from store_api import app
from flask import jsonify
from store_api.models import Category


@app.route("/api/public/get_categories")
def get_categories():
    categories = Category.query.all()

    categoriesList = []
    for c in categories:
        categoriesObject = {}
        categoriesObject["id"] = c.id
        categoriesObject["name"] = c.name
        categoriesList.append(categoriesObject)

    return jsonify({"categories": categoriesList})
