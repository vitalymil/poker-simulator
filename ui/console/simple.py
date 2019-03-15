
import os

class SimplePokerConsole:
    def events_handler(self, event_type, event_data):
        os.system('clear')

        input('prest enter to continue')

    def __print_players(self, event_data):
        
    def __print_table(self, event_data):
        print('----------------------------------')

        if len(event_data.community_cards):
            community_cards_str = ''
            for community_card in event_data.community_cards:
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