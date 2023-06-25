"""Class to handle bills and send them out to the customers."""
from sheet_handler import get_drinks_and_prices, get_names, get_final_order_list


class BillHandler:
    """
    A class to represent a bill handler.
    """
    def __init__(self):
        self.drinks = get_drinks_and_prices()  # {"drink_name": price}
        self.names = get_names()  # ["name1", "name2"]
        self.orders = get_final_order_list()  # [("name", "drink", quantity)]

        self.people = self.create_people()
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
        for order in self.orders:
            name, drink, quantity = order
            self.people[name].drinks[drink] += quantity
            self.people[name].bill += float(self.drinks[drink] * quantity)

    def create_people(self) -> dict:
        """
        Create people objects.
        """
        people = {}
        for name in self.names:
            people[name] = Person(name, [self.drinks.keys()])
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


class Person:
    """
    A class to represent a person.
    """
    def __init__(self, name: str, drinks: list):
        self.name = name
        self.drinks = dict()
        for drink in drinks:
            self.drinks[drink] = 0
        self.bill = float(0)


