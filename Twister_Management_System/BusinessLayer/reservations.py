from typing import Optional

class Reservations:
    def __init__(self, customer_name: str, date: str, email: str) -> None:
        self.__customer_name = customer_name
        self.__date = date
        self.__email = email
        self.__assigned_twister: Optional[str] = None
        self.__status = 'Waiting'
        self.__priority: Optional[int] = None

    def assign_twister(self, twister: Optional[str]) -> None:
        self.__assigned_twister = twister if twister else None
        self.__status = 'Confirmed' if twister else 'Waiting'

    @property
    def priority(self) -> Optional[int]:
        return self.__priority

    @priority.setter
    def priority(self, priority: Optional[int]) -> None:
        self.__priority = priority

    @property
    def customer_name(self) -> str:
        return self.__customer_name
    
    @property
    def email(self) -> str:
        return self.__email

    @property
    def date(self) -> str:
        return self.__date
    
    @date.setter
    def date(self, new_date: str) -> None:
        self.__date = new_date

    def get_assigned_twister(self) -> Optional[str]:
        return self.__assigned_twister

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, status: str) -> None:
        self.__status = status

    def __str__(self) -> str:
        return (f"Reservation for {self.__customer_name} on {self.__date}, "
                f"Status: {self.__status}, Assigned Twister: {self.__assigned_twister}")