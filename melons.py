"""Classes for melon orders."""

from random import randint

import datetime


class AbstractMelonOrder(object):
    """An abstract base class that other Melon Orders inherit from."""

    def __init__(self, species, qty, order_type, tax):

        if qty > 100:
            raise TooManyMelonsError
        self.species = species
        self.qty = qty
        self.mark_shipped = False
        self.order_type = order_type
        self.tax = tax

    def is_rush_hour(self, today):
        if today.weekday() < 5:
            return today.hour >= 8 and today.hour <= 11

    def get_base_price(self):
        """Picks a random integer between 5-9 as base price"""

        base_price = randint(5, 10)
        today = datetime.datetime.today()
        if self.is_rush_hour(today):
            base_price += 4

        return base_price

    def get_total(self):
        """Calculate price, including tax."""

        base_price = self.get_base_price()

        if self.species == 'Christmas':
            base_price *= 1.5

        total = (1 + self.tax) * self.qty * base_price

        return total

    def mark_shipped(self):
        """Record the fact than an order has been shipped."""

        self.shipped = True


class DomesticMelonOrder(AbstractMelonOrder):
    """A melon order within the USA."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        super(DomesticMelonOrder, self).__init__(species, qty,
                                                 order_type="domestic", tax=.08)


class InternationalMelonOrder(AbstractMelonOrder):
    """An international (non-US) melon order."""

    def __init__(self, species, qty, country_code):
        """Initialize melon order attributes."""

        super(InternationalMelonOrder, self).__init__(species, qty, order_type="international", tax=.17)

        self.country_code = country_code

    def get_country_code(self):
        """Return the country code."""

        return self.country_code

    def get_total(self):
        """Adds a flat fee of $3 to orders with less than 10 melons."""

        total = super(InternationalMelonOrder, self).get_total()

        if self.qty < 10:
            total += 3

        return total


class GovernmentMelonOrder(AbstractMelonOrder):
    """A melon order from the Government."""

    def __init__(self, species, qty):
        """Initialize melon order attributes."""

        super(GovernmentMelonOrder, self).__init__(species, qty,
                                                   order_type="Government", tax=0)

        self.passed_inspection = False

    def mark_inspection(self, passed):
        """Record the fact that an order has passed inspection"""

        if passed:

            self.passed_inspection = True


class TooManyMelonsError(ValueError):
    """Raises error if order qty > 100"""
    def __init__(self):
        super(TooManyMelonsError, self).__init__("No more than 100 melons!")
