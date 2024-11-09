from typing import List, Dict, Optional
from datetime import datetime
import re
from BusinessLayer.balloontwister import BalloonTwister
from BusinessLayer.holidays import Holidays
from BusinessLayer.reservations import Reservations
from DataLayer.data_repository import DataRepository

class Scheduler:
    def __init__(self):
        self.__repository = DataRepository('twisters.csv', 'holidays.csv', 'reservations.csv')
        self.__balloon_twisters, self.__holidays, self.__reservations = self.__repository.read_data()
        self.__waiting_list: Dict[str, List[Reservations]] = self.__load_waiting_list()

    def __load_waiting_list(self) -> Dict[str, List[Reservations]]:
        waiting_list: Dict[str, List[Reservations]] = {}
        for reservation in self.__reservations:
            if reservation.status == 'Waiting':
                if reservation.date not in waiting_list:
                    waiting_list[reservation.date] = []
                waiting_list[reservation.date].append(reservation)
        return waiting_list
    
    def add_balloon_twister(self, name: str, availability: List[str]) -> None:
        existing_twister = next((twister for twister in self.__balloon_twisters if twister.name.lower() == name), None)

        if existing_twister:
            unique_availability = [date for date in availability if date not in existing_twister.availability]
            if unique_availability:
                existing_twister.availability.extend(unique_availability)
                print(f"Availability for Balloon Twister {name} updated successfully.")
            else:
                print(f"Balloon Twister {name} already has the provided availability dates.")
        else:
            twister = BalloonTwister(name, availability)
            self.__balloon_twisters.append(twister)
            print(f"Balloon Twister {name} added successfully.")

        self.save()

    def is_valid_date(self, date: str) -> bool:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
            return False
        
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    def add_holiday(self, occasion: str, date: str) -> None:
        if not self.is_valid_date(date):
            print(f"Invalid date format or date is in the past: {date}")
            return
    
        if any(holiday.date == date for holiday in self.__holidays):
            print(f"A holiday on {date} already exists. Cannot add another holiday on the same date.")
        else:
            holiday = Holidays(occasion, date)
            self.__holidays.append(holiday)
            self.save()
            print(f"Holiday '{occasion}' on {date} added successfully.")

    def make_reservation(self, customer_name: str, date: str, email: str) -> str:
        if not self.is_valid_date(date):
            return f"Invalid date format or date is in the past: {date}"
            
        if self.is_holiday(date):
            return "Reservations cannot be made on holidays."

        reservation = Reservations(customer_name, date, email)
        if date in self.__waiting_list and len(self.__waiting_list[date]) > 0:
            reservation.priority = len(self.__waiting_list[date]) + 1
            self.__waiting_list[date].append(reservation)
        else:
            self.assign_twister_to_reservation(reservation)

            if reservation.get_assigned_twister():
                reservation.status = 'Confirmed'
            else:
                reservation.status = 'Waiting'
                self.__waiting_list[date] = [reservation]

        self.__reservations.append(reservation)
        self.__update_waiting_list()
        self.save()
        return "Reservation added."

    def cancel_reservation(self, email: str) -> None:
        reservation = self.__find_reservation_by_email(email)
        if reservation is None:
            print(f"No reservation found for email: {email}")
            return

        reschedule = input(f"Would you like to reschedule your reservation for {reservation.customer_name}? (yes/no): ").strip().lower()
        
        if reschedule == 'yes':
            new_date = input("Please provide a new date for your reservation: ").strip()
            self.__cancel_functions(reservation)
            self.make_reservation(reservation.customer_name, new_date, email)
            print(f"Reservation for {email} rescheduled to {new_date} successfully.")
        else:
            self.__cancel_functions(reservation)
            print(f"Reservation for {email} cancelled successfully.")

        self.save()

    def __cancel_functions(self, reservation: Reservations):
        self.__update_twister_availability(reservation)
        self.__update_cancellation(reservation.date)
            
        self.__remove_from_waiting_list(reservation)
        self.__reservations.remove(reservation)
        self.__update_waiting_list()

    def __update_cancellation(self, date: str) -> None:
        if date in self.__waiting_list and self.__waiting_list[date]:
            next_waiting = self.__waiting_list[date][0]
            self.assign_twister_to_reservation(next_waiting)
            if next_waiting.get_assigned_twister():
                next_waiting.status = 'Confirmed'
                next_waiting.priority = None
                self.__remove_from_waiting_list(next_waiting)
            self.__update_waiting_list()

    def assign_twister_to_reservation(self, reservation: Reservations) -> None:
        for twister in self.__balloon_twisters:
            if reservation.date in twister.availability:
                reservation.assign_twister(twister.name)
                reservation.status = 'Confirmed'
                reservation.priority = None
                twister.assign_reservation(reservation)
                twister.remove_availability(reservation.date)
                return
        reservation.status = 'Waiting'
        
    def is_holiday(self, date: str) -> bool:
        return any(holiday.date == date for holiday in self.__holidays)
    
    def __find_reservation_by_email(self, email: str) -> Optional[Reservations]:
        return next((r for r in self.__reservations if r.email.lower() == email), None)

    def __update_waiting_list(self) -> None:
        for date, reservation_list in self.__waiting_list.items():
            for i, reservation in enumerate(reservation_list):
                reservation.priority = i + 1

    def __remove_from_waiting_list(self, reservation: Reservations) -> None:
        if reservation.date in self.__waiting_list:
            self.__waiting_list[reservation.date] = [r for r in self.__waiting_list[reservation.date] if r != reservation]
            if not self.__waiting_list[reservation.date]:
                del self.__waiting_list[reservation.date]

    def __update_twister_availability(self, reservation: Reservations) -> None:
        assigned_twister_name = reservation.get_assigned_twister()
        if assigned_twister_name:
            for twister in self.__balloon_twisters:
                if twister.name == assigned_twister_name:
                    twister.add_availability(reservation.date)
                    twister.remove_reservation(reservation)
                    self.__update_waiting_list()
                    break

    def view_reservations(self) -> None:
        if self.__reservations:
            for reservation in self.__reservations:
                if reservation.status == 'Confirmed':
                    print(reservation)
        else:
            print("No reservations found!")

    def view_holidays(self) -> None:
        if self.__holidays:
            for holiday in self.__holidays:
                print(holiday)
        else:
            print("No holidays found!")

    def save(self):
        self.__repository.write_data(self.__balloon_twisters, self.__holidays, self.__reservations)