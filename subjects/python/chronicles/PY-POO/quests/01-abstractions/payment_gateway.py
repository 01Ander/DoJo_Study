from abc import ABC, abstractmethod


class PaymentProcessor(ABC):

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


class CreditCardProcessor(PaymentProcessor):

    def process_payment(self, amount: float) -> bool:
        print(f"Processing Credit Card by ${amount}")
        return True


class PaypalProcessor(PaymentProcessor):

    def process_payment(self, amount: float) -> bool:
        print(f"Redirecting to PayPal by ${amount}")
        return True


# class BitcoinProcessor(PaymentProcessor):
#     pass


if __name__ == "__main__":
    my_credit_payment = CreditCardProcessor()
    my_credit_payment.process_payment(265.87)
    paypal_payment = PaypalProcessor()
    paypal_payment.process_payment(1730)
    # btc = BitcoinProcessor()
