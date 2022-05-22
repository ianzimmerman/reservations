from secrets import choice
from unicodedata import name
from models import Restaurant, WalkIn, Table
from datetime import datetime


class CLI:
    def __init__(self, restaurant: Restaurant) -> None:
        self.restaurant = restaurant

    def get_action(self):

        actions = [
            {"name": "Check In Guest", "action": self.check_in},
            {"name": "Show Tables", "action": self.show_tables},
            {"name": "Show Waitlist", "action": self.show_wait_list},
            {"name": "Clear Table", "action": self.check_out},
        ]

        print("----")
        print("Chose an action:")
        for i, a in enumerate(actions):
            print(f"{i+1}: {a['name']}")
        print("----\n")

        action = input("Action:")
        actions[int(action) - 1].get("action")()

    def check_in(self):
        party_size = input("Party Size:")
        party_name = input("Name:")

        party = WalkIn(int(party_size), party_name)

        tables = self.restaurant.available_tables(party.party_size)
        if tables:
            table = self.restaurant.book_table(choice(tables).id, party)
            print(table)
        else:
            self.restaurant.add_waitlist(party)
            for table in self.restaurant.current_wait_times(party.party_size):
                print(table)

    def check_out(self):
        table_number = input("Table Number:")
        self.restaurant.clean_table(int(table_number))

    def book_reservation(self):
        raise NotImplementedError

    def show_tables(self):
        party_size = input("Party Size:")
        for t in self.restaurant.current_wait_times(int(party_size)):
            print(t)

    def show_wait_list(self):
        for party in self.restaurant.waitlist:
            print(party)
