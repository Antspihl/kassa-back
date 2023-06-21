"""Soveldaja kassa rakendus"""
from dataclasses import dataclass

from flask import Flask, request

from writer import add_order

app = Flask(__name__)


@dataclass
class Order:
    customer_name: str
    drink_name: str
    quantity: int


@app.route("/")
def front_page():
    """
    Front page of the app.
    """
    return "Hello, I am working!"


@app.route("/order", methods=["POST"])
def order():
    """
    Read in an order and add to the Google sheet.
    """
    try:
        data = Order(request.json["customer_name"], request.json["drink_name"], request.json["quantity"])
        add_order(data.customer_name, data.drink_name, data.quantity)
        print(f"Order from request: {data}")
        return "ok"
    except Exception as e:
        print(e)
        return e


@app.route("/data", methods=["GET"])
def data():
    """
    Read data from a Google sheet and return it as a json.
    :return:
    """
    #  Todo: read data from a Google sheet and return it as a json


if __name__ == "__main__":
    app.run(debug=True)
