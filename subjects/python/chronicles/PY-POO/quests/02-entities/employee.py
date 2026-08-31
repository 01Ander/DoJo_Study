from abc import ABC, abstractmethod


class Employer(ABC):
    def __init__(self, name: str, salary: int):
        self.name = name
        self.salary = salary

    @abstractmethod
    def calculate_bonus(self) -> float:
        pass


class Developer(Employer):
    def calculate_bonus(self) -> float:
        return self.salary * 0.1


class Manager(Employer):
    def calculate_bonus(self) -> float:
        return self.salary * 0.2


if __name__ == "__main__":
    dev = Developer("Ana", 1000)
    manager = Manager("Bob", 1000)
    print(dev.calculate_bonus())
    print(manager.calculate_bonus())
