"""Interactive human vs heuristic match for the pygame UI."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum, auto

from game.constants import MAX_POINTS, PLAYER_COUNT, ROUNDS_PER_MATCH
from game.deck import deal, full_deck, shuffle_deck
from game.scoring import collected_points, match_penalties
from game.cards import sort_hand
from game.state import Phase, RoundState, create_round, next_seat
from players.heuristic_player import HeuristicPlayer
from players.observation import Observation

HUMAN_SEAT = 0


class UiPhase(Enum):
    PLAYING = auto()
    ROUND_END = auto()
    MATCH_END = auto()


class PauseReason(Enum):
    NONE = auto()
    AFTER_PLAY = auto()
    BEFORE_TRICK_CLEAR = auto()


@dataclass
class PlaySession:
    """Human at seat 0; seats 1–3 are heuristic bots."""

    rng: random.Random = field(default_factory=random.Random)
    round_state: RoundState | None = None
    round_index: int = 0
    first_leader: int = 0
    round_penalty_history: list[list[int]] = field(default_factory=list)
    match_penalties: list[int] = field(default_factory=lambda: [0, 0, 0, 0])
    ui_phase: UiPhase = UiPhase.PLAYING
    last_round_penalties: list[int] = field(default_factory=lambda: [0, 0, 0, 0])
    last_round_collected: list[int] = field(default_factory=lambda: [0, 0, 0, 0])
    _bots: list[HeuristicPlayer] = field(default_factory=list)
    pause: PauseReason = PauseReason.NONE
    display_trick: list[tuple[int, int]] = field(default_factory=list)
    _trick_awaiting_clear: bool = False

    def __post_init__(self) -> None:
        self._bots = [HeuristicPlayer(self.rng) for _ in range(PLAYER_COUNT - 1)]
        self.first_leader = self.rng.randint(0, PLAYER_COUNT - 1)
        self._start_new_round()
        self._advance_bots()

    def _start_new_round(self) -> None:
        deck = shuffle_deck(full_deck(), self.rng)
        hands = deal(deck)
        trump = self.rng.randint(0, 3)
        self.round_state = create_round(hands, trump, self.first_leader)
        self.display_trick = []
        self.pause = PauseReason.NONE
        self._trick_awaiting_clear = False

    def _next_prediction_seat(self) -> int | None:
        rnd = self.round_state
        if rnd is None:
            return None
        for seat in range(PLAYER_COUNT):
            if rnd.predictions[seat] is None:
                return seat
        return None

    def _bot_for_seat(self, seat: int) -> HeuristicPlayer:
        return self._bots[seat - 1]

    def _bot_predict(self, seat: int) -> None:
        rnd = self.round_state
        if rnd is None:
            return
        obs = Observation.for_prediction(seat, rnd.hands[seat], rnd.trump)
        value = self._bot_for_seat(seat).choose_prediction(obs)
        rnd.submit_prediction(seat, value)

    def _bot_play(self, seat: int) -> None:
        rnd = self.round_state
        if rnd is None:
            return
        legal = rnd.legal_plays_for(seat)
        obs = Observation.for_play(
            seat,
            rnd.hands[seat],
            rnd.trump,
            rnd.trick_number,
            rnd.current_trick,
            legal,
        )
        card_id = self._bot_for_seat(seat).choose_play(obs)
        self._play_card(seat, card_id)

    def _play_card(self, seat: int, card_id: int) -> None:
        rnd = self.round_state
        if rnd is None:
            return
        completing = len(rnd.current_trick) == PLAYER_COUNT - 1
        if completing:
            self.display_trick = list(rnd.current_trick) + [(seat, card_id)]
        rnd.play_card(seat, card_id)
        if completing:
            self._trick_awaiting_clear = True
            self.pause = PauseReason.BEFORE_TRICK_CLEAR
        else:
            self.display_trick = list(rnd.current_trick)
            if self._human_is_next_to_play():
                self.pause = PauseReason.NONE
            else:
                self.pause = PauseReason.AFTER_PLAY

    def _human_is_next_to_play(self) -> bool:
        rnd = self.round_state
        return rnd is not None and rnd.phase is Phase.PLAY and rnd.current_player() == HUMAN_SEAT

    def _finish_round(self) -> None:
        rnd = self.round_state
        if rnd is None or rnd.phase is not Phase.DONE:
            return
        penalties = rnd.penalties()
        collected = rnd.collected()
        self.last_round_penalties = penalties
        self.last_round_collected = collected
        self.round_penalty_history.append(penalties)
        self.match_penalties = match_penalties(self.round_penalty_history)
        self.round_index += 1
        if self.round_index >= ROUNDS_PER_MATCH:
            self.ui_phase = UiPhase.MATCH_END
        else:
            self.ui_phase = UiPhase.ROUND_END

    def _advance_bots(self) -> None:
        while self.ui_phase is UiPhase.PLAYING and self.pause is PauseReason.NONE:
            rnd = self.round_state
            if rnd is None:
                return

            if rnd.phase is Phase.PREDICT:
                seat = self._next_prediction_seat()
                if seat is None:
                    rnd.start_play()
                    continue
                if seat == HUMAN_SEAT:
                    return
                self._bot_predict(seat)
                continue

            if rnd.phase is Phase.PLAY:
                seat = rnd.current_player()
                if seat == HUMAN_SEAT:
                    return
                self._bot_play(seat)
                return

            if rnd.phase is Phase.DONE:
                self._finish_round()
                return

    def is_paused(self) -> bool:
        return self.pause is not PauseReason.NONE

    def acknowledge_pause(self) -> None:
        if self.pause is PauseReason.NONE:
            return
        self.display_trick = []
        self._trick_awaiting_clear = False
        self.pause = PauseReason.NONE
        rnd = self.round_state
        if rnd is not None and rnd.phase is Phase.DONE:
            self._finish_round()
            return
        self._advance_bots()

    def needs_human_prediction(self) -> bool:
        rnd = self.round_state
        if rnd is None or rnd.phase is not Phase.PREDICT:
            return False
        return self._next_prediction_seat() == HUMAN_SEAT

    def needs_human_play(self) -> bool:
        if self.is_paused():
            return False
        rnd = self.round_state
        if rnd is None or rnd.phase is not Phase.PLAY:
            return False
        return rnd.current_player() == HUMAN_SEAT

    def submit_prediction(self, value: int) -> None:
        if not self.needs_human_prediction():
            raise ValueError("not waiting for human prediction")
        rnd = self.round_state
        if rnd is None:
            raise ValueError("no active round")
        rnd.submit_prediction(HUMAN_SEAT, value)
        self._advance_bots()

    def submit_play(self, card_id: int) -> None:
        if not self.needs_human_play():
            raise ValueError("not waiting for human play")
        rnd = self.round_state
        if rnd is None:
            raise ValueError("no active round")
        self._play_card(HUMAN_SEAT, card_id)

    def acknowledge_round_end(self) -> None:
        if self.ui_phase is not UiPhase.ROUND_END:
            return
        self.ui_phase = UiPhase.PLAYING
        self.first_leader = next_seat(self.first_leader)
        self._start_new_round()
        self._advance_bots()

    def human_hand(self) -> list[int]:
        rnd = self.round_state
        if rnd is None:
            return []
        return sort_hand(list(rnd.hands[HUMAN_SEAT]), rnd.trump)

    def human_legal_plays(self) -> list[int]:
        rnd = self.round_state
        if rnd is None:
            return []
        return rnd.legal_plays_for(HUMAN_SEAT)

    def current_trick(self) -> list[tuple[int, int]]:
        if self.display_trick:
            return list(self.display_trick)
        rnd = self.round_state
        if rnd is None:
            return []
        return list(rnd.current_trick)

    def trick_winner_seat(self) -> int | None:
        if self.pause is not PauseReason.BEFORE_TRICK_CLEAR:
            return None
        rnd = self.round_state
        if rnd is None:
            return None
        return rnd.last_trick_winner

    def trump_farbe(self) -> int:
        rnd = self.round_state
        return rnd.trump if rnd is not None else 0

    def human_collected_this_round(self) -> int:
        rnd = self.round_state
        if rnd is None:
            return 0
        won_last = rnd.phase is Phase.DONE and rnd.last_trick_winner == HUMAN_SEAT
        return collected_points(rnd.won_cards[HUMAN_SEAT], rnd.trump, won_last_trick=won_last)

    def human_prediction(self) -> int | None:
        rnd = self.round_state
        if rnd is None:
            return None
        return rnd.predictions[HUMAN_SEAT]

    def best_opponent_match_penalty(self) -> int:
        opponents = [self.match_penalties[s] for s in range(1, PLAYER_COUNT)]
        return min(opponents) if opponents else 0

    def status_line(self, prediction_text: str) -> str:
        if self.ui_phase is UiPhase.MATCH_END:
            winner = min(range(PLAYER_COUNT), key=lambda s: self.match_penalties[s])
            if winner == HUMAN_SEAT:
                return f"Match over — you win! Penalty {self.match_penalties[HUMAN_SEAT]} (Space to quit)"
            return (
                f"Match over — seat {winner} wins. Your penalty "
                f"{self.match_penalties[HUMAN_SEAT]} (Space to quit)"
            )

        if self.ui_phase is UiPhase.ROUND_END:
            return (
                f"Round {self.round_index}: penalty {self.last_round_penalties[HUMAN_SEAT]} "
                f"(collected {self.last_round_collected[HUMAN_SEAT]}) — Space for next round"
            )

        rnd = self.round_state
        if rnd is None:
            return ""

        if self.needs_human_prediction():
            text = prediction_text or "0"
            return f"Your prediction (0–{MAX_POINTS}): {text} — Enter to confirm"

        if self.needs_human_play():
            return f"Trick {rnd.trick_number}/9 — click a highlighted card"

        if self.pause is PauseReason.BEFORE_TRICK_CLEAR:
            return f"Trick {rnd.trick_number}/9 complete — click to collect"

        if self.pause is PauseReason.AFTER_PLAY:
            return f"Trick {rnd.trick_number}/9 — click to continue"

        return f"Round {self.round_index + 1}/{ROUNDS_PER_MATCH} — trick {rnd.trick_number}/9"
