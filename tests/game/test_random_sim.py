"""Headless random-vs-random simulation sanity checks."""

import random

from game.constants import MAX_POINTS, PLAYER_COUNT
from game.deck import deal, full_deck, shuffle_deck
from game.state import Phase, create_round


def test_random_full_rounds():
    rng = random.Random(42)
    for _ in range(200):
        deck = shuffle_deck(full_deck(), rng)
        hands = deal(deck)
        trump = rng.randint(0, 3)
        leader = rng.randint(0, 3)
        rnd = create_round(hands, trump, leader)

        for seat in range(PLAYER_COUNT):
            rnd.submit_prediction(seat, rng.randint(0, MAX_POINTS))
        rnd.start_play()

        while rnd.phase is Phase.PLAY:
            seat = rnd.current_player()
            legal = rnd.legal_plays_for(seat)
            assert legal
            card_id = rng.choice(legal)
            rnd.play_card(seat, card_id)

        assert sum(rnd.collected()) == MAX_POINTS
        assert all(len(h) == 0 for h in rnd.hands)
