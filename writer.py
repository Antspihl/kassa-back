"""Klass kassas toimuvate tehingute kirjutamiseks Google Sheetsi."""
import pandas as pd
import pygsheets

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
    if quantity < 0 or customer_name == "" or drink_name == "":
        return
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
