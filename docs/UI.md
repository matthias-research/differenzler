# Differenzler — UI (pygame)

Human play at seat 0 vs three heuristic bots. Rules engine in `game/`; `ui/session.py` drives rounds.

---

## Run

```powershell
pip install -e ".[ui]"
python -m ui.pygame_app
```

### Controls

| Action | Input |
|--------|--------|
| Prediction (0–157) | Type digits, **Enter** |
| Play a card | Click a **highlighted** card in your hand |
| Continue after a bot play | Click anywhere on the table (not needed when it is your turn) |
| Collect trick | Click once when all four cards are shown (winner highlighted) |
| Next round | **Enter** or **Space** on round summary |
| Quit | **ESC** (or after match ends) |

---

## Assets (`resources/`)

German set only (`-german` suffix).

| File | Purpose |
|------|---------|
| `table.png` | Full-screen background |
| `carpet.png` | Trick play area (upper center, above hand) |
| `cards-german.png` | 36 cards, 4×9 grid |
| `suits-german.png` | Trump icons, 1×4 row (Schellen … Eicheln) |

Sprite mapping: `ui/assets.py`. Layout constants: `ui/layout.py`.

---

## Scores (top boxes)

| Box | Meaning |
|-----|---------|
| Left | Points **collected this round** (updates as you win tricks) |
| Right | Your **prediction** for this round |

---

## Seat layout

| Seat | Role | Screen |
|------|------|--------|
| 0 | Human | Hand at bottom |
| 1–3 | Heuristic bots | Trick cards only (hands hidden) |

Trick cards on carpet use seat anchors: bottom / right / top / left.

---

## Code layout

| Module | Role |
|--------|------|
| `ui/session.py` | Match loop, bot turns, human input |
| `ui/layout.py` | Draw table, hit-testing for hand |
| `ui/pygame_app.py` | Event loop |
| `ui/assets.py` | Load bitmaps |

---

## Not implemented yet

- Opponent hand backs / counts at sides
- Deal animation, trick-win animation
- French assets
- `HumanPlayer` in `players/` (UI calls session directly)
