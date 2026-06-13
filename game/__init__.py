"""Pure Differenzler rules engine (no UI or ML dependencies)."""

from game.cards import (
    FARBE_NAMES,
    RANK_NAMES,
    card,
    card_points,
    card_strength,
    farbe,
    is_bauer,
    is_trump,
    rank,
)
from game.constants import (
    CARDS_PER_PLAYER,
    LAST_TRICK_BONUS,
    MAX_POINTS,
    PLAYER_COUNT,
    ROUNDS_PER_MATCH,
    TOTAL_CARD_POINTS,
)
from game.deck import deal, full_deck, shuffle_deck
from game.legal import legal_plays
from game.scoring import (
    collected_points,
    match_penalties,
    round_penalties,
    sum_card_points,
)
from game.state import Phase, RoundState, create_round
from game.tricks import trick_winner

__all__ = [
    "CARDS_PER_PLAYER",
    "FARBE_NAMES",
    "LAST_TRICK_BONUS",
    "MAX_POINTS",
    "PLAYER_COUNT",
    "RANK_NAMES",
    "ROUNDS_PER_MATCH",
    "TOTAL_CARD_POINTS",
    "Phase",
    "RoundState",
    "card",
    "card_points",
    "card_strength",
    "collected_points",
    "create_round",
    "deal",
    "farbe",
    "full_deck",
    "is_bauer",
    "is_trump",
    "legal_plays",
    "match_penalties",
    "rank",
    "round_penalties",
    "shuffle_deck",
    "sum_card_points",
    "trick_winner",
]
