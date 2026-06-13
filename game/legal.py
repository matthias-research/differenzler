"""Legal play computation."""

from __future__ import annotations

from game.cards import farbe, is_bauer, is_trump


def legal_plays(
    hand: list[int],
    lead_card: int | None,
    trump_farbe: int,
) -> list[int]:
    """
    Return sorted legal card IDs from hand.

    If lead_card is None, the player is leading and may play any card.
    """
    if not hand:
        return []

    if lead_card is None:
        return sorted(hand)

    lead_farbe = farbe(lead_card)
    cards_of_lead = [c for c in hand if farbe(c) == lead_farbe]
    trump_cards = [c for c in hand if is_trump(c, trump_farbe)]

    if lead_farbe == trump_farbe:
        if len(trump_cards) == 1 and is_bauer(trump_cards[0], trump_farbe):
            return sorted(hand)
        if trump_cards:
            return sorted(trump_cards)
        return sorted(hand)

    if cards_of_lead:
        legal = set(cards_of_lead) | set(trump_cards)
        return sorted(legal)

    return sorted(hand)
