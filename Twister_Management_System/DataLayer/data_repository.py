import csv
from BusinessLayer.balloontwister import BalloonTwister
from BusinessLayer.holidays import Holidays
from BusinessLayer.reservations import Reservations

path = "../DataLayer/"

class DataRepository:
    def __init__(self, twister_file: str, holiday_file: str, reservation_file: str) -> None:
        self.__twister_file = path + twister_file
        self.__holiday_file = path + holiday_file
        self.__reservation_file = path + reservation_file

    def read_data(self) -> tuple[list[BalloonTwister], list[Holidays], list[Reservations]]:
        twisters: list[BalloonTwister] = []
        holidays: list[Holidays] = []
        reservations: list[Reservations] = []

        with open(self.__twister_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                name, availability = row
                twister = BalloonTwister(name, availability.split('|'))
                twisters.append(twister)

        with open(self.__holiday_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                occasion, date = row
                holiday = Holidays(occasion, date)
                holidays.append(holiday)

        with open(self.__reservation_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                reservation = Reservations(
                    customer_name = row['customer_name'],
                    date = row['reservation_date'],
                    email = row['email']
                )
                reservation.assign_twister(row['assigned_twister']) if row['assigned_twister'] else None
                reservation.status = row['status']
                reservation.priority = int(row['priority']) if row['priority'] and row['priority'] != 'None' else None
                reservations.append(reservation)

        return twisters, holidays, reservations

    def write_data(self, twisters: list[BalloonTwister], holidays: list[Holidays], reservations: list[Reservations]):
  
        with open(self.__twister_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'availability'])
            for twister in twisters:
                availability = '|'.join(twister.availability)
                writer.writerow([twister.name, availability])

        with open(self.__holiday_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['occasion', 'date'])
            for holiday in holidays:
                writer.writerow([holiday.occasion, holiday.date])

        with open(self.__reservation_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['customer_name', 'reservation_date', 'email', 'assigned_twister', 'status', 'priority'])
            for reservation in reservations:
                writer.writerow([
                    reservation.customer_name,
                    reservation.date,
                    reservation.email,
                    reservation.get_assigned_twister() if reservation.assign_twister is not None else '',
                    reservation.status,
                    reservation.priority if reservation.priority is not None else ''
                ])