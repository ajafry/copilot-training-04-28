"""Hangman game engine — because someone has to save the stick figure.

'Do. Or do not. There is no try.' — Yoda, The Empire Strikes Back
(Unfortunately, in Hangman there IS a 'try' and it might kill you.)

Contains the word bank, ASCII gallows art, and HangmanGame state class.
All the logic that keeps our poor stick figure's head attached to their body.
"""

import random
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Constants — no magic numbers; even the Elder Wand has rules
# ---------------------------------------------------------------------------
MAX_WRONG_GUESSES: int = 6          # One more and it's game over, Ned Stark
HINT_TRIGGER_WRONG_COUNT: int = 3   # "Help me, Obi-Wan" threshold
BLANK_CHAR: str = "_"
WIN_MESSAGE: str = "🎉 YOU WIN! As Borat would say: 'Great success!'"
LOSE_MESSAGE: str = "💀 GAME OVER. 'You know nothing, Jon Snow.'"

# ---------------------------------------------------------------------------
# Word bank — 30+ pop-culture themed words, because plain words are boring
# As Tyrion Lannister said: "A mind needs books like a sword needs a whetstone."
# ---------------------------------------------------------------------------
THE_MULTIVERSE_OF_WORDS: list[str] = [
    # Harry Potter universe
    "quidditch",
    "patronus",
    "horcrux",
    "hogwarts",
    "dumbledore",
    "expelliarmus",
    "lumos",
    "basilisk",
    "niffler",
    # Lord of the Rings / The Hobbit
    "mordor",
    "mithril",
    "gollum",
    "balrog",
    "hobbit",
    "gandalf",
    "excalibur",
    # Star Wars
    "lightsaber",
    "holodeck",
    "wookiee",
    "padawan",
    # Marvel / DC
    "vibranium",
    "kryptonite",
    "wakanda",
    "thanos",
    # Sci-Fi
    "delorean",
    "xenomorph",
    "skywalker",
    "tardis",
    # Game of Thrones
    "targaryen",
    "winterfell",
    "dothraki",
    # Video Games / Misc
    "zelda",
    "pokemon",
    "pikachu",
    "endgame",
]

