from io import StringIO
import unittest
from unittest.mock import patch
from auction import Auction
from bid import Bid


class AuctionTestCase(unittest.TestCase):
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
        """Tests that find_by_item() filters the auction repository correctly by item"""
        result = Auction.find_by_item("toaster_1")
        self.assertEqual(result, [self.auction_1])
        empty_result = Auction.find_by_item("something")
        self.assertEqual(empty_result, [])

    def test_save_stores_a_valid_auction(self):
        """Tests that save() stores a valid auction in the in-memory auctions repository"""
        new_auction = Auction(18, 2, "new_item", 10.0, 25).save()
        self.assertEqual(
            Auction.repository, [self.auction_1, self.auction_2, new_auction]
        )

    def test_save_does_not_store_an_invalid_auction(self):
        """Tests that save() does not store an invalid auction (e.g. a auction for an item previously listed for auction) in the in-memory auctions repository"""
        Auction(18, 2, "toaster_1", 10.0, 25).save()
        self.assertEqual(Auction.repository, [self.auction_1, self.auction_2])

    def test_save_logs_message_for_invalid_auction(self):
        """Tests that save() for an invalid auction (e.g. a auction for an item previously listed for auction) logs a DEBUG message"""
        with self.assertLogs(level="DEBUG") as logger:
            Auction(18, 2, "toaster_1", 10.0, 25).save()
            self.assertEqual(
                logger.output,
                [
                    "DEBUG:root:Invalid auction with timestamp=18 for item=toaster_1: item previously listed for sale"
                ],
            )

    def test_find_by_closing_time_returns_the_right_list(self):
        """Tests that find_by_closing_time() filters the auction repository correctly by the provided closing time"""
        result = Auction.find_by_closing_time(20)
        self.assertEqual(result, [self.auction_1, self.auction_2])
        empty_result = Auction.find_by_closing_time(25)
        self.assertEqual(empty_result, [])

    def test_close_when_no_valid_bids(self):
        """Tests that close() sets the right winner, price_paid and status when there are no valid bids"""
        result = self.auction_2.close()
        self.assertEqual(result.winner, "")
        self.assertEqual(result.price_paid, 0.00)
        self.assertEqual(result.status, "UNSOLD")

    def test_close_message_output_when_no_valid_bids(self):
        """Tests that close() prints the right message when there are no valid bids"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.auction_2.close()
            self.assertEqual(fake_out.getvalue(), "20|tv_1||UNSOLD|0.00|0|0.00|0.00\n")

    def test_close_when_bids_below_reserve_price(self):
        """Tests that close() sets the right winner, price_paid and status when bids are below the reserve_price"""
        Bid.repository.append(Bid(18, 1, "tv_1", 150.00))
        Bid.repository.append(Bid(19, 3, "tv_1", 200.00))
        result = self.auction_2.close()
        self.assertEqual(result.winner, "")
        self.assertEqual(result.price_paid, 0.00)
        self.assertEqual(result.status, "UNSOLD")

    def test_close_message_output_when_bids_below_reserve_price(self):
        """Tests that close() prints the right message when bids are below the reserve_price"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            Bid.repository.append(Bid(18, 1, "tv_1", 150.00))
            Bid.repository.append(Bid(19, 3, "tv_1", 200.00))
            self.auction_2.close()
            self.assertEqual(
                fake_out.getvalue(), "20|tv_1||UNSOLD|0.00|2|200.00|150.00\n"
            )

    def test_close_when_bid_above_reserve_price(self):
        """Tests that close() sets the right winner, price_paid and status when one bid is above the reserve_price"""
        result = self.auction_1.close()
        self.assertEqual(result.winner, 5)
        self.assertEqual(result.price_paid, 10.00)
        self.assertEqual(result.status, "SOLD")

    def test_close_message_output_when_bid_above_reserve_price(self):
        """Tests that close() prints the right message when one bid is above the reserve_price"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.auction_1.close()
            self.assertEqual(
                fake_out.getvalue(), "20|toaster_1|5|SOLD|10.00|2|12.50|7.50\n"
            )

    def test_close_when_bids_above_reserve_price(self):
        """Tests that close() sets the right winner, price_paid and status when more than one bid is above the reserve_price"""
        Bid.repository.append(Bid(17, 8, "toaster_1", 20.00))
        result = self.auction_1.close()
        self.assertEqual(result.winner, 8)
        self.assertEqual(result.price_paid, 12.50)
        self.assertEqual(result.status, "SOLD")

    def test_close_message_output_when_bids_above_reserve_price(self):
        """Tests that close() prints the right message when more than one bid is above the reserve_price"""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            Bid.repository.append(Bid(17, 8, "toaster_1", 20.00))
            self.auction_1.close()
            self.assertEqual(
                fake_out.getvalue(), "20|toaster_1|8|SOLD|12.50|3|20.00|7.50\n"
            )


if __name__ == "__main__":
    unittest.main(buffer=True)
