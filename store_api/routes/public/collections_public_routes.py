from store_api import app
from flask import jsonify
from store_api.models import Collection


@app.route("/api/public/get_collections")
def get_collections():
    collections = Collection.query.all()

    collectionsList = []
    for c in collections:
        collectionsObject = {}
        collectionsObject["id"] = c.id
        collectionsObject["name"] = c.name
        collectionsList.append(collectionsObject)

    return jsonify({"collections": collectionsList})
