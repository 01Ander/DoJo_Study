class Thermostat:
    def __init__(self):
        self.temperature = 20.0

    def increase(self, amount: float):
        self.temperature += amount
        if self.temperature > 30.0:
            self.temperature = 30.0  # Maximum cap
