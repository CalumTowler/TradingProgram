"""
Testing out Classes

24/03/19: initial commit
Author: Calum Towler
"""

class Stock:
    def __init__(self, ticker, open_time, open_value, close_value, low, high, volume):
        self.ticker = ticker
        self.open_time = open_time
        self.open_value = open_value
        self.close_value = close_value
        self.low = low
        self.high = high
        self.volume = volume

    def direction_increasing(self):
        if self.open_value < self.close_value:
            return True
        else:
            return False

    def spike(self):
        if self.volume >= 100000:
            return True
        else:
            return False


#MSFT = Stock("MSFT", 1000, 567.2, 572.5, 567.2,572.5, 106437)
#print(MSFT.low)
#print(MSFT.high)
#print(MSFT.direction_increasing())
#print(MSFT.spike())
