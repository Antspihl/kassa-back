"""Class to handle bills and send them out to the customers."""
from sheet_handler import get_drinks_and_prices, get_final_order_list, get_names_and_emails


class BillHandler:
    """
    A class to represent a bill handler.
    """
    def __init__(self):
        self.drinks = get_drinks_and_prices()  # {"drink_name": price}
        self.names_with_emails = get_names_and_emails()  # ["name1", "name2"]
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
        for person in self.names_with_emails:
            name, email = person
            people[name] = Person(name, list(self.drinks.keys()), email)
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
            if person.bill > 0:
                a = {"name": person.name, "bill": f"{person.bill}€"}
                bill_list.append(a)
        return bill_list

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

    def get_person_details_by_name(self, name: str) -> dict:
        """Enter a person's name and get their info as dict
        {
            "name": "name",
            "drinks": {"drink": quantity}
            "bill": float
        }
        """
        person = self.people[name]
        drinks = {}
        for drink, quantity in person.drinks_with_quantity.items():
            if quantity > 0:
                drinks[drink] = quantity
        return {"name": person.name, "drinks": drinks, "bill": person.bill}

    def get_people(self) -> dict:
        """Get a list of people."""
        return self.people

    def get_sum_of_bills(self) -> float:
        """Get the sum of all bills."""
        return sum([person.bill for person in self.people.values()])


class Person:
    """
    A class to represent a person.
    """
    def __init__(self, name: str, drinks: list, email: str):
        self.name = name
        self.drinks_with_quantity = dict()  # {"drink": quantity}
        self.email = email
        for drink in drinks:
            self.drinks_with_quantity[drink] = 0
        self.bill = float(0)

    def __repr__(self):
        return f"{self.name}[{self.email}]: {self.bill}€"


if __name__ == "__main__":
    print(BillHandler().get_sum_of_bills())
    print(BillHandler().get_bill_list())
