# Differenzler — Project Overview

Digital implementation of the Swiss card game **Differenzler** for four players.

The complete game rules are in **[GAME_RULES.md](./GAME_RULES.md)**. Treat that file as the source of truth for rules logic.

---

## Ultimate goal

Train a **neural network that plays Differenzler very well** — strong bidding and card play across eight-round matches.

Everything else (rules engine, heuristics, UI, logging, self-play) exists to support that goal.

---

## What we are building

A flexible four-seat card game where each seat can be any **player type**:

| Type | Role |
|------|------|
| **Human** | Real player (pygame UI) |
| **Random** | Random prediction 0–157; uniform random legal card |
| **Heuristic** | Simple rule-based bot (v1 opponent for human play) |
| **Neural** | PyTorch policy (training and strong play — later) |

**Default first milestone:** human at seat 0 vs three heuristic bots.

**Training configuration example:** four neural players in headless self-play (no UI).

Seat assignment is **configurable per match**, not hard-coded.

---

## Technology stack

| Layer | Choice | Purpose |
|-------|--------|---------|
| Language | **Python 3** | Single stack from rules to training |
| Game engine | Pure Python (`game/`) | Rules, legality, scoring — no UI/ML imports |
| Players | Python (`players/`) | Human, Random, Heuristic, Neural |
| Training | **PyTorch** (`training/`) | Self-play, RL, imitation — never imports pygame |
| Human UI | **Pygame** (`ui/`) | Table, sprite sheet, clicks — human matches only |
| Tests | **pytest** (`tests/`) | Rules correctness |

**Why Python:** PyTorch for the neural net, fast headless self-play, one language for engine + bots + training.

**Why pygame:** the card sprite sheet (4×9 grid) maps cleanly to rects; sufficient for v1 human play. Training runs without rendering for speed.

A web UI (React, etc.) could be added later; the engine and player interface stay UI-agnostic.

---

## Architecture

Strict separation of layers:

```
┌─────────────────────────────────────────────────────────┐
│  ui/          pygame — human visualization only         │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│  runner/      match loop, config, seat → player mapping  │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│  game/        pure rules engine (no pygame, no torch)   │
│               cards · deck · state · legal · tricks · score │
└───────────────────────────┬─────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
│ players/         │ │ training/    │ │ tests/           │
│ human            │ │ self-play    │ │ pytest           │
│ random           │ │ logging      │ │                  │
│ heuristic        │ │ PyTorch model│ │                  │
│ neural           │ │              │ │                  │
└──────────────────┘ └──────────────┘ └──────────────────┘
```

**Design principles:**

1. **`game/`** must not import pygame, PyTorch, or UI code.
2. **`training/`** must not import pygame (headless, maximum throughput).
3. **Players** implement one interface; the engine never branches on player type.
4. Each player receives only its **observation** (secret bids hidden from others until scoring).

---

## Player interface

All seat types implement the same protocol:

```python
class Player(Protocol):
    def choose_prediction(self, obs: Observation) -> int:
        """Return an integer 0–157 (secret until round scoring)."""

    def choose_play(self, obs: Observation) -> int:
        """Return a legal card ID 0–35."""
```

### Player types (behavior)

**Human** — pygame (or CLI debug) prompts for bid and card selection.

**Random** — `prediction ~ Uniform(0, 157)`; play ~ uniform over legal cards.

**Heuristic** — bidding: `(trump card values × 2) + 11 per non-trump Ace`; card play: random legal card for now

**Neural** — PyTorch model; masked softmax over legal bids/plays (design TBD). All three bot seats may share **one network** with identical or varied inference noise.

### Flexible match setup

Configuration drives seat assignment (YAML, CLI, or Python dict):

```yaml
# Default human play
seats: [human, heuristic, heuristic, heuristic]

# Sanity check
seats: [random, random, random, random]

# Self-play training
seats: [neural, neural, neural, neural]

# Mixed curriculum (future)
seats: [neural, neural, heuristic, random]
```

Example CLI (planned):

```bash
python -m ui.play --seats human,heuristic,heuristic,heuristic
python -m training.self_play --seats neural,neural,neural,neural --games 10000
```

---

## Path to a strong neural net

High-level plan; details (observation encoding, architecture, loss) to be decided later.

| Phase | What |
|-------|------|
| 1 | Correct engine + pytest; random vs random headless |
| 2 | Heuristic bots; playable human vs 3× heuristic |
| 3 | **Game logging** — `(observation, action, outcome)` trajectories |
| 4 | **Supervised warm-start** — imitate heuristic (and random) play |
| 5 | **Self-play RL** — reward = negative round/match penalty |
| 6 | **Curriculum** — e.g. neural vs heuristic → neural vs neural |

**Design notes for later:**

- **Bidding vs playing** may need two model heads (or two models): one shot before tricks vs nine sequential decisions with growing public state.
- **Legal move masking** is required: score all actions, zero illegal ones, then argmax/sample.
- **Information hiding** must be reflected in observations: no opponent hands; other players' bids hidden during the prediction phase.

