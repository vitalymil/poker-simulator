
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
        print(f'player {self.__name}')
        print(f'money: {self.__money}, cards: {cards}')
        table.print()
        print('\n')

        max_bet = 0
        my_seat = None
        for seat in table.seats:
            if seat['player'] == self:
                my_seat = seat
            if seat['status'] != 'fold' and seat['current_bet'] > max_bet:
                max_bet = seat['current_bet']
        if max_bet == 0 or max_bet == my_seat['current_bet']:
            return { 'type': 'check', 'bet': 0 }
        elif my_seat['current_bet'] < max_bet:
            return { 'type': 'call', 'bet': min(self.__money, max_bet - my_seat['current_bet']) }

    def finish_round(self, table, seat_index, cards, wins, revealed_cards):
        self.__money += wins[seat_index]

        print(f'player {self.__name}, seat {seat_index}')
        print(f'money: {self.__money}\ncards: {cards}\nwins: {wins}\nother cards: {revealed_cards}')
        table.print()
        print('\n')

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name