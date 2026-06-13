"""Player protocol."""

from __future__ import annotations

from typing import Protocol

from players.observation import Observation


class Player(Protocol):
    def choose_prediction(self, obs: Observation) -> int:
        """Return a secret bid from 0 to 157."""

    def choose_play(self, obs: Observation) -> int:
        """Return a legal card ID 0–35."""