# ---------------------------------------------------------------------------
# ASCII art gallows — 7 stages of increasingly bad news
# Stage 0: pristine gallows (hope remains)
# Stage 6: full stick figure (hope has left the chat)
# "Every picture tells a story. This one tells a tragedy." — Anonymous
# ---------------------------------------------------------------------------
GALLOWS_STAGES: list[str] = [
    # Stage 0 — "Nothing to see here." — Officer Barbrady, South Park
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",

    # Stage 1 — The head appears. "Oh no." — Kevin McCallister, Home Alone
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",

    # Stage 2 — Body joins the party. Uninvited.
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",

    # Stage 3 — Left arm. "I didn't sign up for this." — every left arm
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",

    # Stage 4 — Both arms. T-pose achieved. Very intimidating.
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",

    # Stage 5 — Left leg. "Run, Forrest, RUN!" — Mrs. Gump
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",

    # Stage 6 — Full figure. "It's over, Anakin." — Obi-Wan Kenobi
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


# ---------------------------------------------------------------------------
# Game state — like the Sorting Hat, it knows everything about you
# ---------------------------------------------------------------------------
@dataclass
class HangmanGame:
    """Encapsulates all state for a single Hangman game session.

    'Every game is a story. Let's make this one a good one.' — Anonymous
    (Though given the premise, 'survival story' is more accurate.)
    """

    word: str = field(default_factory=str)
    correct_guesses: set[str] = field(default_factory=set)
    wrong_guesses: list[str] = field(default_factory=list)
    hint_letter: str | None = field(default=None)

    def __post_init__(self) -> None:
        """Validate the word — 'One does not simply pick an empty word.' — Boromir."""
        if not self.word:
            raise ValueError("A Hangman game must have a word. Even Voldemort had a name.")

    # -----------------------------------------------------------------------
    # Derived properties — computed on demand like Doctor Strange's portals
    # -----------------------------------------------------------------------
    @property
    def display_word(self) -> str:
        """Return the word with unguessed letters hidden as blanks.

        'What is hidden will eventually be revealed.' — Albus Dumbledore (paraphrased)
        """
        return " ".join(
            letter if letter in self.correct_guesses else BLANK_CHAR
            for letter in self.word
        )

    @property
    def wrong_count(self) -> int:
        """Return the number of incorrect guesses made so far."""
        return len(self.wrong_guesses)

    @property
    def current_stage(self) -> int:
        """Return the current gallows stage index (0–6).

        Clamped to MAX_WRONG_GUESSES so we don't accidentally invent stage 7.
        """
        return min(self.wrong_count, MAX_WRONG_GUESSES)

    @property
    def gallows_art(self) -> str:
        """Return the ASCII art for the current gallows stage."""
        return GALLOWS_STAGES[self.current_stage]

    @property
    def is_won(self) -> bool:
        """Return True if all letters in the word have been guessed correctly."""
        return all(letter in self.correct_guesses for letter in self.word)

    @property
    def is_lost(self) -> bool:
        """Return True if the player has exceeded the maximum wrong guesses."""
        return self.wrong_count >= MAX_WRONG_GUESSES

    @property
    def is_over(self) -> bool:
        """Return True if the game has ended — win or loss."""
        return self.is_won or self.is_lost

    @property
    def hint_available(self) -> bool:
        """Return True if a hint can be triggered.

        Unlocks after HINT_TRIGGER_WRONG_COUNT wrong guesses, but only once per game.
        'You get one shot. Do not miss your chance to blow.' — Eminem, Lose Yourself
        """
        return (
            self.wrong_count >= HINT_TRIGGER_WRONG_COUNT
            and self.hint_letter is None
            and not self.is_over
        )

    @property
    def all_guesses(self) -> set[str]:
        """Return the union of all guessed letters (correct + wrong)."""
        return self.correct_guesses | set(self.wrong_guesses)

    # -----------------------------------------------------------------------
    # Actions — "With great power comes great responsibility." — Uncle Ben
    # -----------------------------------------------------------------------
    def guess(self, letter: str) -> bool:
        """Process a single letter guess and update game state.

        'Try not. Do. Or do not.' — Yoda
        But here, trying IS doing. And sometimes failing.

        Args:
            letter: A single lowercase letter to guess.

        Returns:
            True if the guess was correct, False otherwise.

        Raises:
            ValueError: If the letter is invalid or already guessed.
        """
        letter = letter.lower().strip()

        if len(letter) != 1 or not letter.isalpha():
            raise ValueError(f"'{letter}' is not a valid letter. Even Groot says more than that.")

        if letter in self.all_guesses:
            raise ValueError(f"'{letter}' was already guessed. Pay attention, 007.")

        if letter in self.word:
            self.correct_guesses.add(letter)
            return True

        self.wrong_guesses.append(letter)
        return False

    def reveal_hint(self) -> str | None:
        """Reveal one unguessed letter as a hint — the Hermione Granger lifeline.

        'When in doubt, go to the library.' — Hermione Granger, Harry Potter
        (Here, the library is us, and we're giving you a freebie.)

        Picks a random unguessed letter from the word, adds it to correct_guesses,
        and stores it in hint_letter. Returns None if no hint is available.

        Returns:
            The revealed letter, or None if hint is not available.
        """
        if not self.hint_available:
            return None

        # Find letters not yet guessed — the unrevealed horcruxes
        unrevealed = [
            letter for letter in set(self.word)
            if letter not in self.correct_guesses
        ]

        if not unrevealed:
            return None

        # "It's a mystery." — Scooby-Doo (before the unmasking)
        self.hint_letter = random.choice(unrevealed)
        self.correct_guesses.add(self.hint_letter)
        return self.hint_letter


# ---------------------------------------------------------------------------
# Factory function — "Let there be game." — Genesis 1:1 (game developer remix)
# ---------------------------------------------------------------------------
def conjure_new_game() -> HangmanGame:
    """Pick a random word and return a fresh HangmanGame instance.

    'Every adventure requires a first step.' — Cheshire Cat, Alice in Wonderland

    Returns:
        A brand-new HangmanGame ready for suffering — I mean, playing.
    """
    chosen_word = random.choice(THE_MULTIVERSE_OF_WORDS)
    return HangmanGame(word=chosen_word)
