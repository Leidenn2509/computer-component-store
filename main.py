from flask import Flask, make_response, render_template, request
import json
from shop import app
#from shop.service import *


@app.route("/", methods=["POST", "GET"])
def main():
    if request.method == "POST":
        return make_response("OK")
    else:
        return render_template("MainPage.html", categories=json.dumps([{"id": "1", "name": "Category1"},
                                                                       {"id": "1.1", "name": "Category2"},
                                                                       {"id": "2", "name": "Category3"}]))


if __name__ == '__main__':
    app.run(debug=True)
