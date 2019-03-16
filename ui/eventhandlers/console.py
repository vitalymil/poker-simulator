
import os

class ConsoleEventHandler:
    def event_handler(self, event_type, event_data):
        os.system('clear')

        self.__print_status(event_type, event_data)
        self.__print_table(event_data)
        self.__print_players(event_type, event_data)

        input('prest enter to continue')

    def __print_status(self, event_type, event_data):
        if event_type == 'start_round':
            print('Round stating')
        elif event_type == 'action':
            player = event_data["action_seat"]["player"]
            action_type = event_data["action"]["type"]
            action_bet = event_data["action"]["bet"]
            print(f'Player {player} made action: {action_type} {action_bet if action_bet > 0 else ""}')
        elif event_type == 'table_cards_updated':
            print('Table cards updated')
        elif event_type == 'win_announce':
            player = event_data["action_seat"]["player"]
            win_size = event_data["action"]["size"]
            print(f'Player {player} won {win_size}')

    def __print_players(self, event_type, event_data):
        for player_idx in range(len(event_data["players"])):
            player = event_data["players"][player_idx]
            cards = event_data["cards"][player_idx]

            print(f'Player {player["player"]} {"(button)" if player["button"] else ""}')
            print(f'bank: {player["player"].get_money()}')

            if event_type != 'table_cards_updated':
                print(f'bet: {player["current_bet"] + player["total_bet"]}')
            else:
                print(f'bet: {player["total_bet"]}')
                
            print(f'status: {player["status"]}')
            print(f'cards: {self.__card_to_str(cards[0])}, {self.__card_to_str(cards[1])}')
            print('-------------')

    def __print_table(self, event_data):
        print('----------------------------------')

        if len(event_data['community_cards']) > 0:
            community_cards_str = ''
            for community_card in event_data['community_cards']:
                community_cards_str = community_cards_str + self.__card_to_str(community_card) + ', '
            print(community_cards_str[:-2])
        else:
            print('-------- NO CARD ON TABLE --------')

        print('----------------------------------')

    def __card_to_str(self, card):
        if card['rank'] < 11:
            return str(card['rank']) + card['suit']
        else:
            rank_mapper = {
                11: 'J',
                12: 'Q',
                13: 'K',
                14: 'A'
            }
            return rank_mapper[card['rank']] + card['suit']