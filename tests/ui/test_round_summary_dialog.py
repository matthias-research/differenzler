"""Tests for round summary dialog."""

from __future__ import annotations

import pygame

from ui.round_summary_dialog import RoundSummaryDialog


def test_handle_event_enter_acknowledges():
    pygame.init()
    dialog = RoundSummaryDialog()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
    assert dialog.handle_event(event) is True


def test_handle_event_ignores_other_keys():
    pygame.init()
    dialog = RoundSummaryDialog()
    event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
    assert dialog.handle_event(event) is False
