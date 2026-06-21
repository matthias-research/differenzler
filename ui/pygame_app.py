"""Playable Differenzler table — human vs three heuristic bots."""

from __future__ import annotations

import sys

import pygame

from ui.assets import load_images
from ui.layout import TableLayout, card_id_at, draw_table
from ui.prediction_dialog import PredictionDialog
from ui.round_summary_dialog import RoundSummaryDialog
from ui.session import PlaySession, UiPhase


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Differenzler")
    clock = pygame.time.Clock()
    images = load_images()

    session = PlaySession()
    layout = TableLayout()
    prediction_dialog = PredictionDialog()
    round_summary_dialog = RoundSummaryDialog()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if session.needs_human_prediction():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    continue
                confirmed = prediction_dialog.handle_event(event)
                if confirmed is not None:
                    session.submit_prediction(confirmed)
                    prediction_dialog.reset()
                continue

            if session.ui_phase is UiPhase.ROUND_END:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    continue
                if round_summary_dialog.handle_event(event):
                    session.acknowledge_round_end()
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN and session.ui_phase is UiPhase.MATCH_END:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if session.is_paused():
                    session.acknowledge_pause()
                elif session.needs_human_play():
                    card_id = card_id_at(layout, event.pos)
                    if card_id is not None and card_id in session.human_legal_plays():
                        session.submit_play(card_id)

        score_left = session.human_collected_this_round()
        prediction = session.human_prediction()
        if prediction is not None:
            score_right = prediction
        elif session.needs_human_prediction() and prediction_dialog.text:
            score_right = int(prediction_dialog.text)
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
            session.status_line(),
            session.trick_winner_seat(),
        )
        if session.needs_human_prediction():
            prediction_dialog.draw(screen)
        elif summary := session.human_round_summary():
            round_number, predicted, collected, difference = summary
            round_summary_dialog.draw(
                screen, round_number, predicted, collected, difference
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
