# Differenzler — Game Rules

Authoritative rules for this implementation. When code and this document disagree, update the code to match this document unless the user explicitly changes the rules.

## Overview

**Differenzler** is a Swiss trick-taking card game for **four individual players**. Each round, players secretly predict how many card points they will collect, then play nine tricks. After each round, each player's penalty is the absolute difference between prediction and actual points collected. A **match** consists of **eight rounds**; the player with the **lowest total penalty** wins.

---

## Cards

### Deck

- **36 cards** = 4 Farben × 9 ranks
- All 36 cards are dealt each round (9 per player)

### Farben (suits)

| Value | Name     |
|-------|----------|
| 0     | Schellen |
| 1     | Schilten |
| 2     | Rosen    |
| 3     | Eicheln  |

### Ranks

| Value | Name   | Non-trump strength |
|-------|--------|--------------------|
| 0     | 6      | weakest            |
| 1     | 7      |                    |
| 2     | 8      |                    |
| 3     | 9      | Nell (trump only)  |
| 4     | 10     |                    |
| 5     | Under  | Bauer (trump only) |
| 6     | Ober   |                    |
| 7     | König  |                    |
| 8     | Ass    | strongest          |

### Internal card encoding

A card is an integer **0–35**:

```
farbe = floor(k / 9)   // 0–3
rank  = k % 9          // 0–8
k     = farbe * 9 + rank
```

### Trump

Exactly one Farbe **t** (0–3) is trump for each round. Trump is chosen **randomly** after the deal.

Trump-specific names:

- Rank 5 (Under) → **Bauer** (strongest trump)
- Rank 3 (9) → **Nell** (second-strongest trump)

---

## Match structure

| Parameter        | Value                          |
|------------------|--------------------------------|
| Players          | 4                              |
| Rounds per match | 8                              |
| Cards per player | 9 per round                    |
| Total points     | **157** per round (see below)  |
| Winner           | Lowest sum of round penalties  |

Between rounds: **shuffle**, **redeal**, choose a **new random trump**.

---

## Round phases

### 1. Deal

Shuffle the deck and deal 9 cards to each player.

### 2. Trump selection

Choose trump Farbe **t** uniformly at random (0–3).

### 3. Predictions

