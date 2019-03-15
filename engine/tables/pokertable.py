
class PokerTable:
    def __init__(self, players):
        self._players = players
        self.reset()
    
    def reset(self):
        self.community_cards = []
        self.seats = []
        for player in self._players:
            self.seats.append({
                'player': player,
                'status': None,
                'total_bet': 0,
                'current_bet': 0,
                'button': False,
                'small': False,
                'big': False
            })