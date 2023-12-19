import pandas as pd
from matplotlib import pyplot as plt

import sheet_handler
from bill_handler import BillHandler

data = sheet_handler.get_all_logs()
data1 = sheet_handler.get_all_logs_filtered()
top7 = BillHandler().get_people().values()
top7 = sorted(top7, key=lambda x: x.bill, reverse=True)[:7]
print(top7)


def drink_amount_pie_chart():
    """
    Pie chart of drink amounts.
    """
    drink_quantity = data.groupby('drink_name')['quantity'].sum().reset_index()

    plt.figure(figsize=(8, 8))
    plt.pie(drink_quantity['quantity'], labels=drink_quantity['drink_name'], autopct='%1.1f%%')
    plt.title('Tellitud jookide protsentuaalne jaotus')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    plt.show()


def drink_popularity_by_amount():
    """
    Bar chart of drink popularity by hour.
    """
    drink_quantity = data.groupby('drink_name')['quantity'].sum().reset_index()
    drink_quantity = drink_quantity.sort_values(by='quantity', ascending=False)
    drink_quantity = drink_quantity.head(10)
    drink_quantity = drink_quantity.sort_values(by='quantity', ascending=True)

    plt.figure(figsize=(8, 8))
    plt.barh(drink_quantity['drink_name'], drink_quantity['quantity'])
    plt.title('Top 10 Drinks by Quantity')
    plt.tight_layout()
    plt.show()


def best_customers():
    """
    Bar chart of the best customers.
    """
    customer_orders = data.groupby('customer_name')['quantity'].sum().sort_values(ascending=False)

    top_5_customers = customer_orders.head(7).reset_index()

    print(top_5_customers)


if __name__ == '__main__':
    drink_amount_pie_chart()
    #drink_popularity_by_amount()
    # best_customers()

