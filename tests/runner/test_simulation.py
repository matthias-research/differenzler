"""Tests for simulation statistics."""

import random

from players.factory import PlayerType
from runner.match import run_simulation
from runner.stats import SimulationResult


def test_simulation_result_averages():
    penalty_lists = [
        [10, 20, 30, 40],
        [6, 14, 34, 36],
    ]
    result = SimulationResult.from_penalty_lists(
        ["random", "heuristic", "random", "heuristic"],
        penalty_lists,
    )
    assert result.rounds == 2
    assert result.total_penalties == [16, 34, 64, 76]
    assert result.average_penalties == [8.0, 17.0, 32.0, 38.0]
    assert result.average_by_type()["random"] == 20.0
    assert result.average_by_type()["heuristic"] == 27.5


def test_run_simulation_mixed_players():
    seats: list[PlayerType] = ["random", "random", "heuristic", "heuristic"]
    result = run_simulation(seats, rounds=50, rng=random.Random(0))
    assert result.rounds == 50
    assert len(result.average_penalties) == 4
    assert all(avg >= 0 for avg in result.average_penalties)
