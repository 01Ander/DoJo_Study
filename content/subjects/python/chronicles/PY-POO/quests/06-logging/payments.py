class ExpiredCardError(Exception):
    pass


class PaymentProcessor:
    def charge(self, card_year: int):
        if card_year < 2024:
            raise ExpiredCardError(f"Expired card")
        return True
