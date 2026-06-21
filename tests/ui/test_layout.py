"""Tests for hand card hit testing."""

from __future__ import annotations

import pygame

from ui.layout import TableLayout, card_id_at


def test_card_id_at_prefers_topmost_overlapping_card():
    layout = TableLayout()
    layout.hand_hit_targets = [
        (10, pygame.Rect(100, 500, 120, 160)),
        (20, pygame.Rect(152, 500, 120, 160)),
    ]
    assert card_id_at(layout, (170, 560)) == 20
    assert card_id_at(layout, (110, 560)) == 10


def test_card_id_at_returns_none_outside_hand():
    layout = TableLayout()
    layout.hand_hit_targets = [(10, pygame.Rect(100, 500, 120, 160))]
    assert card_id_at(layout, (0, 0)) is None
