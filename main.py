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

    else:
        categories = get_categories()
        return render_template('MainPage.html', categories=json.dumps(categories))


if __name__ == '__main__':
    app.run(debug=True)
