"""Fallout: New Vegas terminal hacking solver. Uses likeness (letter-position matches) to narrow the word list."""

from collections import Counter
from rich.console import Console
from rich.prompt import Prompt

CONFIRMED_MESSAGE = "correct"


def likeness(word_a: str, word_b: str) -> int:
    """Return the number of positions where the two words have the same letter."""
    return sum(1 for a, b in zip(word_a, word_b) if a == b)


def max_remaining_after_guess(candidate: str, words: list[str]) -> int:
    """For a candidate guess, return the maximum number of words that could remain for any likeness score."""
    score_counts: Counter[int] = Counter()
    for target in words:
        if candidate == target:
            continue
        score_counts[likeness(candidate, target)] += 1
    return max(score_counts.values()) if score_counts else 0


def find_best_guess(words: list[str]) -> str:
    """Pick the word that minimizes the worst-case number of remaining words."""
    if len(words) <= 2:
        return words[0]

    best_word = words[0]
    min_max_remaining = len(words)

    for candidate in words:
        worst = max_remaining_after_guess(candidate, words)
        if worst < min_max_remaining:
            min_max_remaining = worst
            best_word = candidate

    return best_word


def parse_feedback(text: str, word_length: int) -> int | None:
    """Parse user feedback: 'correct' or a number. Returns None if invalid."""
    if text.strip().lower() == CONFIRMED_MESSAGE:
        return word_length
    try:
        value = int(text.strip())
        if 0 <= value <= word_length:
            return value
    except ValueError:
        pass
    return None


def filter_by_feedback(words: list[str], guess: str, likeness_score: int) -> list[str]:
    """Keep only words that would give this likeness score for the given guess."""
    return [w for w in words if likeness(guess, w) == likeness_score and w != guess]


def run(console: Console) -> None:
    """Main loop: prompt for words from the New Vegas terminal, then guess and narrow the list."""
    console.print("[bold]Fallout: New Vegas[/bold] — Terminal hacking solver")
    console.print("Paste the words from the terminal (comma-separated).\n")
    raw = Prompt.ask("Enter all words separated by a comma")
    words = [w.strip().upper() for w in raw.split(",") if w.strip()]

    if not words:
        console.print("No words provided.")
        return

    word_length = len(words[0])
    if any(len(w) != word_length for w in words):
        console.print("All words must have the same length.")
        return

    while len(words) > 1:
        guess = find_best_guess(words)
        console.print(f"Optimal guess: [bold cyan]{guess}[/bold cyan] (reduces search space best)")

        feedback_str = Prompt.ask("How many letters were correct (likeness)? (or type 'correct')")
        feedback = parse_feedback(feedback_str, word_length)

        if feedback is None:
            console.print("Please enter a valid number or 'correct'.")
            continue

        if feedback == word_length:
            console.print(f"[bold green]Terminal unlocked![/bold green] The word was [bold green]{guess}[/bold green].")
            return

        words = filter_by_feedback(words, guess, feedback)

        if not words:
            console.print("No matching words left. Check your input or the likeness score.")
            return

        console.print(f"Possible words remaining: {len(words)}")

    if words:
        console.print(f"[bold green]Terminal unlocked![/bold green] The word was: [bold green]{words[0]}[/bold green]")
    else:
        console.print("No words found.")


def main() -> None:
    run(Console())


if __name__ == "__main__":
    main()
