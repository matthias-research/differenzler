"""Modal dialog shown when a round ends."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from ui.layout import WINDOW_HEIGHT, WINDOW_WIDTH


@dataclass(frozen=True)
class PlayerRoundResult:
    name: str
    predicted: int
    collected: int
    difference: int
    total: int


@dataclass
class RoundSummaryDialog:
    _ok_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))
    _panel_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._ok_rect.collidepoint(event.pos):
                return True
        return False

    def draw(
        self,
        screen: pygame.Surface,
        round_number: int,
        players: list[PlayerRoundResult],
    ) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        panel_w, panel_h = 580, 340
        panel = pygame.Rect(0, 0, panel_w, panel_h)
        panel.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self._panel_rect = panel

        pygame.draw.rect(screen, (28, 32, 28), panel, border_radius=16)
        pygame.draw.rect(screen, (90, 90, 90), panel, width=2, border_radius=16)

        title_font = pygame.font.SysFont("segoeui", 26, bold=True)
        title = title_font.render(f"Round {round_number} finished", True, (245, 245, 245))
        screen.blit(title, title.get_rect(midtop=(panel.centerx, panel.top + 20)))

        header_font = pygame.font.SysFont("segoeui", 17, bold=True)
        row_font = pygame.font.SysFont("segoeui", 19)

        col_name = panel.left + 24
        col_pred = panel.left + 168
        col_coll = panel.left + 262
        col_diff = panel.left + 368
        col_total = panel.right - 24

        header_y = panel.top + 64
        for label, x in (
            ("Predicted", col_pred),
            ("Collected", col_coll),
            ("Difference", col_diff),
            ("Total", col_total),
        ):
            surf = header_font.render(label, True, (160, 160, 160))
            screen.blit(surf, surf.get_rect(midright=(x, header_y)))

        y = panel.top + 98
        for player in players:
            name_color = (255, 255, 255) if player.name == "You" else (210, 210, 210)
            name_surf = row_font.render(player.name, True, name_color)
            screen.blit(name_surf, (col_name, y))

            for value, x in (
                (player.predicted, col_pred),
                (player.collected, col_coll),
                (player.difference, col_diff),
                (player.total, col_total),
            ):
                value_surf = row_font.render(str(value), True, (245, 245, 245))
                screen.blit(value_surf, value_surf.get_rect(midright=(x, y + 10)))

            y += 36

        ok_w, ok_h = 120, 44
        self._ok_rect = pygame.Rect(0, 0, ok_w, ok_h)
        self._ok_rect.midbottom = (panel.centerx, panel.bottom - 20)
        pygame.draw.rect(screen, (45, 120, 55), self._ok_rect, border_radius=10)
        ok_font = pygame.font.SysFont("segoeui", 22, bold=True)
        ok_label = ok_font.render("OK", True, (255, 255, 255))
        screen.blit(ok_label, ok_label.get_rect(center=self._ok_rect.center))
