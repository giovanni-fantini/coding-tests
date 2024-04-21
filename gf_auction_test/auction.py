import logging
from base_instruction import BaseInstruction
from bid import Bid


class Auction(BaseInstruction):
    """A class to model SELL type instructions. Through the employment of an in-memory repository
    it stores the state of each auction - provided it passes validations - and mutates it upon closing.
    Auctions are validated as follows:
    - Validates the same item was not previously listed for sale

    Args:
        BaseInstruction (class): the parent class BaseInstruction, containing some of the behaviour shared between Auction and Bid

    Attributes:
        timestamp (int): a Unix-epoch time and is the auction start time
        user_id (int): user ID
        item (str): a unique string code for the item on sale
        reserve_price (float): a decimal representing the item reserve price in the site's local currency
        closing_time (int): a Unix-epoch time

    Methods:
        cls.find_by_item(item):
            Available through the parent class. Returns the auction matching the provided item
        cls.find_by_closing_time(time):
            Returns the auctions with a certain closing time
        save():
            Available through the parent class. Stores the auction in its in-memory repository, if validations are succesful
        close():
            Closes the auction, resolving winner, price_paid and status attributes
    """

    repository = []

    @classmethod
    def find_by_closing_time(cls, time):
        """Returns the auctions with a certain closing time

        Args:
            time (int): the closing time to filter for

        Returns:
            list: a list of the matching Auction objects
        """
        return [auction for auction in cls.repository if auction.closing_time == time]

    def __init__(self, timestamp, user_id, item, reserve_price, closing_time):
        super().__init__(timestamp, user_id, item)
        self.reserve_price = reserve_price
        self.closing_time = closing_time
        self.winner = ""
        self.price_paid = 0
        self.status = "UNSOLD"

    def close(self):
        """Closes the auction, resolving winner, price_paid and status attributes

        Returns:
            Auction: returns self
        """
        if self._total_bid_count() == 0:
            self._print_output()
            return self

        if self._total_bid_count() > 0:
            if self._highest_bid().bid_amount < self.reserve_price:
                self._print_output()
                return self

            second_highest_figure = max(
                self.reserve_price, self._runner_up_bid().bid_amount
            )
            self.price_paid = second_highest_figure
            self.status = "SOLD"
            self.winner = self._highest_bid().user_id
            self._print_output()
            return self

    def _validate(self):
        if Auction.find_by_item(self.item):
            logging.debug(f"Invalid auction {self}: item previously listed for sale")
            return False

        return True

    def _sorted_bids(self):
        return sorted(
            Bid.find_by_item(self.item), reverse=True, key=lambda bid: bid.bid_amount
        )

    def _total_bid_count(self):
        return len(self._sorted_bids())

    def _highest_bid(self):
        try:
            return self._sorted_bids()[0]
        except IndexError:
            return Bid()

    def _runner_up_bid(self):
        try:
            return self._sorted_bids()[1]
        except IndexError:
            return Bid()

    def _lowest_bid(self):
        try:
            return self._sorted_bids()[-1]
        except IndexError:
            return Bid()

    def _print_output(self):
        print(
            f"{self.closing_time}|{self.item}|{self.winner}|{self.status}|{self.price_paid:.2f}|{self._total_bid_count()}|{self._highest_bid().bid_amount:.2f}|{self._lowest_bid().bid_amount:.2f}"
        )
