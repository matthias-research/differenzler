"""Heuristic bot: trump×2 + side Aces bid; random legal card play (for now)."""

from __future__ import annotations

import random

from players.heuristic import heuristic_prediction
from players.observation import Observation
from players.random_player import RandomPlayer


class HeuristicPlayer:
    """
    Bidding uses the trump-value × 2 plus 11 per non-trump Ace rule.

    Card play is not yet heuristic; a uniform random legal card is chosen.
    """

    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng_player = RandomPlayer(rng)

    def choose_prediction(self, obs: Observation) -> int:
        return heuristic_prediction(list(obs.hand), obs.trump)

    def choose_play(self, obs: Observation) -> int:
        return self._rng_player.choose_play(obs)
