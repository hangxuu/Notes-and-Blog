from collections import namedtuple

Customer = namedtuple('Customer', 'name level')
promos = []


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

        self.total = self.price * self.quantity


class Order:

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'


def promotion(promo_func):
    promos.append(promo_func)
    return promo_func


@promotion
def promo_99_for_4(order):
    discount = 0
    items = order.cart
    items.sort(key=lambda a: a.price, reverse=True)
    i, total = 0, 0
    for item in items:
        if item.quantity >= 4 - i:
            total += (4 - i) * item.price
            break
        else:
            i += item.quantity
            total += item.total
    discount += total - 99
    return discount


@promotion
def promo_great_than_2(order):
    discount = 0
    nums = sum(item.quantity for item in order.cart)
    if nums >= 2:
        discount += order.total() * .1
    return discount


@promotion
def promo_great_than_3(order):
    discount = 0
    nums = sum(item.quantity for item in order.cart)
    if nums >= 3:
        discount += order.total() * .2
    return discount


def best_promo(order):
    return max(promo(order) for promo in promos)


if __name__ == "__main__":
    joe = Customer('John Doe', 'plus')
    ann = Customer('Ann Smith', 'normal')
    cart = [
        LineItem('百香果', 3, 39),
        LineItem('大台芒', 2, 29),
    ]
    print(Order(joe, cart, promo_99_for_4))
    # total: 175, due: 128.00
    print(Order(joe, cart, promo_great_than_2))
    # total: 175, due: 157.50
    print(Order(joe, cart, promo_great_than_3))
    # total: 175, due: 140.00
    print(Order(joe, cart, best_promo))
    # total: 175, due: 128.00 -- best promotion
