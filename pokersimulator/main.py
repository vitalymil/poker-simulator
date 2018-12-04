
from pokertable.pokertable import *
from pockerplayer.dummyplayer import *
from pokerdeck.dummydeck import *
from holdemdealer.holdemdealer import *

players = [PokerDummyPlayer(1000, 'A'), PokerDummyPlayer(1000, 'B'), PokerDummyPlayer(1000, 'C')]
table = PokerTable(players)
deck = DummyDeck()
dealer = HoldemDealer(table, deck, 25, 50)

dealer.init_game()
dealer.play_round()