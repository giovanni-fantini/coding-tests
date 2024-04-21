class Heartbeat:
    """A simple class to model heartbeat instructions, these messages may appear periodically in the input
    to ensure that auctions can be closed in the absence of bids.

    Attributes:
        timestamp (int): is an integer representing a Unix epoch time
    """

    def __init__(self, timestamp):
        self.timestamp = timestamp
