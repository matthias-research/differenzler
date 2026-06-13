"""Random legal-move bot."""

from __future__ import annotations

import random

from game.constants import MAX_POINTS
from players.base import Player
from players.observation import Observation


class RandomPlayer:
    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()

    def choose_prediction(self, obs: Observation) -> int:
        return self._rng.randint(0, MAX_POINTS)

    def choose_play(self, obs: Observation) -> int:
        if not obs.legal_plays:
            raise ValueError("no legal plays available")
        return self._rng.choice(obs.legal_plays)
