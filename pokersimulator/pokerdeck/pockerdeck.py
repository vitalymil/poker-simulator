import random

class PokerDeck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.__cards = []
        for suit in ('d', 'h', 's', 'c'):
            for rank in range(2,15):
                self.__cards.append({
                    'suit': suit,
                    'rank': rank
                })
        
    def shuffle(self):
        self.__cards.sort(key=PokerDeck.__random_map)
    
    def draw(self):
        return self.__cards.pop()
    
    def compute_winner(self, hands, community_cards):
        pass

    def __compute_score(self, hand):
        hand.sort(key=PokerDeck.__card_rank_map)

        same_suit = True
        is_streight = True
        pairs = [0] * len(hand)
        pairs_count = 0

        for card_index in range(1, len(hand)):
            same_suit = same_suit and hand[card_index]['suit'] == hand[card_index - 1]['suit']
            is_streight = is_streight and hand[card_index]['rank'] - 1 == hand[card_index - 1]['rank']
            if hand[card_index]['rank'] == hand[card_index - 1]:
                pairs[card_index - 1] = True
                pairs_count += 1
        
        if is_streight:
            if same_suit:
                if hand[0]['rank'] == 10:
                    pass #royal
                else:
                    pass #starit-flush
            else:
                pass #streight
        elif same_suit:
            pass #flush
        elif (pairs_count == 3 and 
                (
                    (pairs[0] and pairs[1] and pairs[2]) or
                    (pairs[1] and pairs[2] and pairs[3])
                )
            ):
            pass #4ofakind
        elif (pairs_count == 3 and 
                (
                    (pairs[0] and pairs[1] and pairs[3]) or
                    (pairs[0] and pairs[2] and pairs[3])
                )
            ):
            pass #house
        elif (pairs_count == 2 and 
                (
                    (pairs[0] and pairs[1]) or
                    (pairs[1] and pairs[2]) or
                    (pairs[2] and pairs[3])
                )
            ):
            pass #three
        elif (pairs_count == 2 and 
                (
                    (pairs[0] and pairs[2]) or
                    (pairs[1] and pairs[3])
                )
            ):
            pass #twopair
        elif pairs_count == 1:
            return self.__pair_score(hand, pairs)
        else:
            return self.__high_card_score(hand)

    def __high_card_score(self, hand):
        return (0x1 * hand[0]['rank'] +
                0x10 * hand[1]['rank'] +
                0x100 * hand[2]['rank'] +
                0x1000 * hand[3]['rank'] +
                0x10000 * hand[4]['rank'])
    
    def __pair_score(self, hand, pairs):
        res = 0
        high_count = 0
        for i in range(len(hand)):
            if pairs[i]:
                res += (16**5) * hand[i]['rank']
            elif i > 0 and pairs[i - 1]:
                pass
            else:
                res += (16**(high_count + 2)) * hand[i]['rank'] # incorrect, need to reverse order
                high_count += 1
        return res

    def __two_pairs_score(self, hand, pairs):



    @staticmethod
    def __random_map(element):
        return random.random()
    
    @staticmethod
    def __card_rank_map(card):
        return card['rank']