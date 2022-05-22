from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
from secrets import token_urlsafe

AVG_OCCUPATION_TIMES = {
    2: timedelta(minutes=30),
    4: timedelta(minutes=45),
    6: timedelta(minutes=60),
}


def _now() -> datetime:
    return datetime.now()


@dataclass
class WalkIn:
    party_size: int
    name: str

    id: str = token_urlsafe(3)
    check_in_time: datetime = _now()

    @property
    def current_wait_time(self):
        return datetime.now() - self.check_in_time

    def __repr__(self) -> str:
        return f"{self.name} (Party of {self.party_size}): {self.current_wait_time} wait time."


@dataclass
class Reservation:
    name: str
    party_size: int
    reservation_time: datetime
    id: str = token_urlsafe(3)

    @property
    def past_due(self):
        return datetime.now() > self.reservation_time


@dataclass
class Table:
    id: int
    seats: int
    occupied: bool = False
    occupied_at: datetime = None
    occupied_by: Reservation | WalkIn = None

    reservations: List[Reservation] = None

    @property
    def occupied_for(self) -> timedelta:
        """return timedelta since occupied"""
        if self.occupied:
            return datetime.now() - self.occupied_at

        return 0

    def estimated_time_free(
        self, avg_occupation_times: dict[int, timedelta] = AVG_OCCUPATION_TIMES
    ) -> datetime:
        seat_time = avg_occupation_times[self.seats]
        return self.occupied_at + seat_time

    def book(self, party: WalkIn | Reservation):
        self.occupied = True
        self.occupied_at = datetime.now()
        self.occupied_by = party

    def clean(self):
        self.occupied = False
        self.occupied_at = None
        self.occupied_by = None

    def is_available_at(
        self,
        time: datetime,
        avg_occupation_times: dict[int, timedelta] = AVG_OCCUPATION_TIMES,
    ) -> bool:
        """check if occupied or reserved at time"""
        seat_time = avg_occupation_times[self.seats]

        if self.occupied:
            return time > (self.occupied_at + seat_time)
        elif self.reservations:
            return any(
                [
                    (r.reservation_time < time)
                    and (time < (r.reservation_time + seat_time))
                    for r in self.reservations
                ]
            )
        else:
            return True

    def __repr__(self) -> str:
        return f"Table {self.id} ({self.seats} Top); Available: {self.estimated_time_free() - datetime.now() if self.occupied else 'Now'}"


class Restaurant:
    def __init__(self, name: str, tables: list[Table]) -> None:
        self.name = name
        self.tables = tables
        self.waitlist: list[WalkIn] = []

    def available_tables(self, party_size: int) -> list[Table]:
        return [
            t
            for t in self.tables
            if t.is_available_at(datetime.now())
            and party_size <= t.seats
            and t.seats - party_size < 2
        ]

    def add_waitlist(self, party: WalkIn) -> None:
        self.waitlist.append(party)

    def book_table(self, table_number: int, party: WalkIn | Reservation) -> Table:
        self.tables[table_number - 1].book(party)
        return self.tables[table_number - 1]

    def clean_table(self, table_number: int) -> None:
        self.tables[table_number - 1].clean()

    def current_wait_times(self, party_size: int) -> list[Table]:
        return [
            t for t in self.tables if party_size <= t.seats and t.seats - party_size < 2
        ]
