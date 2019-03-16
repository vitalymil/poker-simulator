
import os

class ConsoleInputHandler:
    def input_handler(self, input_type, input_data):
        if input_type == 'get_action':
            return self.__get_action_input()
        elif input_type == 'show_cards':
            return self.__get_show_cards()

    def __get_action_input(self):
        action_type = input('enter action [fold/check/call/raise]\n')
        action_bet = 0

        if action_type in ('call', 'raise'):
            action_bet = int(input('enter bet size\n'))

        return {
            'type': action_type,
            'bet': action_bet
        }

    def __get_show_cards(self):
        return input('show cards? [y/n]\n') == 'y'