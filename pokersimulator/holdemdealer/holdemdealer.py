
class HoldemDealer:
    def __init__(self, table, deck, small, big):
        self.__table = table
        self.__deck = deck
        self.__small = small
        self.__big = big

    def init_game(self):
        self.__table.reset()
        self.__button_index = -1

        for idx, seat in enumerate(self.__table.seats):
            if seat['player'].has_money():
                if not self.__button_index < 0:
                    seat['button'] = True
                    self.__button_index = idx
            else:
                raise ValueError(f'player {idx} has no money')
        
    def play_round(self):
        if len(self.__table.seats) < 2:
            raise ValueError('not enough avaliable players')

        self.__inplay_count = len(self.__table.seats)
        self.__table.community_cards = []
        for seat in self.__table.seats:
            seat['total_bet'] = 0
            seat['status'] = None
            seat['small'] = False
            seat['big'] = False
        
        self.__next_button()
        self.__deal_cards()

        return self.__play_preflop()

    def __next_button(self):
        self.__table.seats[self.__button_index]['button'] = False
        self.__button_index = (self.__button_index + 1) % len(self.__table.seats)

        self.__table.seats[self.__button_index]['button'] = True
        self.__table.seats[(self.__button_index + 1) % len(self.__table.seats)]['small'] = True
        self.__table.seats[(self.__button_index + 2) % len(self.__table.seats)]['big'] = True
    
    def __deal_cards(self):
        self.__deck.reset()
        self.__deck.shuffle()

        self.__players_cards = []
        for _ in self.__table.seats:
            self.__players_cards.append([
                self.__deck.draw(),
                self.__deck.draw()
            ])

    def __get_seat_action(self, seat_index):
        seat = self.__table.seats[seat_index]

        if (seat['status'] == 'allin' or 
            seat['status'] == 'fold' or
            (seat['current_bet'] == self.__cur_bet and seat['status'] != None)):
            return False
        
        action = None
        valid_action = False
        while not valid_action:
            action = seat['player'].get_action(self.__table, self.__players_cards[seat_index])
            valid_action = (action['type'] == 'fold' or
                            (action['type'] == 'check' and seat['current_bet'] == self.__cur_bet) or
                            (action['type'] == 'call' and seat['current_bet'] + action['bet'] == self.__cur_bet) or
                            (action['type'] == 'raise' and seat['current_bet'] + action['bet'] > self.__cur_bet) or
                            (action['type'] == 'allin' and action['bet'] > 0 and not seat['player'].has_money()))
        
        seat['status'] = action['type']
        if (action['type'] == 'call' or
            action['type'] == 'raise' or
            action['type'] == 'allin'):
            seat['current_bet'] += seat['player'].take_money(action['bet'])
            if seat['current_bet'] > self.__cur_bet:
                self.__cur_bet = seat['current_bet']

        if action['type'] == 'fold':
            self.__inplay_count -= 1

        return True

    def __start_betting(self, with_blinds):
        self.__cur_bet = self.__big if with_blinds else 0

        for seat in self.__table.seats:
            seat['current_bet'] = 0
            seat['status'] = None
            if with_blinds:
                if seat['small']:
                    seat['current_bet'] = seat['player'].take_money(self.__small)
                if seat['big']:
                    seat['current_bet'] = seat['player'].take_money(self.__big)
            
            if not seat['player'].has_money():
                seat['status'] = 'allin'

        passes_count = 0
        cur_seat_index = (self.__button_index + 1) % len(self.__table.seats)
        if with_blinds:
            cur_seat_index = (cur_seat_index + 2) % len(self.__table.seats)

        while passes_count < len(self.__table.seats) and self.__inplay_count > 1:
            if not self.__get_seat_action(cur_seat_index):
                passes_count += 1
            else:
                passes_count = 0
            cur_seat_index = (cur_seat_index + 1) % len(self.__table.seats)

        for seat in self.__table.seats:
            seat['total_bet'] = seat['total_bet'] + seat['current_bet']

    def total_bet_order(self, seat_index):
        return self.__table.seats[seat_index]['total_bet']

    def __showdown(self):
        revealed_cards = [None] * len(self.__table.seats)
        compiting_hands = [None] * len(self.__table.seats)
        cur_seat_index = (self.__button_index + 1) % len(self.__table.seats)
        

        for _ in range(len(self.__table.seats)):
            seat = self.__table.seats[cur_seat_index]
            cur_seat_index = (cur_seat_index + 1) % len(self.__table.seats)

            if seat['status'] != 'fold':
                compiting_hands[cur_seat_index] = self.__players_cards[cur_seat_index]
                if seat['player'].show_cards():
                    revealed_cards[cur_seat_index] = self.__players_cards[cur_seat_index]
                else:
                    if self.__inplay_count > 1:
                        seat['status'] = 'fold'
                        compiting_hands[cur_seat_index] = None
        
        results = self.__deck.compute_winner(compiting_hands, self.__table.community_cards)
        winnings = [0] * len(self.__table.seats)

        for seat in self.__table.seats:
            seat['current_bet'] = seat['total_bet']

        for result in results:
            pots = []
            result.sort(key=self.total_bet_order)
            for winner_index in result:
                pot = 0
                winner_seat = self.__table.seats[winner_index]
                for seat in self.__table.seats:
                    seat_pay = min(winner_seat['current_bet'], seat['current_bet'])
                    pot += seat_pay
                    seat['current_bet'] -= seat_pay
                pots.append(pot)
            for result_index in range(len(result)):
                for pot_index in range(result_index + 1):
                    winnings[result[result_index]] += pots[pot_index] / (len(pots) - pot_index)
        
        for win_index in range(len(winnings)):
            self.__table.seats[win_index]['player'].finish_round(self.__table, win_index,
                self.__players_cards[win_index], winnings, revealed_cards)

        self.__table.seats = [seat for seat in self.__table.seats if seat['player'].has_money()]

        return len(self.__table.seats) > 2

    def __play_preflop(self):
        return self.__play_stage(0, self.__play_flop, True)
    
    def __play_flop(self):
        return self.__play_stage(3, self.__play_turn)

    def __play_turn(self):
        return self.__play_stage(1, self.__play_river)

    def __play_river(self):
        return self.__play_stage(1, self.__showdown)

    def __play_stage(self, draw_amount, next_stage, with_blinds=False):
        for _ in range(draw_amount):
            self.__table.community_cards.append(self.__deck.draw())
            
        self.__start_betting(with_blinds)
        if self.__inplay_count < 2:
            return self.__showdown()
        
        return next_stage()
        
