class MovingTotal:
    def __init__(self):
        self.numbers = []

    def append(self, numbers):
        """
        :param numbers: (list) The list of numbers.
        """
        self.numbers += numbers

    def contains(self, total):
        """
        :param total: (int) The total to check for.
        :returns: (bool) If MovingTotal contains the total.
        """
        for i in range(0, len(self.numbers) - 2):
            if sum(self.numbers[i:i + 3]) == total:
                return True
        return False
    
if __name__ == "__main__":
    movingtotal = MovingTotal()
    
    movingtotal.append([1, 2, 3, 4])
    print(movingtotal.contains(6))
    print(movingtotal.contains(9))
    print(movingtotal.contains(12))
    print(movingtotal.contains(7))
    
    movingtotal.append([5])
    print(movingtotal.contains(6))
    print(movingtotal.contains(9))
    print(movingtotal.contains(12))
    print(movingtotal.contains(7))
    
    movingtotal.append([6])
    print(movingtotal.contains(6))
    print(movingtotal.contains(9))
    print(movingtotal.contains(12))
    print(movingtotal.contains(7))
    print(movingtotal.contains(15))
    print(movingtotal.contains(16))
    print(movingtotal.contains(11))