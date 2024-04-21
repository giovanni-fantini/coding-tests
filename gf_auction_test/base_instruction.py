class BaseInstruction:
    """A class to model the common behaviour between Auction and Bid instructions

    Attributes:
        timestamp (int): a Unix-epoch time and is the auction start time
        user_id (int): user ID
        item (str): a unique string code for the item on sale

    Methods:
        cls.find_by_item(item):
            Returns the instructions matching the provided item
        save():
            Stores the instruction in its in-memory repository, if validations are succesful
    """

    repository = []

    @classmethod
    def find_by_item(cls, item):
        """Returns the instructions matching the provided item

        Args:
            item (str): the unix string code for the item

        Returns:
            list: a list of the matching BaseInstruction objects
        """
        return [element for element in cls.repository if element.item == item]

    def __init__(self, timestamp, user_id, item):
        self.timestamp = timestamp
        self.user_id = user_id
        self.item = item

    def __str__(self):
        return f"with timestamp={self.timestamp} for item={self.item}"

    def save(self):
        """Stores the instruction in its in-memory repository, if validations are succesful

        Returns:
            BaseInstruction: returns self
        """
        if not self._validate():
            return None

        self.repository.append(self)
        return self

    def _validate(self):
        raise NotImplementedError
