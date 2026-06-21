"""Modal dialog shown when a round ends."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from ui.layout import WINDOW_HEIGHT, WINDOW_WIDTH


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
        predicted: int,
        collected: int,
        difference: int,
    ) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        panel_w, panel_h = 440, 280
        panel = pygame.Rect(0, 0, panel_w, panel_h)
        panel.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self._panel_rect = panel

        pygame.draw.rect(screen, (28, 32, 28), panel, border_radius=16)
        pygame.draw.rect(screen, (90, 90, 90), panel, width=2, border_radius=16)

        title_font = pygame.font.SysFont("segoeui", 26, bold=True)
        title = title_font.render(f"Round {round_number} finished", True, (245, 245, 245))
        screen.blit(title, title.get_rect(midtop=(panel.centerx, panel.top + 24)))

        row_font = pygame.font.SysFont("segoeui", 22)
        rows = [
            ("Predicted", predicted),
            ("Collected", collected),
            ("Difference", difference),
        ]
        y = panel.top + 78
        for label, value in rows:
            label_surf = row_font.render(f"{label}:", True, (190, 190, 190))
            value_surf = row_font.render(str(value), True, (255, 255, 255))
            screen.blit(label_surf, (panel.left + 48, y))
            screen.blit(value_surf, value_surf.get_rect(midright=(panel.right - 48, y + 11)))
            y += 40

        ok_w, ok_h = 120, 44
        self._ok_rect = pygame.Rect(0, 0, ok_w, ok_h)
        self._ok_rect.midbottom = (panel.centerx, panel.bottom - 24)
        pygame.draw.rect(screen, (45, 120, 55), self._ok_rect, border_radius=10)
        ok_font = pygame.font.SysFont("segoeui", 22, bold=True)
        ok_label = ok_font.render("OK", True, (255, 255, 255))
        screen.blit(ok_label, ok_label.get_rect(center=self._ok_rect.center))
