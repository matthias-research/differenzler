"""Tests for scoring."""

from game.cards import card, card_points
from game.constants import LAST_TRICK_BONUS, MAX_POINTS, TOTAL_CARD_POINTS
from game.deck import full_deck
from game.scoring import (
    collected_points,
    match_penalties,
    round_penalties,
    sum_card_points,
)


def test_total_card_points_is_152():
    for trump in range(4):
        deck = full_deck()
        total = sum_card_points(deck, trump)
        assert total == TOTAL_CARD_POINTS


def test_max_points_with_last_trick_bonus():
    assert TOTAL_CARD_POINTS + LAST_TRICK_BONUS == MAX_POINTS


def test_collected_points_last_trick_bonus():
    trump = 1
    cards = [card(0, 4), card(2, 8)]
    base = sum_card_points(cards, trump)
    assert collected_points(cards, trump, won_last_trick=False) == base
    assert collected_points(cards, trump, won_last_trick=True) == base + LAST_TRICK_BONUS


def test_round_penalties():
    predictions = [80, 40, 60, 77]
    collected = [72, 45, 60, 80]
    assert round_penalties(predictions, collected) == [8, 5, 0, 3]


def test_match_penalties():
    rounds = [
        [8, 5, 0, 3],
        [10, 2, 4, 1],
    ]
    assert match_penalties(rounds) == [18, 7, 4, 4]


def test_bauer_and_nell_points_in_trump():
    trump = 2
    assert card_points(card(trump, 5), trump) == 20
    assert card_points(card(trump, 3), trump) == 14
