"""Tests for card encoding and attributes."""

import pytest

from game.cards import (
    card,
    card_points,
    card_strength,
    farbe,
    is_bauer,
    is_trump,
    rank,
    sort_hand,
)
from game.constants import POINTS_NON_TRUMP, POINTS_TRUMP, TRUMP_STRENGTH


@pytest.mark.parametrize(
    "farbe_id, rank_id, expected",
    [
        (0, 0, 0),
        (0, 8, 8),
        (1, 0, 9),
        (3, 8, 35),
    ],
)
def test_card_encoding(farbe_id, rank_id, expected):
    assert card(farbe_id, rank_id) == expected
    assert farbe(expected) == farbe_id
    assert rank(expected) == rank_id


def test_trump_strength_order():
    """Bauer > Nell > Ass within trump."""
    t = 2
    bauer = card(t, 5)
    nell = card(t, 3)
    ass = card(t, 8)
    six = card(t, 0)

    assert card_strength(bauer, t) > card_strength(nell, t)
    assert card_strength(nell, t) > card_strength(ass, t)
    assert card_strength(ass, t) > card_strength(six, t)


def test_trump_strength_matches_constants():
    t = 1
    for rank_id, strength in enumerate(TRUMP_STRENGTH):
        assert card_strength(card(t, rank_id), t) == strength


def test_non_trump_strength_is_rank():
    trump = 0
    for rank_id in range(9):
        c = card(2, rank_id)
        assert card_strength(c, trump) == rank_id


@pytest.mark.parametrize("rank_id", range(9))
def test_point_tables(rank_id):
    trump = 3
    trump_card = card(trump, rank_id)
    non_trump = card(1, rank_id)
    assert card_points(trump_card, trump) == POINTS_TRUMP[rank_id]
    assert card_points(non_trump, trump) == POINTS_NON_TRUMP[rank_id]


def test_bauer_detection():
    trump = 2
    assert is_bauer(card(trump, 5), trump)
    assert not is_bauer(card(trump, 3), trump)
    assert not is_bauer(card(1, 5), trump)


def test_is_trump():
    trump = 1
    assert is_trump(card(trump, 4), trump)
    assert not is_trump(card(2, 4), trump)


def test_sort_hand_trump_first_then_farbe_and_rank():
    trump = 2
    hand = [card(0, 8), card(2, 5), card(2, 0), card(1, 4), card(3, 1)]
    assert sort_hand(hand, trump) == [
        card(2, 0),
        card(2, 5),
        card(0, 8),
        card(1, 4),
        card(3, 1),
    ]
