"""Deck creation, shuffling, and dealing."""

from __future__ import annotations

import random

from game.constants import CARDS_PER_PLAYER, CARD_COUNT, PLAYER_COUNT


def full_deck() -> list[int]:
    """Return a new deck as card IDs 0–35."""
    return list(range(CARD_COUNT))


def shuffle_deck(deck: list[int], rng: random.Random | None = None) -> list[int]:
    """Return a shuffled copy of deck."""
    shuffled = deck.copy()
    (rng or random).shuffle(shuffled)
    return shuffled


def deal(deck: list[int]) -> list[list[int]]:
    """
    Deal 9 cards to each of 4 players from a 36-card deck.

    Returns hands indexed by seat 0–3.
    """
    if len(deck) != CARD_COUNT:
        raise ValueError(f"deck must have {CARD_COUNT} cards, got {len(deck)}")
    hands: list[list[int]] = []
    for seat in range(PLAYER_COUNT):
        start = seat * CARDS_PER_PLAYER
        end = start + CARDS_PER_PLAYER
        hands.append(deck[start:end].copy())
    return hands
