"""Table layout and drawing."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from ui.assets import card_sprite_rect, suit_sprite_rect

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

HAND_CARD_HEIGHT = 168
HAND_OVERLAP_STEP = 52
TRICK_CARD_HEIGHT = 152
TRUMP_ICON_HEIGHT = 48

CARPET_WIDTH_RATIO = 0.46
CARPET_CENTER_Y = 310
CARPET_HAND_GAP = 36

# Trick card anchor on carpet (normalized x, y within carpet rect).
TRICK_SEAT_NORM: dict[int, tuple[float, float]] = {
    0: (0.50, 0.64),
    1: (0.74, 0.50),
    2: (0.50, 0.36),
    3: (0.26, 0.50),
}


def scale_to_height(surface: pygame.Surface, height: int) -> pygame.Surface:
    if surface.get_height() == height:
        return surface
    width = int(surface.get_width() * height / surface.get_height())
    return pygame.transform.smoothscale(surface, (width, height))


@dataclass
class TableLayout:
    carpet_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))
    hand_card_rects: dict[int, pygame.Rect] = field(default_factory=dict)

    def compute_carpet_rect(self) -> pygame.Rect:
        hand_bottom = WINDOW_HEIGHT - 24
        hand_top = hand_bottom - HAND_CARD_HEIGHT
        max_carpet_bottom = hand_top - CARPET_HAND_GAP
        carpet_w = int(WINDOW_WIDTH * CARPET_WIDTH_RATIO)
        # Height filled in draw when carpet image is known.
        carpet_rect = pygame.Rect(0, 0, carpet_w, carpet_w)
        carpet_rect.center = (WINDOW_WIDTH // 2, CARPET_CENTER_Y)
        if carpet_rect.bottom > max_carpet_bottom:
            carpet_rect.bottom = max_carpet_bottom
        self.carpet_rect = carpet_rect
        return carpet_rect


def draw_card(
    screen: pygame.Surface,
    cards_sheet: pygame.Surface,
    card_id: int,
    x: int,
    y: int,
    height: int,
    highlight: bool = False,
) -> pygame.Rect:
    src = card_sprite_rect(card_id, cards_sheet.get_width(), cards_sheet.get_height())
    image = cards_sheet.subsurface(src)
    width = int(image.get_width() * height / image.get_height())
    scaled = pygame.transform.smoothscale(image, (width, height))
    dest = pygame.Rect(x, y - height, width, height)
    screen.blit(scaled, dest)
    if highlight:
        pygame.draw.rect(screen, (255, 220, 80), dest, width=3, border_radius=4)
    return dest


def draw_score_box(screen: pygame.Surface, rect: pygame.Rect, value: int) -> None:
    pygame.draw.rect(screen, (18, 18, 18), rect, border_radius=14)
    pygame.draw.rect(screen, (70, 70, 70), rect, width=2, border_radius=14)
    font = pygame.font.SysFont("segoeui", 42, bold=True)
    label = font.render(str(value), True, (245, 245, 245))
    screen.blit(label, label.get_rect(center=rect.center))


def draw_table(
    screen: pygame.Surface,
    images: dict[str, pygame.Surface],
    layout: TableLayout,
    trump_farbe: int,
    human_hand: list[int],
    trick: list[tuple[int, int]],
    legal_plays: list[int],
    score_left: int,
    score_right: int,
    status_line: str,
) -> None:
    table = pygame.transform.smoothscale(images["table"], (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(table, (0, 0))

    carpet_src = images["carpet"]
    carpet_w = int(WINDOW_WIDTH * CARPET_WIDTH_RATIO)
    carpet_h = int(carpet_w * carpet_src.get_height() / carpet_src.get_width())
    carpet = pygame.transform.smoothscale(carpet_src, (carpet_w, carpet_h))
    carpet_rect = layout.compute_carpet_rect()
    carpet_rect.size = (carpet_w, carpet_h)
    carpet_rect.center = layout.carpet_rect.center
    if carpet_rect.bottom > layout.carpet_rect.bottom:
        carpet_rect.bottom = layout.carpet_rect.bottom
    layout.carpet_rect = carpet_rect
    screen.blit(carpet, carpet_rect)

    score_w, score_h = 120, 64
    draw_score_box(screen, pygame.Rect(36, 28, score_w, score_h), score_left)
    draw_score_box(screen, pygame.Rect(WINDOW_WIDTH - score_w - 36, 28, score_w, score_h), score_right)

    suits_sheet = images["suits"]
    suit_src = suit_sprite_rect(trump_farbe, suits_sheet.get_width(), suits_sheet.get_height())
    suit_img = suits_sheet.subsurface(suit_src)
    trump = scale_to_height(suit_img, TRUMP_ICON_HEIGHT)
    trump_rect = trump.get_rect(topright=(carpet_rect.right - 16, carpet_rect.top + 16))
    screen.blit(trump, trump_rect)

    cards_sheet = images["cards"]
    for seat, card_id in trick:
        fx, fy = TRICK_SEAT_NORM[seat]
        cx = carpet_rect.left + int(carpet_rect.width * fx)
        cy = carpet_rect.top + int(carpet_rect.height * fy)
        draw_card(screen, cards_sheet, card_id, cx, cy, TRICK_CARD_HEIGHT)

    legal_set = set(legal_plays)
    layout.hand_card_rects.clear()
    overlap_step = HAND_OVERLAP_STEP
    hand_width = HAND_CARD_HEIGHT * 9 / 13 + overlap_step * (max(len(human_hand), 1) - 1)
    hand_left = int((WINDOW_WIDTH - hand_width) / 2)
    hand_bottom = WINDOW_HEIGHT - 24
    for index, card_id in enumerate(human_hand):
        x = hand_left + index * overlap_step
        rect = draw_card(
            screen,
            cards_sheet,
            card_id,
            x,
            hand_bottom,
            HAND_CARD_HEIGHT,
            highlight=bool(legal_set) and card_id in legal_set,
        )
        layout.hand_card_rects[card_id] = rect

    font = pygame.font.SysFont("segoeui", 22)
    status = font.render(status_line, True, (240, 240, 240))
    screen.blit(status, status.get_rect(midtop=(WINDOW_WIDTH // 2, 100)))


def card_id_at(layout: TableLayout, pos: tuple[int, int]) -> int | None:
    for card_id, rect in layout.hand_card_rects.items():
        if rect.collidepoint(pos):
            return card_id
    return None
