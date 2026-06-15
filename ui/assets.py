"""Load German UI bitmaps from resources/."""

from __future__ import annotations

from pathlib import Path

import pygame

RESOURCES_DIR = Path(__file__).resolve().parent.parent / "resources"

CARDS_GERMAN = RESOURCES_DIR / "cards-german.png"
SUITS_GERMAN = RESOURCES_DIR / "suits-german.png"
TABLE = RESOURCES_DIR / "table.png"
CARPET = RESOURCES_DIR / "carpet.png"

RANKS_PER_ROW = 9
FARBEN_COUNT = 4
SUITS_PER_ROW = 4


def card_sprite_rect(card_id: int, sheet_width: int, sheet_height: int) -> pygame.Rect:
    """Sprite rect for card_id 0–35 on cards-german.png (4 rows × 9 columns)."""
    farbe_id = card_id // RANKS_PER_ROW
    rank_id = card_id % RANKS_PER_ROW
    cell_w = sheet_width / RANKS_PER_ROW
    cell_h = sheet_height / FARBEN_COUNT
    return pygame.Rect(int(rank_id * cell_w), int(farbe_id * cell_h), int(cell_w), int(cell_h))


def suit_sprite_rect(farbe_id: int, sheet_width: int, sheet_height: int) -> pygame.Rect:
    """Sprite rect for trump Farbe 0–3 on suits-german.png (1×4 row: Schellen … Eicheln)."""
    cell_w = sheet_width / SUITS_PER_ROW
    return pygame.Rect(int(farbe_id * cell_w), 0, int(cell_w), sheet_height)


def load_images() -> dict[str, pygame.Surface]:
    missing = [p for p in (CARDS_GERMAN, SUITS_GERMAN, TABLE, CARPET) if not p.is_file()]
    if missing:
        raise FileNotFoundError("Missing UI assets: " + ", ".join(str(p) for p in missing))

    if pygame.display.get_surface() is None:
        pygame.display.set_mode((1, 1))

    return {
        "cards": pygame.image.load(CARDS_GERMAN).convert_alpha(),
        "suits": pygame.image.load(SUITS_GERMAN).convert_alpha(),
        "table": pygame.image.load(TABLE).convert(),
        "carpet": pygame.image.load(CARPET).convert_alpha(),
    }
