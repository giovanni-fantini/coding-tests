import unittest
from auction import Auction
from bid import Bid


class BidTestCase(unittest.TestCase):
    def setUp(self):
        self.auction_1 = Auction(10, 1, "toaster_1", 10.0, 20)
        self.auction_2 = Auction(15, 8, "tv_1", 250.0, 20)
        Auction.repository = [self.auction_1, self.auction_2]
        self.bid_1 = Bid(12, 8, "toaster_1", 7.50)
        self.bid_2 = Bid(13, 5, "toaster_1", 12.50)
        Bid.repository = [self.bid_1, self.bid_2]

    def tearDown(self):
        Auction.repository = []
        Bid.repository = []

    def test_find_by_item_returns_the_right_list(self):
        """Tests that find_by_item() filters the bid repository correctly by item"""
        result = Bid.find_by_item("toaster_1")
        self.assertEqual(result, [self.bid_1, self.bid_2])
        empty_result = Bid.find_by_item("something")
        self.assertEqual(empty_result, [])

    def test_save_stores_a_valid_bid(self):
        """Tests that save() stores a valid bid in the in-memory bid repository"""
        new_bid = Bid(18, 2, "toaster_1", 100).save()
        self.assertEqual(Bid.repository, [self.bid_1, self.bid_2, new_bid])

    def test_save_does_not_store_bid_on_unexisting_auction(self):
        """Tests that save() does not store an invalid bid (e.g. a bid for an item not on auction) in the in-memory bid repository"""
        Bid(18, 2, "other_item", 100).save()
        self.assertEqual(Bid.repository, [self.bid_1, self.bid_2])

    def test_save_logs_message_for_bid_on_unexisting_auction(self):
        """Tests that save() for an invalid bid (e.g. a bid for an item not on auction) logs a DEBUG message"""
        with self.assertLogs(level="DEBUG") as logger:
            Bid(18, 2, "other_item", 100).save()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Invalid bid with timestamp=18 for item=other_item: item not listed for sale"
                ],
            )

    def test_save_does_not_store_bid_after_closing_time(self):
        """Tests that save() does not store an invalid bid (e.g. a bid for an item whose auction is closed) in the in-memory bid repository"""
        Bid(21, 2, "toaster_1", 100).save()
        self.assertEqual(Bid.repository, [self.bid_1, self.bid_2])

    def test_save_logs_message_for_bid_after_closing_time(self):
        """Tests that save() for an invalid bid (e.g. a bid for an item whose auction is closed) logs a DEBUG message"""
        with self.assertLogs(level="DEBUG") as logger:
            Bid(21, 2, "toaster_1", 100).save()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Invalid bid with timestamp=21 for item=toaster_1: bid added after auction closed at timestamp=20"
                ],
            )

    def test_save_does_not_store_bid_from_listing_owner(self):
        """Tests that save() does not store an invalid bid (e.g. a bid from an user on its own listing) in the in-memory bid repository"""
        Bid(11, 1, "toaster_1", 100).save()
        self.assertEqual(Bid.repository, [self.bid_1, self.bid_2])

    def test_save_logs_message_for_bid_from_listing_owner(self):
        """Tests that save() for an invalid bid (e.g. a bid from an user on its own listing) logs a DEBUG message"""
        with self.assertLogs(level="DEBUG") as logger:
            Bid(11, 1, "toaster_1", 100).save()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Invalid bid with timestamp=11 for item=toaster_1: user with id=1 cannot bid on own listing"
                ],
            )

    def test_save_does_not_store_smaller_bid_from_same_user(self):
        """Tests that save() does not store an invalid bid (e.g. a bid from a user who previously submitted a larger one) in the in-memory bid repository"""
        Bid(14, 5, "toaster_1", 10.0).save()
        self.assertEqual(Bid.repository, [self.bid_1, self.bid_2])

    def test_save_logs_message_for_smaller_bid_from_same_user(self):
        """Tests that save() for an invalid bid (e.g. a bid from a user who previously submitted a larger one) logs a DEBUG message"""
        with self.assertLogs(level="DEBUG") as logger:
            Bid(14, 5, "toaster_1", 10.0).save()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Invalid bid with timestamp=14 for item=toaster_1: bid_amount=10.0 lower than previously placed bid_amount=12.5 by same user"
                ],
            )


if __name__ == "__main__":
    unittest.main(buffer=True)
