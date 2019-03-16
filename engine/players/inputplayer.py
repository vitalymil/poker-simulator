
class PokerInputPlayer:
    def __init__(self, initial_money, name, input_hanlder):
        self.__money = initial_money
        self.__name = name
        self.__input_hanlder = input_hanlder
    
    def get_money(self):
        return self.__money

    def has_money(self):
        return self.__money > 0
    
    def take_money(self, amount):
        to_take = min(self.__money, amount)
        self.__money -= amount
        return to_take
    
    def show_cards(self):
        return self.__input_hanlder('show_cards', {})
    
    def get_action(self, table, cards):
        return self.__input_hanlder('get_action', {
            'table': table, 
            'cards': cards
        })

    def finish_round(self, table, cards, win_size, revealed_cards):
        self.__money += win_size

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name