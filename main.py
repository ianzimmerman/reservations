from models import WalkIn, Reservation, Table, Restaurant
from random import choice
from ui.cli import CLI

RANDOM_TABLES = [
    (i + 1, seats) for i, seats in enumerate([choice([2, 4, 6]) for _ in range(10)])
]


if __name__ == "__main__":
    tables = [Table(*t) for t in RANDOM_TABLES]
    r = Restaurant("Ian's Place", tables)
    i = CLI(r)

    while True:
        i.get_action()
