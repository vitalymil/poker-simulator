
from engine.dealers.holdemdealer import HoldemDealer
from engine.decks.dummydeck import DummyDeck
from engine.players.dummyplayer import PokerDummyPlayer
from engine.tables.pokertable import PokerTable
import test

players = [PokerDummyPlayer(1000, 'A'), PokerDummyPlayer(1000, 'B'), PokerDummyPlayer(1000, 'C')]
table = PokerTable(players)
deck = DummyDeck()
dealer = HoldemDealer(table, deck, 25, 50)

dealer.init_game()
dealer.play_round()