"""Run full rounds and matches with configured players."""

from __future__ import annotations

import random
from dataclasses import dataclass

from game.constants import PLAYER_COUNT, ROUNDS_PER_MATCH
from game.deck import deal, full_deck, shuffle_deck
from game.scoring import match_penalties
from game.state import Phase, create_round, next_seat
from players.base import Player
from players.factory import PlayerType, make_players
from players.observation import Observation
from runner.stats import SimulationResult


@dataclass
class RoundResult:
    penalties: list[int]
    predictions: list[int]
    collected: list[int]
    trump: int
    first_leader: int


@dataclass
class MatchResult:
    round_results: list[RoundResult]
    match_penalties: list[int]


def run_round(
    players: list[Player],
    rng: random.Random,
    first_leader: int,
) -> RoundResult:
    deck = shuffle_deck(full_deck(), rng)
    hands = deal(deck)
    trump = rng.randint(0, 3)
    rnd = create_round(hands, trump, first_leader)

    for seat in range(PLAYER_COUNT):
        obs = Observation.for_prediction(seat, rnd.hands[seat], trump)
        prediction = players[seat].choose_prediction(obs)
        rnd.submit_prediction(seat, prediction)

    rnd.start_play()
    while rnd.phase is Phase.PLAY:
        seat = rnd.current_player()
        legal = rnd.legal_plays_for(seat)
        obs = Observation.for_play(
            seat,
            rnd.hands[seat],
            trump,
            rnd.trick_number,
            rnd.current_trick,
            legal,
        )
        card_id = players[seat].choose_play(obs)
        rnd.play_card(seat, card_id)

    predictions = [p if p is not None else 0 for p in rnd.predictions]
    return RoundResult(
        penalties=rnd.penalties(),
        predictions=predictions,
        collected=rnd.collected(),
        trump=trump,
        first_leader=first_leader,
    )


def run_match(
    players: list[Player],
    rng: random.Random | None = None,
    rounds: int = ROUNDS_PER_MATCH,
) -> MatchResult:
    if len(players) != PLAYER_COUNT:
        raise ValueError("players must have length 4")
    if rounds < 1:
        raise ValueError("rounds must be at least 1")

    shared_rng = rng or random.Random()
    round_results: list[RoundResult] = []
    first_leader = shared_rng.randint(0, PLAYER_COUNT - 1)

    for _ in range(rounds):
        result = run_round(players, shared_rng, first_leader)
        round_results.append(result)
        first_leader = next_seat(first_leader)

    penalty_lists = [r.penalties for r in round_results]
    return MatchResult(
        round_results=round_results,
        match_penalties=match_penalties(penalty_lists),
    )


def run_simulation(
    seat_types: list[PlayerType],
    rounds: int,
    rng: random.Random | None = None,
) -> SimulationResult:
    """Play ``rounds`` rounds with the given seat configuration."""
    if len(seat_types) != PLAYER_COUNT:
        raise ValueError("seat_types must have length 4")

    players = make_players(seat_types, rng)
    match = run_match(players, rng=rng, rounds=rounds)
    penalty_lists = [r.penalties for r in match.round_results]
    return SimulationResult.from_penalty_lists(list(seat_types), penalty_lists)
