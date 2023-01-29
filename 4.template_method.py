
from abc import ABC, abstractmethod

class Someday(ABC):
    
    @abstractmethod
    def morning(self):
        ...

    @abstractmethod
    def evening(self):
        ...

    def have_a_good_day(self):
        self.morning()
        self.evening()


class Sunny(Someday):
    
    def morning(self):
        print("Running")

    def evening(self):
        print("Baseketball")


class Rainy(Someday):
    def morning(self):
        print("Sleeping")

    def evening(self):
        print("Play video games.")


if __name__ == "__main__":
    days = [Sunny(), Rainy(), Sunny()]
    for i, day in enumerate(days):
        print(f"\nDay: {i + 1}\n{'-' * 20}")
        day.have_a_good_day()

    
