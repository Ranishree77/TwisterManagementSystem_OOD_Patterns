import sys
sys.path.append("../")

from BusinessLayer.twister_scheduler import Scheduler

class TwisterSchedulerApp:
    def __init__(self) -> None:
        self.__scheduler = Scheduler()

    def show_menu(self) -> None:
        while True:
            print("\nBalloon Twister Scheduler")
            print("1. Add Balloon Twister")
            print("2. Add Holiday")
            print("3. Make Reservation")
            print("4. Cancel Reservation")
            print("5. View Reservations")
            print("6. View Holidays")
            print("7. Exit")

            choice = int(input("Enter your choice: "))
            if choice == 1:
                name = input("Enter the name of the balloon twister: ").lower()
                availability = input("Enter availability dates (YYYY-MM-DD)(comma separated): ").split(',')
                self.__scheduler.add_balloon_twister(name, availability)

            elif choice == 2:
                occasion = input("Enter the occasion: ")
                date = input("Enter the date (YYYY-MM-DD): ")
                self.__scheduler.add_holiday(occasion, date)

            elif choice == 3:
                customer_name = input("Enter the customer's name: ")
                date = input("Enter the reservation date (YYYY-MM-DD): ")
                email = input("Enter the email id: ")
                result = self.__scheduler.make_reservation(customer_name, date, email)
                print(result)

            elif choice == 4:
                email = input("Enter the email id: ").lower()
                self.__scheduler.cancel_reservation(email)
        
            elif choice == 5:
                self.__scheduler.view_reservations()

            elif choice == 6:
                self.__scheduler.view_holidays()

            elif choice == 7:
                print("Exiting the program.")
                break

            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    app = TwisterSchedulerApp()
    app.show_menu()