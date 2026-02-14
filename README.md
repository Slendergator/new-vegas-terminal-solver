# Fallout: New Vegas Terminal Hacking Solver

Python CLI that solves the Fallout: New Vegas terminal hacking mini-game by using likeness scores and a minimax strategy to find the password in fewer guesses.

## How it works

- **Likeness**: The game reports how many letter positions match between your guess and the password. This solver uses that feedback to eliminate impossible candidates.
- **Minimax guess selection**: For each guess, it picks the word that minimizes the worst-case number of remaining candidates, so you reach the answer faster.

## Requirements

- Python 3.10+
- [rich](https://github.com/Textualize/rich) (Console, Prompt)

## Installation

```bash
pip install rich
```

## Usage

1. Run the solver:

   ```bash
   python new_vegas_solver.py
   ```

2. Paste the words from the in-game terminal when prompted (comma-separated).
3. Enter the **likeness** score after each guess (how many letters matched in position), or type `correct` when you've unlocked the terminal.

## Example

```
Fallout: New Vegas — Terminal hacking solver
Paste the words from the terminal (comma-separated).

Enter all words separated by a comma: RATHER, HARDER, FATHER, BARBER, RIPPER, DOLLAR
Optimal guess: FATHER (reduces search space best)
How many letters were correct (likeness)? (or type 'correct') 2
Possible words remaining: 3
Optimal guess: RATHER (reduces search space best)
How many letters were correct (likeness)? (or type 'correct') correct
Terminal unlocked! The word was RATHER.
```
