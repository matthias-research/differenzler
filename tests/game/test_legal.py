"""Tests for legal play rules."""

from game.cards import card
from game.legal import legal_plays


def test_lead_any_card():
    hand = [card(0, 0), card(1, 4), card(2, 8)]
    assert legal_plays(hand, None, trump_farbe=3) == sorted(hand)


def test_follow_suit_or_trump():
    trump = 2
    lead = card(1, 4)  # Schilten 10
    hand = [card(1, 0), card(1, 8), card(2, 3), card(trump, 0)]
    legal = legal_plays(hand, lead, trump)
    assert card(1, 0) in legal
    assert card(1, 8) in legal
    assert card(trump, 0) in legal
    assert card(2, 3) not in legal


def test_no_lead_color_any_card():
    trump = 0
    lead = card(2, 4)
    hand = [card(1, 1), card(3, 2), card(3, 8)]
    assert legal_plays(hand, lead, trump) == sorted(hand)


def test_trump_led_must_play_trump():
    trump = 1
    lead = card(trump, 2)
    hand = [card(trump, 0), card(trump, 8), card(2, 4)]
    legal = legal_plays(hand, lead, trump)
    assert legal == [card(trump, 0), card(trump, 8)]
    assert card(2, 4) not in legal


def test_bauer_exception_only_bauer():
    trump = 3
    lead = card(trump, 4)
    bauer = card(trump, 5)
    hand = [bauer, card(0, 1), card(2, 6)]
    assert legal_plays(hand, lead, trump) == sorted(hand)


def test_bauer_exception_not_when_other_trump():
    trump = 3
    lead = card(trump, 4)
    hand = [card(trump, 5), card(trump, 0), card(0, 1)]
    legal = legal_plays(hand, lead, trump)
    assert legal == [card(trump, 0), card(trump, 5)]
    assert card(0, 1) not in legal


def test_trump_led_no_trump_any_card():
    trump = 2
    lead = card(trump, 1)
    hand = [card(0, 3), card(1, 4), card(3, 8)]
    assert legal_plays(hand, lead, trump) == sorted(hand)
