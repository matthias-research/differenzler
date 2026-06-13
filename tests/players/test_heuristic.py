"""Tests for heuristic prediction."""

from game.cards import card
from game.constants import MAX_POINTS
from game.deck import deal, full_deck
from players.heuristic import heuristic_prediction


def test_trump_only_hand():
    trump = 2
    hand = [card(trump, 5), card(trump, 3), card(trump, 0)]  # Bauer, Nell, 6
    # (20 + 14 + 0) * 2 = 68
    assert heuristic_prediction(hand, trump) == 68


def test_side_aces_only():
    trump = 0
    hand = [card(1, 8), card(2, 8), card(3, 8)]
    assert heuristic_prediction(hand, trump) == 33


def test_trump_ace_not_double_counted():
    trump = 1
    hand = [card(trump, 8), card(2, 8)]
    # trump ace: 11 * 2 = 22, one side ace: 11 -> 33
    assert heuristic_prediction(hand, trump) == 33


def test_all_four_predictions_sum_to_157():
    trump = 3
    hands = deal(full_deck())
    total = sum(heuristic_prediction(hand, trump) for hand in hands)
    assert total == MAX_POINTS


def test_all_four_predictions_sum_to_157_any_trump():
    hands = deal(full_deck())
    for trump in range(4):
        total = sum(heuristic_prediction(hand, trump) for hand in hands)
        assert total == MAX_POINTS
