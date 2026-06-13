# Differenzler

Swiss card game **Differenzler** for four players — rules engine, heuristic bots, and (planned) neural-network players.

## Documentation

- [Game rules](docs/GAME_RULES.md)
- [Project overview & roadmap](docs/PROJECT.md)

## Setup

```powershell
cd differenzler
pip install -e ".[dev]"
```

Requires **Python 3.9+**.

## Run simulations

Default: 2 random + 2 heuristic players, 1000 rounds:

```powershell
python -m runner.simulate
```

More rounds and fixed seed:

```powershell
python -m runner.simulate --rounds 10000 --seed 42
```

Custom seats (seats 0–3):

```powershell
python -m runner.simulate --rounds 5000 --seats random,random,heuristic,heuristic
```

## Tests

```powershell
python -m pytest tests -v
```

## Project layout

```
game/       Pure rules engine
players/    Random, heuristic (and later neural) bots
runner/     Match loop and headless simulation
docs/       Rules and architecture
assets/     Card sprite sheet
```
