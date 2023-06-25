"""Klass kassas toimuvate tehingute kirjutamiseks Google Sheetsi."""
import pandas as pd
import pygsheets
import unicodedata

# authorization API key
gc = pygsheets.authorize(service_file="sheets_api.json")

df = pd.DataFrame()
df["timestamp"] = []
df["customer_name"] = []
df["drink_name"] = []
df["quantity"] = []


def log_transactions(customer_name: str, drink_name: str, quantity: int, has_record: bool):
    """
    Log all transactions, e.g. who ordered what and how many. Can be used for debugging
    """
    sh = gc.open("Soveldaja kassa")
    wks = sh[0]  # table name: "Tellimuste kokkuvõte"
    log = sh[1]  # table name: "Tellimuste logi"

    wks_existing_data = wks.get_all_records()
    log_existing_data = log.get_all_records()

    order_data = {
        "customer_name": customer_name,
        "drink_name": drink_name,
        "quantity": quantity
    }

    log_data = {
        "timestamp": pd.Timestamp.now(),
        "customer_name": customer_name,
        "drink_name": drink_name,
        "quantity": quantity
    }

    log_existing_data.append(log_data)
    wks_existing_data.append(order_data)
    log.set_dataframe(pd.DataFrame(log_existing_data), start="A1")

    if not has_record:
        wks.set_dataframe(pd.DataFrame(wks_existing_data), start="A1")


def add_order(customer_name: str, drink_name: str, quantity: int):
    """
    Add a drink to a customer's order. If the customer already has an order, add to the existing order.
    """
    has_record = False
    sh = gc.open("Soveldaja kassa")
    wks = sh[0]  # table name: main

    existing_data = wks.get_all_records()
    print(f"Existing data: {existing_data}")

    for row in existing_data:
        if row["customer_name"] == customer_name and row["drink_name"] == drink_name:
            has_record = True
            if pd.isna(row["quantity"]):
                row["quantity"] = 0
            row["quantity"] += quantity
            break

    log_transactions(customer_name, drink_name, quantity, has_record)

    wks.set_dataframe(pd.DataFrame(existing_data), start="A1")


def get_drinks() -> list:
    """
    Get all drinks from the Google sheet.
    """
    sh = gc.open("Soveldaja kassa")
    wks = sh[2]  # table name: "Joogid"
    existing_data = wks.get_all_records()
    return parse_drink_data(existing_data)


def get_drinks_and_prices() -> dict:
    """
    Get all drinks from the Google sheet.
    """
    sh = gc.open("Soveldaja kassa")
    wks = sh[2]  # table name: "Joogid"
    existing_data = wks.get_all_records()
    return parse_drink_and_price_data(existing_data)


def get_names() -> list[str]:
    """
    Get all customers from the Google sheet.
    """
    sh = gc.open("Soveldaja kassa")
    wks = sh[3]  # table name: "Nimed"
    existing_data = wks.get_all_records()
    print(f"Existing data: {existing_data}")
    return parse_name_data(existing_data).pop("names")


def get_final_order_list() -> list:
    """
    Get all orders from the Google sheet.
    """
    sh = gc.open("Soveldaja kassa")
    wks = sh[0]  # table name: "Tellimuste kokkuvõte"
    existing_data = wks.get_all_records()
    return parse_order_data(existing_data)


def parse_order_data(data: list) -> list:
    """
    [{"customer_name": "name", "drink_name": "drink", "quantity": quantity}] => [("name", "drink", quantity)]
    """
    parsed_data = []
    for item in data:
        parsed_data.append((item["customer_name"], item["drink_name"], item["quantity"]))
    return parsed_data


def parse_drink_data(data: list) -> list:
    """
    Parse data from Google Sheets to a dict.
    """
    parsed_data = []
    for item in data:
        parsed_data.append(item["drink_name"])
    # Replace non-ascii characters
    parsed_data = [unicodedata.normalize('NFKD', i).encode('ascii', 'ignore').decode('utf-8') for i in parsed_data]
    return parsed_data


def parse_name_data(data: list) -> dict:
    """
    Parse data from Google Sheets to a dict.
    """
    parsed_data = {"names": []}
    for item in data:
        parsed_data["names"].append(item["name"])
    # Replace non-ascii characters
    parsed_data["names"] = [unicodedata.normalize('NFKD', i).encode('ascii', 'ignore').decode('utf-8') for i in parsed_data["names"]]
    return parsed_data


def parse_drink_and_price_data(data: list) -> dict:
    """
    [{'drink_name': 'Aperol Spritz', 'price': 5}, {'drink_name': 'Limoncello Spritz', 'price': 5}] =>
    {'Aperol Spritz': 5, 'Limoncello Spritz': 5'}
    """
    parsed_data = {}
    for item in data:
        parsed_data[item["drink_name"]] = item["price"]
    # Replace non-ascii characters
    parsed_data = {unicodedata.normalize('NFKD', k).encode('ascii', 'ignore').decode('utf-8'): v for k, v in parsed_data.items()}
    return parsed_data
