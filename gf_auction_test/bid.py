import logging
from base_instruction import BaseInstruction


class Bid(BaseInstruction):
    """A class to model BID type instructions. Through the employment of an in-memory repository
    it stores the state of each bid, provided it passes validations. Bids are validated as follows:
    - Validates item is on sale (e.g. there is an auction object with matching item)
    - Validates the bid is placed before the corresponding auction closes
    - Validates a user cannot bid on its own auction
    - Validates the bid is higher than any bids previously submitted by the same user

    Args:
        BaseInstruction (class): the parent class BaseInstruction, containing some of the behaviour shared between Auction and Bid

    Attributes:
        timestamp (int): a Unix-epoch time and is the time of the bid
        user_id (int): user ID
        item (str): a unique string code for the item on sale
        bid_amount (float): a decimal representing the bid_amount in the site's local currency

    Methods:
        cls.find_by_item(item):
            Available through the parent class. Returns the bids matching the provided item
        save():
            Available through the parent class. Stores the bid in its in-memory repository, if validations are succesful.
    """

    repository = []

    def __init__(self, timestamp=0, user_id=0, item=None, bid_amount=0.0):
        super().__init__(timestamp, user_id, item)
        self.bid_amount = bid_amount

    def _auction(self):
        from auction import Auction

        try:
            return Auction.find_by_item(self.item)[0]
        except IndexError:
            return False

    def _validate(self):
        if not self._auction():
            logging.debug(f"Invalid bid {self}: item not listed for sale")
            return False
        auction_closing_time = self._auction().closing_time
        if self.timestamp > auction_closing_time:
            logging.debug(
                f"Invalid bid {self}: bid added after auction closed at timestamp={auction_closing_time}"
            )
            return False
        if self.user_id == self._auction().user_id:
            logging.debug(
                f"Invalid bid {self}: user with id={self.user_id} cannot bid on own listing"
            )
            return False
        if self._user_bids():
            user_max_bid = max((bid.bid_amount for bid in self._user_bids()))
            if self.bid_amount <= user_max_bid:
                logging.debug(
                    f"Invalid bid {self}: bid_amount={self.bid_amount} lower than previously placed bid_amount={user_max_bid} by same user"
                )
                return False

        return True

    def _user_bids(self):
        return [bid for bid in Bid.repository if bid.user_id == self.user_id]
