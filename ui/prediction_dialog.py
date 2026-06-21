"""Modal dialog for entering round prediction."""

from __future__ import annotations

from dataclasses import dataclass, field

import pygame

from game.constants import MAX_POINTS
from ui.layout import WINDOW_HEIGHT, WINDOW_WIDTH


@dataclass
class PredictionDialog:
    text: str = ""
    _ok_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))
    _panel_rect: pygame.Rect = field(default_factory=lambda: pygame.Rect(0, 0, 0, 0))

    def reset(self) -> None:
        self.text = ""

    def append_digit(self, digit: str) -> None:
        candidate = self.text + digit
        if int(candidate) <= MAX_POINTS:
            self.text = candidate

    def confirm(self) -> int | None:
        value = int(self.text or "0")
        if 0 <= value <= MAX_POINTS:
            return value
        return None

    def handle_event(self, event: pygame.event.Event) -> int | None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self.confirm()
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.append_digit(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._ok_rect.collidepoint(event.pos):
                return self.confirm()
        return None

    def draw(self, screen: pygame.Surface) -> None:
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        panel_w, panel_h = 420, 220
        panel = pygame.Rect(0, 0, panel_w, panel_h)
        panel.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self._panel_rect = panel

        pygame.draw.rect(screen, (28, 32, 28), panel, border_radius=16)
        pygame.draw.rect(screen, (90, 90, 90), panel, width=2, border_radius=16)

        title_font = pygame.font.SysFont("segoeui", 26, bold=True)
        title = title_font.render("Your prediction", True, (245, 245, 245))
        screen.blit(title, title.get_rect(midtop=(panel.centerx, panel.top + 24)))

        hint_font = pygame.font.SysFont("segoeui", 18)
        hint = hint_font.render(
            f"Points you expect to collect (0–{MAX_POINTS})",
            True,
            (190, 190, 190),
        )
        screen.blit(hint, hint.get_rect(midtop=(panel.centerx, panel.top + 58)))

        field = pygame.Rect(panel.left + 40, panel.top + 96, panel.width - 80, 48)
        pygame.draw.rect(screen, (12, 12, 12), field, border_radius=8)
        pygame.draw.rect(screen, (100, 100, 100), field, width=2, border_radius=8)

        value_font = pygame.font.SysFont("segoeui", 32, bold=True)
        display = self.text or "0"
        value_surf = value_font.render(display, True, (255, 255, 255))
        screen.blit(value_surf, value_surf.get_rect(midleft=(field.left + 16, field.centery)))

        ok_w, ok_h = 120, 44
        self._ok_rect = pygame.Rect(0, 0, ok_w, ok_h)
        self._ok_rect.midbottom = (panel.centerx, panel.bottom - 24)
        pygame.draw.rect(screen, (45, 120, 55), self._ok_rect, border_radius=10)
        ok_font = pygame.font.SysFont("segoeui", 22, bold=True)
        ok_label = ok_font.render("OK", True, (255, 255, 255))
        screen.blit(ok_label, ok_label.get_rect(center=self._ok_rect.center))
