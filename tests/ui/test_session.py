"""Tests for interactive play session."""

from __future__ import annotations

import random

from ui.session import PlaySession, UiPhase


def _play_human_turns(session: PlaySession) -> None:
    while session.ui_phase is UiPhase.PLAYING:
        if session.is_paused():
            session.acknowledge_pause()
            continue
        if session.needs_human_prediction():
            session.submit_prediction(0)
        elif session.needs_human_play():
            session.submit_play(session.human_legal_plays()[0])
        else:
            break


def test_session_completes_one_round():
    session = PlaySession(rng=random.Random(1))
    _play_human_turns(session)
    assert session.ui_phase in (UiPhase.ROUND_END, UiPhase.MATCH_END)


def test_session_completes_full_match():
    session = PlaySession(rng=random.Random(2))
    while session.ui_phase is not UiPhase.MATCH_END:
        if session.ui_phase is UiPhase.ROUND_END:
            session.acknowledge_round_end()
            continue
        _play_human_turns(session)
    assert len(session.round_penalty_history) == 8