---

## Milestones

| Step | Deliverable |
|------|-------------|
| **1** | Pure `game/` module + pytest (tricks, legal plays, scoring, 157 points) |
| **2** | `Player` protocol + Random + Heuristic |
| **3** | Config-driven match runner (headless, no UI) |
| **4** | Pygame UI — human + configurable opponents |
| **5** | Game logger + PyTorch project skeleton |
| **6** | Neural player + training loop |

**v1 done when:** you can play a full eight-round match against three heuristic bots in pygame.

**Ultimate done when:** neural self-play produces a bot that consistently beats heuristics.

---

## Planned directory layout

```
differenzler/
├── docs/
│   ├── GAME_RULES.md       ← authoritative rules
│   └── PROJECT.md          ← this file
├── assets/
│   └── cards/              ← sprite sheet (4 rows × 9 columns)
├── game/                   ← pure rules engine (no pygame/torch)
│   ├── cards.py
│   ├── deck.py
│   ├── state.py
│   ├── legal.py
│   ├── tricks.py
│   └── scoring.py
├── players/
│   ├── base.py             ← Player protocol
│   ├── human.py
│   ├── random_player.py
│   ├── heuristic.py
│   └── neural.py           ← later
├── runner/
│   └── match.py            ← config, game loop, seat wiring
├── ui/
│   └── pygame_app.py       ← human visualization
├── training/
│   ├── self_play.py
│   ├── model.py
│   └── train.py
├── tests/
│   └── game/
├── config/
│   └── default.yaml        ← e.g. seats: [human, heuristic, heuristic, heuristic]
├── pyproject.toml
└── requirements.txt
```

---

## Current state

| Asset / area        | Status                                  |
|---------------------|-----------------------------------------|
| Card sprite sheet   | Present (4 rows × 9 columns, one image) |
| Game rules          | Documented in `docs/GAME_RULES.md`      |
| Project plan        | This document                           |
| Game engine (`game/`) | **Done** (milestone 1)                |
| pytest suite        | **Done** (`tests/game/`)                |
| Player types        | **Partial** — random + heuristic (milestone 2) |
| pygame UI           | Not yet implemented (milestone 4)       |
| Neural net / PyTorch| Planned (milestones 5–6)                |

---

## Key implementation concepts

### Card IDs

Cards are integers **0–35**. See [GAME_RULES.md](./GAME_RULES.md) for Farben, ranks, trump strength, points, and sprite mapping.

### Phases (state machine)

```
MATCH_START
  └─ (repeat 8 times) ROUND:
       DEAL → CHOOSE_TRUMP → PREDICT (secret) → PLAY (9 tricks) → SCORE
  └─ MATCH_END
```

### Information hiding

- During **PREDICT**, each player submits a bid visible only to themselves and the engine; other players must not see it until scoring.
- During **PLAY**, each player sees its own hand and public table state — not opponents' hands.

### Seat numbering

| Seat | Default role | Screen position (pygame) |
|------|--------------|--------------------------|
| 0    | Human        | Bottom                   |
| 1    | Bot          | Right                    |
| 2    | Bot          | Top                      |
| 3    | Bot          | Left                     |

Counter-clockwise turn order: **0 → 1 → 2 → 3 → 0** — `(seat + 1) % 4`.

---

## Card rendering (pygame)

Single sprite sheet: **4 rows** (Farben 0–3) × **9 columns** (ranks 0–8).

```
x = (k % 9) * cell_width
y = (k // 9) * cell_height
```

Row order top-to-bottom: Schellen, Schilten, Rosen, Eicheln.

---

## Testing priorities

1. **Trump strength order** — Bauer beats Nell beats Ass …
2. **Trick winner** — trump beats lead suit; off-suit cards never win
3. **Legal plays** — follow suit or trump; Bauer-only exception
4. **Points** — trump vs non-trump tables; last-trick +5; total 157
5. **Scoring** — `abs(prediction - collected)`; eight-round sum
6. **Rotation** — random first leader in match round 1; CCW each subsequent round
7. **Headless sim** — millions of random vs random games without crash or rule violation

---

## For agents working on this repo

1. Read **`docs/GAME_RULES.md`** before changing rules logic.
2. Keep **`game/`** free of pygame, PyTorch, and UI imports.
3. Keep **`training/`** free of pygame — headless only.
4. Add new seat types by implementing **`Player`** in `players/` — do not embed bot logic in `game/`.
5. Match constants (`TRUMP_STRENGTH`, point arrays, `157`, etc.) to the rules document exactly.
6. Preserve **secret bids** and **information hiding** in observations.
7. Match setup must stay **configurable** (any combination of human / random / heuristic / neural per seat).

---

## Deferred decisions (neural net)

To be specified when milestone 5 begins:

- Observation vector layout (hand encoding, played cards, trump, trick context, bids)
- One vs two model heads (prediction vs play)
- Training algorithm (behavioral cloning → self-play policy gradient, etc.)
- Whether all four seats share weights during training

These do not block milestones 1–4.
