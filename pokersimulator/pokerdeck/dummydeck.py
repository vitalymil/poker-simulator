from .pockerdeck import *

class DummyDeck(PokerDeck):
    def __init__(self):
        super().__init__()

    def shuffle(self):
        self.__cards = [
            { 'suit': 's', 'rank': 14 },
            { 'suit': 'h', 'rank': 2  },
            { 'suit': 'd', 'rank': 3  },
            { 'suit': 'h', 'rank': 6  },
            { 'suit': 'd', 'rank': 7  },

            { 'suit': 'd', 'rank': 14 },
            { 'suit': 'h', 'rank': 14 },

            { 'suit': 'd', 'rank': 13 },
            { 'suit': 'h', 'rank': 13 },

            { 'suit': 'd', 'rank': 12 },
            { 'suit': 'h', 'rank': 12 }
        ]
    
    def draw(self):
        return self.__cards.pop()