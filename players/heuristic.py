"""Heuristic prediction rule for Differenzler."""

from game.cards import card_points, is_trump, rank

ACE_RANK = 8
SIDE_ACE_POINTS = 11


def heuristic_prediction(hand: list[int], trump_farbe: int) -> int:
    """
    Predict collected points:

    (sum of trump card values × 2) + (11 per non-trump Ace).

    The trump Ace is counted only in the trump sum, not again as a side Ace.
    """
    trump_value = sum(
        card_points(card_id, trump_farbe)
        for card_id in hand
        if is_trump(card_id, trump_farbe)
    )
    side_aces = sum(
        1
        for card_id in hand
        if rank(card_id) == ACE_RANK and not is_trump(card_id, trump_farbe)
    )
    return trump_value * 2 + SIDE_ACE_POINTS * side_aces
