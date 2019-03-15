
import os

class PokerDummyPlayer:
    def __init__(self, initial_money, name):
        self.__money = initial_money
        self.__name = name
    
    def has_money(self):
        return self.__money > 0
    
    def take_money(self, amount):
        to_take = min(self.__money, amount)
        self.__money -= amount
        return to_take
    
    def show_cards(self):
        return True
    
    def get_action(self, table, cards):
        max_bet = 0
        my_seat = None
        for seat in table.seats:
            if seat['player'] == self:
                my_seat = seat
            if seat['status'] != 'fold' and seat['current_bet'] > max_bet:
                max_bet = seat['current_bet']
        if max_bet == 0 or max_bet == my_seat['current_bet']:
            action = { 'type': 'check', 'bet': 0 }
        elif my_seat['current_bet'] < max_bet:
            action = { 'type': 'call', 'bet': min(self.__money, max_bet - my_seat['current_bet']) }

        return action

    def finish_round(self, table, seat_index, cards, wins, revealed_cards):
        self.__money += wins[seat_index]

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name