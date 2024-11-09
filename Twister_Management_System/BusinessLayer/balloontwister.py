from typing import Optional
from BusinessLayer.reservations import Reservations

class BalloonTwister:
    def __init__(self, name: str, availability: Optional[list[str]] = None):
        self.__name = name
        self.__availability = availability if availability else []
        self.__assigned_reservations: list[Reservations] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def availability(self) -> list[str]:
        return self.__availability

    def add_availability(self, date: str) -> None:
        if date not in self.__availability:
            self.__availability.append(date)

    def assign_reservation(self, reservation: Reservations) -> None:
        self.__assigned_reservations.append(reservation)

    def remove_availability(self, date: str) -> None:
        if date in self.__availability:
            self.__availability.remove(date)

    def remove_reservation(self, reservation: Reservations) -> None:
        if reservation in self.__assigned_reservations:
            self.__assigned_reservations.remove(reservation)

    def __str__(self) -> str:
        return f"Balloon Twister: {self.__name}, Availability: {', '.join(self.__availability)}"