
class PokerInputPlayer:
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
        return input('show cards? [y/n]\n') == 'y'
    
    def get_action(self, table, cards):
        print(f'player {self.__name}')
        print(f'money: {self.__money}, cards: {cards}')
        table.print()
        print('\n')

        action_type = input('enter action [fold/check/call/raise]\n')
        action_bet = 0

        if action_type in ('call', 'raise'):
            action_bet = int(input('enter bet size\n'))

        return {
            'type': action_type,
            'bet': action_bet
        }

    def finish_round(self, table, cards, win_size, revealed_cards):
        self.__money += win_size

        print(f'player {self.__name}')
        print(f'money: {self.__money}, cards: {cards}, win: {win_size}, other cards: {revealed_cards}')
        table.print()
        print('\n')

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name