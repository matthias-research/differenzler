"""Card encoding and per-card attributes."""

from game.constants import (
    FARBE_COUNT,
    POINTS_NON_TRUMP,
    POINTS_TRUMP,
    RANK_COUNT,
    TRUMP_STRENGTH,
)

FARBE_NAMES = ("Schellen", "Schilten", "Rosen", "Eicheln")
RANK_NAMES = ("6", "7", "8", "9", "10", "Under", "Ober", "König", "Ass")


def farbe(card_id: int) -> int:
    """Return Farbe 0–3 for card_id 0–35."""
    return card_id // RANK_COUNT


def rank(card_id: int) -> int:
    """Return rank 0–8 for card_id 0–35."""
    return card_id % RANK_COUNT


def card(farbe_id: int, rank_id: int) -> int:
    """Build card_id from Farbe and rank."""
    if not 0 <= farbe_id < FARBE_COUNT:
        raise ValueError(f"farbe must be 0–3, got {farbe_id}")
    if not 0 <= rank_id < RANK_COUNT:
        raise ValueError(f"rank must be 0–8, got {rank_id}")
    return farbe_id * RANK_COUNT + rank_id


def is_trump(card_id: int, trump_farbe: int) -> bool:
    return farbe(card_id) == trump_farbe


def is_bauer(card_id: int, trump_farbe: int) -> bool:
    """True if card is the Bauer (Under of trump Farbe)."""
    return farbe(card_id) == trump_farbe and rank(card_id) == 5


def card_strength(card_id: int, trump_farbe: int) -> int:
    """Return strength 0–8 (higher wins within the same Farbe)."""
    card_rank = rank(card_id)
    if is_trump(card_id, trump_farbe):
        return TRUMP_STRENGTH[card_rank]
    return card_rank


def card_points(card_id: int, trump_farbe: int) -> int:
    """Return point value of a card for the given trump Farbe."""
    card_rank = rank(card_id)
    if is_trump(card_id, trump_farbe):
        return POINTS_TRUMP[card_rank]
    return POINTS_NON_TRUMP[card_rank]


def sort_hand(hand: list[int], trump_farbe: int) -> list[int]:
    """Sort for display: trump Farbe first, then other Farben 0–3, ranks low to high."""

    def key(card_id: int) -> tuple[int, int, int]:
        f = farbe(card_id)
        return (0 if f == trump_farbe else 1, f, rank(card_id))

    return sorted(hand, key=key)
