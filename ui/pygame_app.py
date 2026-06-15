"""Playable Differenzler table — human vs three heuristic bots."""

from __future__ import annotations

import sys

import pygame

from game.constants import MAX_POINTS
from ui.assets import load_images
from ui.layout import TableLayout, card_id_at, draw_table
from ui.session import HUMAN_SEAT, PlaySession, UiPhase


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Differenzler")
    clock = pygame.time.Clock()
    images = load_images()

    session = PlaySession()
    layout = TableLayout()
    prediction_text = ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    if session.needs_human_prediction():
                        try:
                            value = int(prediction_text or "0")
                            if 0 <= value <= MAX_POINTS:
                                session.submit_prediction(value)
                                prediction_text = ""
                        except ValueError:
                            prediction_text = ""
                    elif session.ui_phase is UiPhase.ROUND_END:
                        session.acknowledge_round_end()
                    elif session.ui_phase is UiPhase.MATCH_END:
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    prediction_text = prediction_text[:-1]
                elif event.unicode.isdigit() and session.needs_human_prediction():
                    candidate = prediction_text + event.unicode
                    if int(candidate) <= MAX_POINTS:
                        prediction_text = candidate
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if session.needs_human_play():
                    card_id = card_id_at(layout, event.pos)
                    if card_id is not None and card_id in session.human_legal_plays():
                        session.submit_play(card_id)

        if session.tick():
            pygame.time.delay(280)

        score_left = session.human_collected_this_round()
        prediction = session.human_prediction()
        if prediction is not None:
            score_right = prediction
        elif session.needs_human_prediction() and prediction_text:
            score_right = int(prediction_text)
        else:
            score_right = 0

        draw_table(
            screen,
            images,
            layout,
            session.trump_farbe(),
            session.human_hand(),
            session.current_trick(),
            session.human_legal_plays() if session.needs_human_play() else [],
            score_left,
            score_right,
            session.status_line(prediction_text),
        )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def main() -> None:
    try:
        run()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
