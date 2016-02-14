import random
import uuid


class CAHPlayer(object):
    """
    Represents a player in the game for the game logic portion of the server.
    """

    @property
    def hand_size(self):
        return len(self.hand)

    def __init__(self, name=None):
        self.connected = False
        self.hand = set()
        self.awesome_points = 0
        self.is_czar = False
        self.name = name
        self.id = uuid.uuid4()
        self.was_czar = 0
        self.submitted = None

    @property
    def player_id(self):
        return self.id

    def play_card(self, card_to_play):
        assert card_to_play == type(Card)
        self.submitted = card_to_play
        return (self.id, card_to_play)

    def judge_card(self, card_chosen):
        assert card_chosen == type(Card)
        assert self.is_czar
        return (self.id, card_chosen)

class Card(object):
    """
    Pythonic representation for the cards in the json.
    """
    def __init__(self, card_id, card_type, text, num_answers, expansion):
        self.card_id = card_id
        self.card_type = card_type
        self.text = text
        self.num_answers = num_answers
        self.expansion = expansion


class AICAHPlayer(CAHPlayer):
    """
    Purely for testing, will pick cards at random to facilitate testing alone.
    """

    def play_card(self, card_to_play):
        card = random.choice(self.hand)
        return card

    def judge_card(self, cards):
        return random.choice(cards)
