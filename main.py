from flask import Flask, make_response, render_template, request
import json
from shop import app
from shop.service import *


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))

        if data["action"] == "sendProducts":
            products = get_products(data["category"])
            return make_response(json.dumps({"action": "setProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendFilterValues":
            values = get_filter_values(data["category"])
            return make_response(json.dumps({"action": "setFilterValues", "values": values}), 200,
                                 {"content_type": "application/json"})
        elif data["action"] == "sendFilteredProducts":
            products = get_filtered_products(data)
            return make_response(json.dumps({"action": "setFilteredProducts", "products": products}), 200,
                                 {"content_type": "application/json"})
    else:
        shop_info = get_shop_info()
        categories = get_categories()
        return render_template('MainPage.html', categories=json.dumps(categories), shop_info=json.dumps(shop_info))


@app.route('/admin', methods=["POST", "GET"])
def admin():
    if request.method == 'POST':
        data = json.loads(request.data.decode('utf-8').replace('\0', ''))
        if data["action"] == "addCategory":
            add_category(data)
            categories = get_categories()
            node_categories = get_node_categories()
            leaf_categories = get_leaf_categories()
            return make_response(json.dumps({"action": "setCategories", "node_categories": node_categories,
                                             "leaf_categories": leaf_categories, "categories": categories}), 200,
                                 {"content_type": "application/json"})
    else:
        shop_info = get_shop_info()
        categories = get_categories()
        node_categories = get_node_categories()
        leaf_categories = get_leaf_categories()
        products = get_all_products()
        return render_template('AdminPage.html',
                               categories=json.dumps(categories),
                               node_categories=json.dumps(node_categories),
                               leaf_categories=json.dumps(leaf_categories),
                               products=json.dumps(products),
                               shop_info=json.dumps(shop_info))


if __name__ == '__main__':
    app.run(debug=True)
