"""Soveldaja kassa rakendus"""
from dataclasses import dataclass

from flask import Flask, request
from flask_cors import CORS, cross_origin

from bill_handler import BillHandler
from sheet_handler import add_order, get_drinks, get_names, get_names_and_emails, get_last_20_orders

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@dataclass
class Order:
    """
    Dataclass for an order.
    """
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
@cross_origin(send_wildcard=True, origins='*')
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
        print("==", e)
        return e


@app.route("/orders", methods=["GET"])
@cross_origin(send_wildcard=True)
def get_last_orders():
    """
    Return 20 last orders that were sent from the app.
    """
    try:
        return get_last_20_orders()
    except Exception as e:
        print("==", e)
        return e


@app.route("/drinks", methods=["GET"])
@cross_origin(send_wildcard=True)
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
@cross_origin(send_wildcard=True)
def names():
    """
    Read name data from a Google sheet and return it as a json.
    """
    try:
        return get_names()
    except Exception as e:
        print(e)
        return e


@app.route("/bills", methods=["GET"])
@cross_origin(send_wildcard=True)
def bills():
    """
    Read name data from a Google sheet and return it as a json.
    """
    bill_handler = BillHandler()
    try:
        return bill_handler.get_bill_list()
    except Exception as e:
        print(e)
        return e


@app.route("/billDetails", methods=["GET"])
@cross_origin(send_wildcard=True)
def bill_details():
    """
    Read name data from a Google sheet and return it as a json.
    """
    bill_handler = BillHandler()
    try:
        return bill_handler.get_bill_details()
    except Exception as e:
        print(e)
        return e


@app.route("/emails", methods=["GET"])
@cross_origin(send_wildcard=True)
def names_and_emails():
    """
    Read name data from a Google sheet and return it as a json.
    """
    try:
        return get_names_and_emails()
    except Exception as e:
        print(e)
        return e


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
