
from engine.dealers.holdemdealer import HoldemDealer
from engine.decks.dummydeck import DummyDeck
from engine.players.dummyplayer import PokerDummyPlayer
from engine.tables.pokertable import PokerTable

class HoldemEngine:
    def __init__(self, event_notifier):
        self._players = [
            PokerDummyPlayer(1000, 'A'), 
            PokerDummyPlayer(1000, 'B'), 
            PokerDummyPlayer(1000, 'C')
        ]
        self._table = PokerTable(self._players)
        self._deck = DummyDeck()
        self._dealer = HoldemDealer(self._table, self._deck, 25, 50, event_notifier)
    
    def start(self):
        self._dealer.init_game()
        self._dealer.play_round()