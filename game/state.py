"""Round state machine for a single round of Differenzler."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from game.cards import farbe
from game.constants import CARDS_PER_PLAYER, MAX_POINTS, PLAYER_COUNT
from game.legal import legal_plays
from game.scoring import collected_points, round_penalties
from game.tricks import trick_winner


class Phase(Enum):
    PREDICT = auto()
    PLAY = auto()
    DONE = auto()


def next_seat(seat: int) -> int:
    """Advance counter-clockwise."""
    return (seat + 1) % PLAYER_COUNT


@dataclass
class RoundState:
    """Mutable state for one round after deal and trump selection."""

    hands: list[list[int]]
    trump: int
    leader: int
    predictions: list[int | None] = field(default_factory=lambda: [None] * PLAYER_COUNT)
    phase: Phase = Phase.PREDICT
    trick_number: int = 0
    current_trick: list[tuple[int, int]] = field(default_factory=list)
    won_cards: list[list[int]] = field(default_factory=lambda: [[] for _ in range(PLAYER_COUNT)])
    last_trick_winner: int | None = None

    def all_predictions_in(self) -> bool:
        return all(p is not None for p in self.predictions)

    def submit_prediction(self, seat: int, value: int) -> None:
        if self.phase is not Phase.PREDICT:
            raise ValueError("predictions are only allowed in PREDICT phase")
        if not 0 <= value <= MAX_POINTS:
            raise ValueError(f"prediction must be 0–{MAX_POINTS}, got {value}")
        if self.predictions[seat] is not None:
            raise ValueError(f"seat {seat} already predicted")
        self.predictions[seat] = value

    def start_play(self) -> None:
        if not self.all_predictions_in():
            raise ValueError("all players must predict before play")
        self.phase = Phase.PLAY
        self.trick_number = 1

    def current_player(self) -> int:
        if self.phase is not Phase.PLAY:
            raise ValueError("no current player outside PLAY phase")
        if not self.current_trick:
            return self.leader
        last_seat = self.current_trick[-1][0]
        return next_seat(last_seat)

    def legal_plays_for(self, seat: int) -> list[int]:
        if self.phase is not Phase.PLAY:
            return []
        if seat != self.current_player():
            return []
        hand = self.hands[seat]
        lead_card = self.current_trick[0][1] if self.current_trick else None
        return legal_plays(hand, lead_card, self.trump)

    def play_card(self, seat: int, card_id: int) -> None:
        if self.phase is not Phase.PLAY:
            raise ValueError("can only play cards in PLAY phase")
        if seat != self.current_player():
            raise ValueError(f"not seat {seat}'s turn")
        if card_id not in self.hands[seat]:
            raise ValueError(f"card {card_id} not in hand of seat {seat}")

        legal = self.legal_plays_for(seat)
        if card_id not in legal:
            raise ValueError(f"card {card_id} is not a legal play")

        self.hands[seat].remove(card_id)
        self.current_trick.append((seat, card_id))

        if len(self.current_trick) == PLAYER_COUNT:
            self._finish_trick()

    def _finish_trick(self) -> None:
        winner = trick_winner(self.current_trick, self.trump)
        for _, card_id in self.current_trick:
            self.won_cards[winner].append(card_id)

        self.last_trick_winner = winner
        self.leader = winner
        self.current_trick = []

        if self.trick_number == CARDS_PER_PLAYER:
            self.phase = Phase.DONE
        else:
            self.trick_number += 1

    def collected(self) -> list[int]:
        """Points collected per seat; only valid when round is DONE."""
        return [
            collected_points(
                self.won_cards[seat],
                self.trump,
                won_last_trick=(self.last_trick_winner == seat),
            )
            for seat in range(PLAYER_COUNT)
        ]

    def penalties(self) -> list[int]:
        """Round penalties; only valid when round is DONE."""
        if self.phase is not Phase.DONE:
            raise ValueError("round is not finished")
        predictions = [p if p is not None else 0 for p in self.predictions]
        return round_penalties(predictions, self.collected())


def create_round(
    hands: list[list[int]],
    trump: int,
    leader: int,
) -> RoundState:
    """Create a round in PREDICT phase from dealt hands."""
    if len(hands) != PLAYER_COUNT:
        raise ValueError("hands must have length 4")
    for seat, hand in enumerate(hands):
        if len(hand) != CARDS_PER_PLAYER:
            raise ValueError(f"seat {seat} must have {CARDS_PER_PLAYER} cards")
    if not 0 <= trump <= 3:
        raise ValueError("trump must be 0–3")
    if not 0 <= leader <= 3:
        raise ValueError("leader must be 0–3")

    return RoundState(
        hands=[hand.copy() for hand in hands],
        trump=trump,
        leader=leader,
    )
