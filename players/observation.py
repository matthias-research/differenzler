"""What one player is allowed to see when choosing an action."""

from __future__ import annotations

from dataclasses import dataclass, field

from game.state import Phase


@dataclass(frozen=True)
class Observation:
    seat: int
    hand: tuple[int, ...]
    trump: int
    phase: Phase
    legal_plays: tuple[int, ...] = ()
    trick_number: int = 0
    current_trick: tuple[tuple[int, int], ...] = field(default_factory=tuple)

    @classmethod
    def for_prediction(cls, seat: int, hand: list[int], trump: int) -> Observation:
        return cls(
            seat=seat,
            hand=tuple(hand),
            trump=trump,
            phase=Phase.PREDICT,
        )

    @classmethod
    def for_play(
        cls,
        seat: int,
        hand: list[int],
        trump: int,
        trick_number: int,
        current_trick: list[tuple[int, int]],
        legal_plays: list[int],
    ) -> Observation:
        return cls(
            seat=seat,
            hand=tuple(hand),
            trump=trump,
            phase=Phase.PLAY,
            legal_plays=tuple(legal_plays),
            trick_number=trick_number,
            current_trick=tuple(current_trick),
        )
