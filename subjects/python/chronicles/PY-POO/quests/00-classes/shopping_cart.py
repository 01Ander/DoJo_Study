
class cart:
    def __init__(self, customer_id: str) -> dict:
        self.customer_id = customer_id
        self.items = []
        self.total = 0.0

    def add_item(self, item_name: str, price: float) -> None:
        self.items.append(item_name)
        self.total += price


# new_cart = cart('tx1')
# new_cart.add_item('manzana', 20.0)
# print(new_cart.customer_id)
# print(new_cart.items)
# print(new_cart.total)
# print(new_cart)

if __name__ == "__main__":
    new_cart = cart("cust_12")
    new_cart.add_item('manzanas', 20.0)
    new_cart.add_item('jugo', 35.5)

    print(f"Cart total: ${new_cart.total}, for: {new_cart.items}")
