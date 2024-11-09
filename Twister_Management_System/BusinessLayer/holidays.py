class Holidays:
    def __init__(self, occasion: str, date: str) -> None:
        self.__occasion = occasion
        self.__date = date

    @property
    def date(self) -> str:
        return self.__date
    
    @property
    def occasion(self) -> str:
        return self.__occasion
    
    def __str__(self) -> str:
        return f"Holiday: {self.__occasion} on {self.__date}"
