"""Class to handle bills and send them out to the customers."""
from sheet_handler import get_drinks_and_prices, get_names, get_final_order_list


class BillHandler:
    """
    A class to represent a bill handler.
    """
    def __init__(self):
        self.drinks = get_drinks_and_prices()  # {"drink_name": price}
        self.names = get_names()  # ["name1", "name2"]
        self.all_orders = get_final_order_list()  # [("name", "drink", quantity)]

        self.people = self.create_people()  # {"name": Person}
        self.assign_bills()

    def get_bill(self, name: str) -> int:
        """
        Get a bill for a person.
        """
        return self.people[name].bill

    def assign_bills(self) -> None:
        """
        Go through orders and assign final bills to people.
        """
        for order in self.all_orders:
            name, drink, quantity = order
            self.people[name].drinks_with_quantity[drink] += quantity
            self.people[name].bill += float(self.drinks[drink] * quantity)

    def create_people(self) -> dict:
        """
        Create people objects.
        """
        people = {}
        for name in self.names:
            people[name] = Person(name, list(self.drinks.keys()))
        return people

    def get_summary(self) -> str:
        """
        Get a summary of the bills.
        """
        summary = "Arvete kokkuvõtte:\n"
        people = [person for person in self.people.values()].sort(key=lambda x: x.bill, reverse=True)
        for person in people:
            summary += f"{person.name}: {person.bill}€\n"
        return summary[:-1]

    def get_bill_list(self) -> list:
        """
        Get a list of bills.
        """
        bill_list = []
        for person in self.people.values():
            bill_list.append((person.name, person.bill))
        return [person for person in bill_list if person[1] > 0]

    def get_bill_details(self) -> list:
        """
        Get a list of people with their drinks.
        {"name": "name", "drinks": {"drink": quantity}}
        """
        bill_details = []
        for person in self.people.values():
            if person.bill > 0:
                drinks = {}
                for drink, quantity in person.drinks_with_quantity.items():
                    if quantity > 0:
                        drinks[drink] = quantity
                bill_details.append({person.name: drinks})
        return bill_details


class Person:
    """
    A class to represent a person.
    """
    def __init__(self, name: str, drinks: list):
        self.name = name
        self.drinks_with_quantity = dict()  # {"drink": quantity}
        for drink in drinks:
            self.drinks_with_quantity[drink] = 0
        self.bill = float(0)
