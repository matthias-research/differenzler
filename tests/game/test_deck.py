"""Tests for deck and dealing."""

from game.constants import CARDS_PER_PLAYER, CARD_COUNT, PLAYER_COUNT
from game.deck import deal, full_deck, shuffle_deck


def test_full_deck():
    deck = full_deck()
    assert len(deck) == CARD_COUNT
    assert sorted(deck) == list(range(CARD_COUNT))


def test_shuffle_preserves_cards():
    deck = full_deck()
    shuffled = shuffle_deck(deck)
    assert sorted(shuffled) == sorted(deck)
    assert shuffled is not deck


def test_deal():
    deck = full_deck()
    hands = deal(deck)
    assert len(hands) == PLAYER_COUNT
    assert all(len(h) == CARDS_PER_PLAYER for h in hands)
    assert sorted(card for hand in hands for card in hand) == list(range(CARD_COUNT))
