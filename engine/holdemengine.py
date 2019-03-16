
from engine.dealers.holdemdealer import HoldemDealer
from engine.decks.dummydeck import DummyDeck
from engine.players.dummyplayer import PokerDummyPlayer
from engine.players.inputplayer import PokerInputPlayer
from engine.tables.pokertable import PokerTable

class HoldemEngine:
    def __init__(self, event_handler, input_handler):
        self._players = [
            PokerDummyPlayer(1000, 'A'), 
            PokerDummyPlayer(1000, 'B'), 
            PokerInputPlayer(1000, 'C', input_handler)
        ]
        self._table = PokerTable(self._players)
        self._deck = DummyDeck()
        self._dealer = HoldemDealer(self._table, self._deck, 25, 50, event_handler)
    
    def start(self):
        self._dealer.init_game()
        self._dealer.play_round()