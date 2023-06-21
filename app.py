"""Soveldaja kassa rakendus"""
from dataclasses import dataclass

from flask import Flask, request
from flask_cors import CORS, cross_origin

from sheet_handler import add_order, get_drinks, get_names

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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
    return "Tsauki-tsau, ma töötan"


@app.route("/order", methods=["POST"])
@cross_origin()
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


@app.route("/drinks", methods=["GET"])
@cross_origin()
def drinks():
    """
    Read drinks data from a Google sheet and return it as a json.
    """
    try:
        return get_drinks()
    except Exception as e:
        print(e)
        return e


@app.route("/names", methods=["GET"])
@cross_origin()
def names():
    """
    Read name data from a Google sheet and return it as a json.
    """
    try:
        return get_names()
    except Exception as e:
        print(e)
        return e


if __name__ == "__main__":
    app.run(debug=True)
