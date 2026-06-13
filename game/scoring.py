"""Round and match scoring."""

from game.cards import card_points
from game.constants import LAST_TRICK_BONUS, PLAYER_COUNT


def sum_card_points(cards: list[int], trump_farbe: int) -> int:
    """Sum point values of cards for the given trump Farbe."""
    return sum(card_points(c, trump_farbe) for c in cards)


def collected_points(
    won_cards: list[int],
    trump_farbe: int,
    won_last_trick: bool,
) -> int:
    """Total points collected including last-trick bonus."""
    total = sum_card_points(won_cards, trump_farbe)
    if won_last_trick:
        total += LAST_TRICK_BONUS
    return total


def round_penalties(
    predictions: list[int],
    collected: list[int],
) -> list[int]:
    """Return per-seat round penalty |prediction - collected|."""
    if len(predictions) != PLAYER_COUNT or len(collected) != PLAYER_COUNT:
        raise ValueError("predictions and collected must have length 4")
    return [abs(p - c) for p, c in zip(predictions, collected)]


def match_penalties(round_penalty_lists: list[list[int]]) -> list[int]:
    """Sum round penalties across all rounds for each seat."""
    if not round_penalty_lists:
        return [0] * PLAYER_COUNT
    totals = [0] * PLAYER_COUNT
    for round_penalties_list in round_penalty_lists:
        if len(round_penalties_list) != PLAYER_COUNT:
            raise ValueError("each round penalty list must have length 4")
        for seat in range(PLAYER_COUNT):
            totals[seat] += round_penalties_list[seat]
    return totals
