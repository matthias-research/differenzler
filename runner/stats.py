"""Simulation statistics over many rounds."""

from __future__ import annotations

from dataclasses import dataclass

from game.constants import PLAYER_COUNT


@dataclass
class SimulationResult:
    seat_types: list[str]
    rounds: int
    total_penalties: list[int]
    average_penalties: list[float]

    @classmethod
    def from_penalty_lists(
        cls,
        seat_types: list[str],
        penalty_lists: list[list[int]],
    ) -> SimulationResult:
        rounds = len(penalty_lists)
        totals = [0] * PLAYER_COUNT
        for penalties in penalty_lists:
            for seat in range(PLAYER_COUNT):
                totals[seat] += penalties[seat]
        averages = [total / rounds for total in totals] if rounds else [0.0] * PLAYER_COUNT
        return cls(
            seat_types=seat_types,
            rounds=rounds,
            total_penalties=totals,
            average_penalties=averages,
        )

    def average_by_type(self) -> dict[str, float]:
        """Mean average penalty grouped by player type."""
        buckets: dict[str, list[float]] = {}
        for seat, player_type in enumerate(self.seat_types):
            buckets.setdefault(player_type, []).append(self.average_penalties[seat])
        return {
            player_type: sum(values) / len(values)
            for player_type, values in buckets.items()
        }

    def format_report(self) -> str:
        lines = [f"Rounds played: {self.rounds}", "", "Per seat:"]
        for seat, player_type in enumerate(self.seat_types):
            avg = self.average_penalties[seat]
            total = self.total_penalties[seat]
            lines.append(
                f"  Seat {seat} ({player_type:9s}): "
                f"avg penalty {avg:7.2f}  (total {total})"
            )

        by_type = self.average_by_type()
        if len(by_type) > 1:
            lines.extend(["", "By player type:"])
            for player_type in sorted(by_type):
                lines.append(f"  {player_type:9s}: avg penalty {by_type[player_type]:7.2f}")

        return "\n".join(lines)
