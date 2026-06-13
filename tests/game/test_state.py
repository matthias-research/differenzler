"""Tests for round state machine."""

import pytest

from game.cards import card
from game.constants import CARDS_PER_PLAYER, MAX_POINTS, PLAYER_COUNT
from game.deck import deal, full_deck
from game.state import Phase, RoundState, create_round, next_seat


def make_round(trump: int = 1, leader: int = 0) -> RoundState:
    hands = deal(full_deck())
    return create_round(hands, trump, leader)


def test_next_seat_counter_clockwise():
    assert next_seat(0) == 1
    assert next_seat(3) == 0


def test_prediction_phase():
    rnd = make_round()
    assert rnd.phase is Phase.PREDICT
    for seat in range(PLAYER_COUNT):
        rnd.submit_prediction(seat, 50)
    with pytest.raises(ValueError):
        rnd.submit_prediction(0, 40)
    with pytest.raises(ValueError):
        rnd.submit_prediction(0, 200)
    rnd.start_play()
    assert rnd.phase is Phase.PLAY
    assert rnd.trick_number == 1


def test_play_through_full_round():
    trump = 2
    leader = 0
    hands = deal(full_deck())
    rnd = create_round(hands, trump, leader)
    for seat in range(PLAYER_COUNT):
        rnd.submit_prediction(seat, 0)
    rnd.start_play()

    plays = 0
    while rnd.phase is Phase.PLAY:
        seat = rnd.current_player()
        legal = rnd.legal_plays_for(seat)
        assert legal, f"no legal plays for seat {seat}"
        rnd.play_card(seat, legal[0])
        plays += 1

    assert rnd.phase is Phase.DONE
    assert plays == 9 * PLAYER_COUNT
    assert all(len(h) == 0 for h in rnd.hands)
    assert sum(len(w) for w in rnd.won_cards) == 36

    collected = rnd.collected()
    assert sum(collected) == MAX_POINTS
    penalties = rnd.penalties()
    assert len(penalties) == PLAYER_COUNT


def test_illegal_play_rejected():
    trump = 0
    hands = [
        [card(1, 4), card(2, 0), card(2, 1), card(2, 2),
         card(2, 3), card(2, 4), card(2, 5), card(2, 6), card(2, 7)],
        [card(1, 0), card(1, 1), card(2, 0), card(2, 1),
         card(2, 2), card(2, 3), card(2, 4), card(2, 5), card(2, 6)],
        [card(3, 0)] * 9,
        [card(1, 2), card(1, 3), card(1, 5), card(1, 6),
         card(1, 7), card(1, 8), card(3, 1), card(3, 2), card(3, 3)],
    ]
    rnd = create_round(hands, trump, leader=0)
    for seat in range(PLAYER_COUNT):
        rnd.submit_prediction(seat, 0)
    rnd.start_play()

    rnd.play_card(0, card(1, 4))  # lead Schilten
    with pytest.raises(ValueError):
        # seat 1 holds Schilten but tries an off-suit non-trump Rosen card
        rnd.play_card(1, card(2, 0))