- **When:** After the deal, before the first trick
- **How:** All four players submit **simultaneously** and **secretly** (other players must not see a player's prediction)
- **Range:** Any integer from **0** to **157**

### 4. Play — nine tricks

See [Trick play](#trick-play), [Trick winner](#trick-winner), and [Legal plays](#legal-plays).

### 5. Scoring

Each player sums the point values of all cards they won in tricks. If a player won the **ninth (final) trick**, add **5 bonus points**.

```
round_penalty = abs(prediction - collected_points)
```

---

## First trick leader

| Match round | First leader                                      |
|-------------|---------------------------------------------------|
| Round 1     | Random player (seat 0–3)                          |
| Rounds 2–8  | Next player counter-clockwise from previous round |

Within a round, the **winner of each trick** leads the next trick.

---

## Player seats and turn order

Counter-clockwise play order (from the human player's perspective):

| Seat | Screen position | Plays after |
|------|-----------------|-------------|
| 0    | Bottom (human)  | —           |
| 1    | Right           | Seat 0      |
| 2    | Top             | Seat 1      |
| 3    | Left            | Seat 2      |

Turn order: **0 → 1 → 2 → 3 → 0**

When advancing counter-clockwise: `next_seat = (seat + 1) % 4`

---

## Trick play

1. The leader plays one card face-up (the **lead card**).
2. Each other player plays one card, in counter-clockwise order.
3. After four cards, determine the trick winner.
4. The winner collects the four cards and leads the next trick.
5. Repeat until all nine tricks are played.

---

## Trick winner

Let:

- **t** = trump Farbe
- **c** = Farbe of the lead card (first card played in the trick)

### Eligibility

Only cards of Farbe **t** or Farbe **c** can win the trick. Cards of any other Farbe **never win**, even if played legally.

### Comparison

1. **Any trump card beats any non-trump card.**
2. Among cards of the **same** Farbe, the card with **higher strength** wins.

### Strength within a Farbe

**Non-trump:** strength equals rank (0 weakest … 8 strongest).

**Trump:** ranks ordered by strength (weakest → strongest):

```
rank:     0,  1,  2,  4,  6,  7,  8,  3,  5
name:     6,  7,  8, 10, Ober, König, Ass, Nell, Bauer
```

Implementation lookup (strength level 0–8 for each rank):

```
TRUMP_STRENGTH = [0, 1, 2, 4, 6, 7, 8, 3, 5]  // indexed by rank
```

---

## Legal plays

Let **c** = Farbe of the lead card, **t** = trump Farbe.

| Situation                         | Legal plays                                              |
|-----------------------------------|----------------------------------------------------------|
| Leading the trick                 | Any card in hand                                         |
| Not leading — general             | Any **trump** card is always legal                       |
| Holds one or more cards of Farbe c | Must play a card of Farbe **c** **or** a trump card      |
| Holds no card of Farbe c          | Any card in hand                                         |

### Bauer exception

When the lead card is trump (**c = t**), a player whose **only** trump card is the **Bauer** (rank 5 of Farbe t) **is not required** to play it. They may play **any** card from their hand instead.

If the player holds the Bauer **and any other trump**, normal rules apply: they must play a trump card.

---

## Point values

Points depend on rank and whether the card's Farbe equals trump **t**.

Indexed by rank 0–8:

```
POINTS_TRUMP     = [0, 0, 0, 14, 10, 20, 3, 4, 11]
POINTS_NON_TRUMP = [0, 0, 0, 0, 10, 2, 3, 4, 11]
```

| Rank | Card        | Trump | Non-trump |
|------|-------------|-------|-----------|
| 0    | 6           | 0     | 0         |
| 1    | 7           | 0     | 0         |
| 2    | 8           | 0     | 0         |
| 3    | 9 / Nell    | 14    | 0         |
| 4    | 10          | 10    | 10        |
| 5    | Under/Bauer | 20    | 2         |
| 6    | Ober        | 3     | 3         |
| 7    | König       | 4     | 4         |
| 8    | Ass         | 11    | 11        |

### Last-trick bonus

The player who wins **trick 9** receives **+5 points** in addition to the card values in that trick.

Total points available per round: **157** (152 from cards + 5 last-trick bonus).

---

## Scoring summary

**Per round (per player):**

```
collected = sum(point values of won cards) + (5 if won trick 9 else 0)
penalty   = abs(prediction - collected)
```

**Per match (per player):**

```
match_score = sum of 8 round penalties
```

**Winner:** player with the **lowest** `match_score`.

---

## Card artwork (sprite sheet)

One image contains all 36 cards in a **4 × 9 grid**:

- **Rows** (top → bottom): Schellen, Schilten, Rosen, Eicheln (Farben 0–3)
- **Columns** (left → right): ranks 0–8 (6 through Ass)

Sprite rect for card `k`:

```
farbe = floor(k / 9)
rank  = k % 9
x = rank * (sheetWidth / 9)
y = farbe * (sheetHeight / 4)
```

---

## Implementation reference

These constants should live in the game core and match this document exactly:

```typescript
const FARBE_NAMES = ['Schellen', 'Schilten', 'Rosen', 'Eicheln'];
const RANK_NAMES  = ['6', '7', '8', '9', '10', 'Under', 'Ober', 'König', 'Ass'];

const TRUMP_STRENGTH     = [0, 1, 2, 4, 6, 7, 8, 3, 5];
const POINTS_TRUMP       = [0, 0, 0, 14, 10, 20, 3, 4, 11];
const POINTS_NON_TRUMP   = [0, 0, 0, 0, 10, 2, 3, 4, 11];

const LAST_TRICK_BONUS   = 5;
const MAX_POINTS         = 157;
const ROUNDS_PER_MATCH   = 8;
const CARDS_PER_PLAYER   = 9;
const PLAYER_COUNT       = 4;
```
