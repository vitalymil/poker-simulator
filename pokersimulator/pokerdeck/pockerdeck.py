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

    def __score_map(self, elem):
        return elem[0]
    
    def compute_winner(self, hands, community_cards):
        if len(community_cards) < 5:
            for idx, hand in enumerate(hands):
                if hand != None:
                    return [[idx]]

        hand_scores = [0] * len(hands)
        for idx, hand in enumerate(hands):
            score = 0
            if hand != None:
                score = self.__compute_best_score(hand, community_cards)
            hand_scores[idx] = (score, idx)

        hand_scores.sort(key=self.__score_map)

        result = [[hand_scores[0][1]]]
        for i in range(1, len(hand_scores)):
            if hand_scores[i][0] == hand_scores[i - 1][0]:
                result[len(result) - 1].append(hand_scores[i][1])
            else:
                result.append([hand_scores[i][1]])

        return result

    def __compute_best_score(self, hand, community_cards):
        all_cards = hand + community_cards
        max_score = -1
        for i in range(len(all_cards)):
            for j in range(i, len(all_cards)):
                cur_score = self.__compute_score([all_cards[k] for k in range(len(all_cards)) if k not in (i, j)])
                if cur_score > max_score:
                    max_score = cur_score
        return max_score


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
                    return self.__royal_score(hand)
                else:
                    return self.__streight_flush_score(hand)
            else:
                return self.__streight_score(hand)
        elif same_suit:
            return self.__flush_score(hand)
        elif (pairs_count == 3 and 
                (
                    (pairs[0] and pairs[1] and pairs[2]) or
                    (pairs[1] and pairs[2] and pairs[3])
                )
            ):
            return self.__quads_score(hand, pairs)
        elif (pairs_count == 3 and 
                (
                    (pairs[0] and pairs[1] and pairs[3]) or
                    (pairs[0] and pairs[2] and pairs[3])
                )
            ):
            return self.__house_score(hand, pairs)
        elif (pairs_count == 2 and 
                (
                    (pairs[0] and pairs[1]) or
                    (pairs[1] and pairs[2]) or
                    (pairs[2] and pairs[3])
                )
            ):
            return self.__trips_score(hand, pairs)
        elif (pairs_count == 2 and 
                (
                    (pairs[0] and pairs[2]) or
                    (pairs[1] and pairs[3])
                )
            ):
            return self.__two_pairs_score(hand, pairs)
        elif pairs_count == 1:
            return self.__pair_score(hand, pairs)
        else:
            return self.__high_card_score(hand)

    def __high_card_score(self, hand):
        return ((16**0) * hand[0]['rank'] +
                (16**1) * hand[1]['rank'] +
                (16**2) * hand[2]['rank'] +
                (16**3) * hand[3]['rank'] +
                (16**4) * hand[4]['rank'])
    
    def __pair_score(self, hand, pairs):
        res = 0
        high_count = 0
        for i in range(len(hand)):
            if pairs[i]:
                res += (16**5) * hand[i]['rank']
            elif i > 0 and pairs[i - 1]:
                pass
            else:
                res += (16**(high_count + 2)) * hand[i]['rank']
                high_count += 1
        return res

    def __two_pairs_score(self, hand, pairs):
        res = 0
        pair_count = 0
        for i in range(len(hand)):
            if pairs[i]:
                res += (16**(pair_count + 5)) * hand[i]['rank']
                pair_count += 1
            elif i > 0 and pairs[i - 1]:
                pass
            else:
                res += (16**4) * hand[i]['rank']
        return res

    def __trips_score(self, hand, pairs):
        res = 0
        high_count = 0
        for i in range(len(hand)):
            if pairs[i] and pairs[i + 1]:
                res += (16**7) * hand[i]['rank']
            elif not pairs[i] and (i == 0 or pairs[i - 1]):
                res += (16**(high_count + 5)) * hand[i]['rank']
                high_count += 1
        return res

    def __streight_score(self, hand):
        return (16**8) * hand[4]['rank']

    def __flush_score(self, hand):
        return ((16**5) * hand[0]['rank'] +
                (16**6) * hand[1]['rank'] +
                (16**7) * hand[2]['rank'] +
                (16**8) * hand[3]['rank'] +
                (16**9) * hand[4]['rank'])

    def __house_score(self, hand, pairs):
        res = 0
        for i in range(len(hand) - 2):
            if not pairs[i]:
                res += (16**9) * hand[i]['rank']
            elif pairs[i] and pairs[i + 1]:
                res += (16**10) * hand[i]['rank']
        return res

    def __quads_score(self, hand, pairs):
        res = (16**11) * hand[1]['rank']
        if not pairs[0]:
            res += (16**10) * hand[0]['rank']
        else:
            res += (16**10) * hand[4]['rank']
        return res

    def __streight_flush_score(self, hand):
        return (16**12) * hand[4]['rank']

    def __royal_score(self, hand):
        return 16**13


    @staticmethod
    def __random_map(element):
        return random.random()
    
    @staticmethod
    def __card_rank_map(card):
        return card['rank']