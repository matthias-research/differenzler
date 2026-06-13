"""Headless simulation CLI."""

from __future__ import annotations

import argparse
import random

from players.factory import PLAYER_TYPES, PlayerType
from runner.match import run_simulation

DEFAULT_SEATS: list[PlayerType] = ["random", "random", "heuristic", "heuristic"]


def parse_seats(value: str) -> list[PlayerType]:
    parts = [part.strip().lower() for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("seats must list exactly 4 player types")
    for part in parts:
        if part not in PLAYER_TYPES:
            raise argparse.ArgumentTypeError(
                f"unknown player type {part!r}; choose from {', '.join(PLAYER_TYPES)}"
            )
    return parts  # type: ignore[return-value]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run headless Differenzler simulations and report average penalties.",
    )
    parser.add_argument(
        "--rounds",
        "-n",
        type=int,
        default=1000,
        help="number of rounds to play (default: 1000)",
    )
    parser.add_argument(
        "--seats",
        type=parse_seats,
        default=DEFAULT_SEATS,
        help=(
            "comma-separated player types for seats 0–3 "
            f"(default: {','.join(DEFAULT_SEATS)})"
        ),
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="random seed for reproducible runs",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.rounds < 1:
        parser.error("--rounds must be at least 1")

    rng = random.Random(args.seed)
    result = run_simulation(args.seats, args.rounds, rng=rng)
    print(result.format_report())


if __name__ == "__main__":
    main()
