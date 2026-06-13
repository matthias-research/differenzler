"""Tests for trick winner resolution."""

from game.cards import card
from game.tricks import trick_winner


def test_highest_lead_suit_wins_without_trump():
    trump = 0
    lead = card(2, 4)
    plays = [
        (0, lead),
        (1, card(2, 0)),
        (2, card(2, 8)),
        (3, card(1, 7)),
    ]
    assert trick_winner(plays, trump) == 2


def test_trump_beats_lead_suit():
    trump = 1
    lead = card(2, 8)
    plays = [
        (0, lead),
        (1, card(trump, 0)),
        (2, card(2, 4)),
        (3, card(3, 8)),
    ]
    assert trick_winner(plays, trump) == 1


def test_higher_trump_wins():
    trump = 3
    plays = [
        (0, card(trump, 0)),
        (1, card(trump, 8)),
        (2, card(trump, 3)),
        (3, card(trump, 5)),
    ]
    assert trick_winner(plays, trump) == 3  # Bauer


def test_off_suit_never_wins():
    trump = 0
    lead = card(2, 4)
    plays = [
        (0, lead),
        (1, card(1, 8)),
        (2, card(3, 8)),
        (3, card(2, 0)),
    ]
    assert trick_winner(plays, trump) == 0


def test_low_trump_beats_high_side_card():
    trump = 2
    lead = card(1, 8)
    plays = [
        (0, lead),
        (1, card(trump, 0)),
        (2, card(1, 4)),
        (3, card(3, 6)),
    ]
    assert trick_winner(plays, trump) == 1
