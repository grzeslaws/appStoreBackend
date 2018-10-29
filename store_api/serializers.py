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
    product_item["description"] = p.description
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


def product_item_for_order_payu(p, q):
    product_item = {}
    product_item["name"] = p.name
    product_item["unitPrice"] = p.price
    product_item["quantity"] = q
    return product_item


def customer_item(c):
    customer = {}
    customer["first_name"] = c.first_name
    customer["last_name"] = c.last_name
    customer["email"] = c.email
    customer["street"] = c.street
    customer["city"] = c.city
    customer["zip_code"] = c.zip_code
    customer["telephone"] = c.telephone
    customer["customer_uuid"] = c.customer_uuid
    return customer


def payment_post_type_item(i):
    type_item = {}
    type_item["id"] = i.id
    type_item["name"] = i.name
    type_item["cost"] = i.cost
    return type_item
