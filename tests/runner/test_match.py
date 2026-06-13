"""Tests for headless match runner."""

import random

from game.constants import ROUNDS_PER_MATCH
from players import make_players
from runner import run_match, run_round


def test_run_round_heuristic():
    players = make_players(["heuristic"] * 4, random.Random(1))
    result = run_round(players, random.Random(2), first_leader=0)
    assert len(result.penalties) == 4
    assert sum(result.predictions) == 157
    assert sum(result.collected) == 157


def test_run_match_heuristic():
    players = make_players(["heuristic"] * 4, random.Random(3))
    result = run_match(players, random.Random(4), rounds=ROUNDS_PER_MATCH)
    assert len(result.round_results) == ROUNDS_PER_MATCH
    assert len(result.match_penalties) == 4
    for round_result in result.round_results:
        assert sum(round_result.predictions) == 157
