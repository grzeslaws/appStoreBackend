def product_item(p):

    categoryList = []
    for cat in p.categories:
        category = {}
        category["id"] = cat.id
        category["name"] = cat.name
        categoryList.append(category)
    
    collectionsList = []
    for col in p.collections:
        collection = {}
        collection["id"] = col.id
        collection["name"] = col.name
        collectionsList.append(collection)

    product_item = {}
    product_item["id"] = p.id
    product_item["name"] = p.name
    product_item["image_path"] = p.image_path
    product_item["product_uuid"] = p.product_uuid
    product_item["price"] = p.price
    product_item["quantity"] = p.quantity
    product_item["categories"] = categoryList
    product_item["collections"] = collectionsList

    return product_item


def product_item_in_order(p):

    product_item = {}
    product_item["id"] = p.id
    product_item["name"] = p.name
    product_item["image_path"] = p.image_path
    product_item["product_uuid"] = p.product_uuid
    product_item["price"] = p.price

    return product_item
