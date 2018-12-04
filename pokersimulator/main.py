
from pokertable.pokertable import *
from pokerinputplayer.pokerinputplayer import *
from pokerdeck.pockerdeck import *
from holdemdealer.holdemdealer import *

players = [PokerInputPlayer(1000, 'A'), PokerInputPlayer(1000, 'B'), PokerInputPlayer(1000, 'C')]
table = PokerTable(players)
deck = PokerDeck()
dealer = HoldemDealer(table, deck, 25, 50)

dealer.init_game()
dealer.play_round()