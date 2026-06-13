"""Create players from type names."""

from __future__ import annotations

import random
from typing import Literal

from players.base import Player
from players.heuristic_player import HeuristicPlayer
from players.random_player import RandomPlayer

PlayerType = Literal["random", "heuristic"]

PLAYER_TYPES = ("random", "heuristic")


def make_player(player_type: PlayerType, rng: random.Random | None = None) -> Player:
    if player_type == "random":
        return RandomPlayer(rng)
    if player_type == "heuristic":
        return HeuristicPlayer(rng)
    raise ValueError(f"unknown player type: {player_type!r}")


def make_players(
    seat_types: list[PlayerType],
    rng: random.Random | None = None,
) -> list[Player]:
    if len(seat_types) != 4:
        raise ValueError("seat_types must have length 4")
    shared_rng = rng or random.Random()
    return [make_player(t, shared_rng) for t in seat_types]
