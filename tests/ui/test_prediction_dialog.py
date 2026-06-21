"""Tests for prediction dialog logic."""

from __future__ import annotations

import pygame

from game.constants import MAX_POINTS
from ui.prediction_dialog import PredictionDialog


def test_confirm_empty_is_zero():
    dialog = PredictionDialog()
    assert dialog.confirm() == 0


def test_confirm_parses_value():
    dialog = PredictionDialog()
    dialog.text = "67"
    assert dialog.confirm() == 67


def test_append_digit_respects_max():
    dialog = PredictionDialog()
    for ch in "157":
        dialog.append_digit(ch)
    assert dialog.text == "157"
    dialog.append_digit("0")
    assert dialog.text == "157"


def test_handle_event_enter_confirms():
    pygame.init()
    dialog = PredictionDialog()
    dialog.text = "42"
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    assert dialog.handle_event(event) == 42
