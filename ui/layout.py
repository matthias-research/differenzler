"""Table layout and drawing."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from ui.assets import card_sprite_rect, suit_sprite_rect

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

HAND_CARD_HEIGHT = 160
HAND_OVERLAP_STEP = 52
TRICK_CARD_HEIGHT = 148
TRUMP_ICON_HEIGHT = 44

CARPET_WIDTH_RATIO = 0.456  # 20% larger than 0.38
CARPET_TOP_MARGIN = 98
CARPET_HAND_GAP = 22
SCORE_BOX_TOP = 28

PLAYABLE_OUTLINE = (220, 45, 45)
TRICK_WINNER_OUTLINE = (255, 210, 60)

# Seat offsets from carpet center (fraction of carpet width/height).
TRICK_SEAT_OFFSET: dict[int, tuple[float, float]] = {
    0: (0.0, 0.14),   # bottom (human)
    1: (0.14, 0.0),   # right
    2: (0.0, -0.14),  # top
    3: (-0.14, 0.0),  # left
}


def scale_to_height(surface: pygame.Surface, height: int) -> pygame.Surface:
    if surface.get_height() == height:
        return surface
    width = int(surface.get_width() * height / surface.get_height())
    return pygame.transform.smoothscale(surface, (width, height))


@dataclass
class TableLayout:
    carpet_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))
    hand_hit_targets: list[tuple[int, pygame.Rect]] = field(default_factory=list)

    def compute_carpet_rect(self, carpet_src: pygame.Surface) -> pygame.Rect:
        hand_bottom = WINDOW_HEIGHT - 24
        hand_top = hand_bottom - HAND_CARD_HEIGHT
        max_bottom = hand_top - CARPET_HAND_GAP
        max_height = max_bottom - CARPET_TOP_MARGIN

        carpet_w = int(WINDOW_WIDTH * CARPET_WIDTH_RATIO)
        carpet_h = int(carpet_w * carpet_src.get_height() / carpet_src.get_width())

        if carpet_h > max_height:
            carpet_h = max_height
            carpet_w = int(carpet_h * carpet_src.get_width() / carpet_src.get_height())

        carpet_rect = pygame.Rect(0, 0, carpet_w, carpet_h)
        carpet_rect.midtop = (WINDOW_WIDTH // 2, CARPET_TOP_MARGIN)
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
    highlight_color: tuple[int, int, int] = PLAYABLE_OUTLINE,
    *,
    center: bool = False,
) -> pygame.Rect:
    src = card_sprite_rect(card_id, cards_sheet.get_width(), cards_sheet.get_height())
    image = cards_sheet.subsurface(src)
    width = int(image.get_width() * height / image.get_height())
    if center:
        dest = pygame.Rect(x - width // 2, y - height // 2, width, height)
    else:
        dest = pygame.Rect(x, y - height, width, height)
    scaled = pygame.transform.smoothscale(image, dest.size)
    screen.blit(scaled, dest)
    if highlight:
        pygame.draw.rect(screen, highlight_color, dest, width=3, border_radius=4)
    return dest


def trick_card_width(cards_sheet: pygame.Surface, height: int = TRICK_CARD_HEIGHT) -> int:
    src = card_sprite_rect(0, cards_sheet.get_width(), cards_sheet.get_height())
    return int(src.width * height / src.height)


def trick_card_center(
    carpet_rect: pygame.Rect,
    seat: int,
    *,
    card_width: int | None = None,
    card_height: int | None = None,
) -> tuple[int, int]:
    ox, oy = TRICK_SEAT_OFFSET[seat]
    cx = carpet_rect.centerx + int(carpet_rect.width * ox)
    cy = carpet_rect.centery + int(carpet_rect.height * oy)
    if card_width is not None:
        half = card_width // 2
        if seat == 1:
            cx += half
        elif seat == 3:
            cx -= half
    if card_height is not None:
        shift = int(card_height * 0.15)
        if seat == 2:
            cy -= shift
        elif seat == 0:
            cy += shift
    return cx, cy


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
    trick_winner_seat: int | None = None,
) -> None:
    table = pygame.transform.smoothscale(images["table"], (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(table, (0, 0))

    carpet_src = images["carpet"]
    carpet_rect = layout.compute_carpet_rect(carpet_src)
    carpet = pygame.transform.smoothscale(carpet_src, carpet_rect.size)
    screen.blit(carpet, carpet_rect)

    score_w, score_h = 120, 64
    draw_score_box(screen, pygame.Rect(36, SCORE_BOX_TOP, score_w, score_h), score_left)
    draw_score_box(
        screen, pygame.Rect(WINDOW_WIDTH - score_w - 36, SCORE_BOX_TOP, score_w, score_h), score_right
    )

    suits_sheet = images["suits"]
    suit_src = suit_sprite_rect(trump_farbe, suits_sheet.get_width(), suits_sheet.get_height())
    suit_img = suits_sheet.subsurface(suit_src)
    trump = scale_to_height(suit_img, TRUMP_ICON_HEIGHT)
    trump_rect = trump.get_rect(topright=(carpet_rect.right - 14, carpet_rect.top + 14))
    screen.blit(trump, trump_rect)

    cards_sheet = images["cards"]
    trick_card_w = trick_card_width(cards_sheet)
    for seat, card_id in trick:
        cx, cy = trick_card_center(
            carpet_rect, seat, card_width=trick_card_w, card_height=TRICK_CARD_HEIGHT
        )
        draw_card(
            screen,
            cards_sheet,
            card_id,
            cx,
            cy,
            TRICK_CARD_HEIGHT,
            center=True,
            highlight=seat == trick_winner_seat,
            highlight_color=TRICK_WINNER_OUTLINE,
        )

    legal_set = set(legal_plays)
    layout.hand_hit_targets.clear()
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
            highlight_color=PLAYABLE_OUTLINE,
        )
        layout.hand_hit_targets.append((card_id, rect))

    font = pygame.font.SysFont("segoeui", 22)
    status = font.render(status_line, True, (240, 240, 240))
    screen.blit(status, status.get_rect(midtop=(WINDOW_WIDTH // 2, carpet_rect.top + 24)))


def card_id_at(layout: TableLayout, pos: tuple[int, int]) -> int | None:
    for card_id, rect in reversed(layout.hand_hit_targets):
        if rect.collidepoint(pos):
            return card_id
    return None
