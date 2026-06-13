"""Trick winner resolution."""

from game.cards import card_strength, farbe, is_trump


def trick_winner(
    plays: list[tuple[int, int]],
    trump_farbe: int,
) -> int:
    """
    Determine the winning seat for a completed trick.

    plays: list of (seat, card_id) in play order; first entry is the lead.
    Returns the winning seat.
    """
    if not plays:
        raise ValueError("plays must not be empty")

    lead_farbe = farbe(plays[0][1])
    winner_seat, winner_card = plays[0]

    for seat, card_id in plays[1:]:
        if _beats(card_id, winner_card, lead_farbe, trump_farbe):
            winner_seat, winner_card = seat, card_id

    return winner_seat


def _beats(
    challenger: int,
    current: int,
    lead_farbe: int,
    trump_farbe: int,
) -> bool:
    challenger_trump = is_trump(challenger, trump_farbe)
    current_trump = is_trump(current, trump_farbe)

    if challenger_trump and not current_trump:
        return True
    if current_trump and not challenger_trump:
        return False

    challenger_eligible = challenger_trump or farbe(challenger) == lead_farbe
    current_eligible = current_trump or farbe(current) == lead_farbe

    if not challenger_eligible:
        return False
    if not current_eligible:
        return True

    if challenger_trump and current_trump:
        return card_strength(challenger, trump_farbe) > card_strength(
            current, trump_farbe
        )

    if farbe(challenger) == lead_farbe and farbe(current) == lead_farbe:
        return card_strength(challenger, trump_farbe) > card_strength(
            current, trump_farbe
        )

    return False
