"""Hangman game page — where stick figures go to meet their maker.

'Game over, man! Game over!' — Private Hudson, Aliens
(Unless you guess correctly. Then it's more of a 'game continues, man!')

Renders the full Hangman game using Streamlit session state, ASCII art gallows,
letter-by-letter guessing, and a hint system for when things get desperate.
"""

import streamlit as st

from utils.hangman_engine import (
    HINT_TRIGGER_WRONG_COUNT,
    MAX_WRONG_GUESSES,
    LOSE_MESSAGE,
    WIN_MESSAGE,
    HangmanGame,
    conjure_new_game,
)

# ---------------------------------------------------------------------------
# Constants — "In the beginning, God created the constants." — Genesis (probably)
# ---------------------------------------------------------------------------
SESSION_GAME_KEY: str = "hangman_game"
SESSION_MESSAGE_KEY: str = "hangman_message"
SESSION_MESSAGE_TYPE_KEY: str = "hangman_message_type"  # "success" | "error" | "info"

GALLOWS_FONT_SIZE: str = "0.85rem"
ALPHABET: str = "abcdefghijklmnopqrstuvwxyz"


# ---------------------------------------------------------------------------
# Session state helpers — "Initialise everything. Trust no one." — Fox Mulder
# ---------------------------------------------------------------------------
def _boot_session_state() -> None:
    """Initialise session state keys for the Hangman game.

    'You must unlearn what you have learned.' — Yoda
    But first, you must learn it. So: initialise.
    """
    if SESSION_GAME_KEY not in st.session_state:
        st.session_state[SESSION_GAME_KEY] = conjure_new_game()
    if SESSION_MESSAGE_KEY not in st.session_state:
        st.session_state[SESSION_MESSAGE_KEY] = ""
    if SESSION_MESSAGE_TYPE_KEY not in st.session_state:
        st.session_state[SESSION_MESSAGE_TYPE_KEY] = "info"


def _get_game() -> HangmanGame:
    """Retrieve the current game from session state."""
    return st.session_state[SESSION_GAME_KEY]


def _set_message(text: str, kind: str = "info") -> None:
    """Store a UI feedback message to be displayed on the next render."""
    st.session_state[SESSION_MESSAGE_KEY] = text
    st.session_state[SESSION_MESSAGE_TYPE_KEY] = kind


# ---------------------------------------------------------------------------
# Event callbacks — "Actions speak louder than render cycles." — Streamlit Kant
# ---------------------------------------------------------------------------
def _on_new_game() -> None:
    """Reset the game state — 'Reset? RESET?! Fine. Let's do this.' — The Mandalorian."""
    st.session_state[SESSION_GAME_KEY] = conjure_new_game()
    st.session_state[SESSION_MESSAGE_KEY] = ""
    st.session_state[SESSION_MESSAGE_TYPE_KEY] = "info"


def _on_guess(letter: str) -> None:
    """Handle a letter guess button click.

    'I volunteer as tribute!' — Katniss Everdeen, The Hunger Games
    (Each letter bravely steps forward to potentially save the stick figure.)
    """
    game: HangmanGame = _get_game()

    if game.is_over:
        return

    try:
        correct = game.guess(letter)
    except ValueError as hermione_disapproves:
        _set_message(str(hermione_disapproves), "error")
        return

    if correct:
        if game.is_won:
            _set_message(WIN_MESSAGE, "success")
        else:
            _set_message(f"✅ '{letter.upper()}' is in the word!", "success")
    else:
        if game.is_lost:
            _set_message(f"{LOSE_MESSAGE}\nThe word was: **{game.word.upper()}**", "error")
        else:
            remaining = MAX_WRONG_GUESSES - game.wrong_count
            _set_message(
                f"❌ '{letter.upper()}' is not in the word. "
                f"{remaining} guess(es) remaining.",
                "error",
            )


def _on_hint() -> None:
    """Trigger the hint system — the Obi-Wan Kenobi of last resorts.

    'Help me, Obi-Wan Kenobi, you're my only hope.' — Princess Leia
    (This activates after {HINT_TRIGGER_WRONG_COUNT} wrong guesses.)
    """
    game: HangmanGame = _get_game()
    revealed = game.reveal_hint()

    if revealed:
        _set_message(
            f"🔍 Hint: the letter **'{revealed.upper()}'** has been revealed for you!",
            "info",
        )
    else:
        _set_message("No hint available right now.", "info")


# ---------------------------------------------------------------------------
# UI sub-renderers — "Divide and conquer." — Julius Caesar (software architect)
# ---------------------------------------------------------------------------
def _render_gallows(game: HangmanGame) -> None:
    """Render the ASCII art gallows in a styled code block.

    'Art is whatever you can get away with.' — Andy Warhol
    (ASCII art is whatever a monospace font can get away with.)
    """
    st.code(game.gallows_art, language=None)


def _render_word_display(game: HangmanGame) -> None:
    """Render the masked word with correct guesses revealed.

    'The truth is out there.' — Fox Mulder, The X-Files
    (The letters are also out there. Some of them, anyway.)
    """
    st.markdown(
        f"""
        <div style="
            font-size:2rem;
            font-family:monospace;
            letter-spacing:0.4rem;
            text-align:center;
            padding:1rem 0;
            color:#58a6ff;
            font-weight:700;
        ">
            {game.display_word}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_guess_tracker(game: HangmanGame) -> None:
    """Render correct and incorrect guesses in two columns.

    'Keep your friends close and your enemies closer.' — Michael Corleone
    (Correct guesses are friends. Wrong guesses are enemies.)
    """
    col_right, col_wrong = st.columns(2)

    with col_right:
        st.markdown("**✅ Correct Guesses**")
        correct_display = ", ".join(
            sorted(letter.upper() for letter in game.correct_guesses
                   if letter != game.hint_letter)
        ) or "None yet"
        hint_display = (
            f", **{game.hint_letter.upper()}** *(hint)*"
            if game.hint_letter
            else ""
        )
        st.markdown(f"{correct_display}{hint_display}")

    with col_wrong:
        st.markdown("**❌ Wrong Guesses**")
        wrong_display = ", ".join(
            letter.upper() for letter in game.wrong_guesses
        ) or "None yet"
        st.markdown(
            f'<span style="color:#ff7b72">{wrong_display}</span>',
            unsafe_allow_html=True,
        )


def _render_alphabet_buttons(game: HangmanGame) -> None:
    """Render one clickable button per letter of the alphabet.

    'Every vote counts.' — Hamilton (the musical)
    (Every letter counts too. Choose wisely.)
    """
    st.markdown("**Pick a Letter:**")

    # Render in rows of 9 — like the Fellowship, but with more members
    letters = list(ALPHABET)
    row_size = 9
    rows = [letters[i:i + row_size] for i in range(0, len(letters), row_size)]

    for row in rows:
        cols = st.columns(len(row))
        for col, letter in zip(cols, row):
            already_guessed = letter in game.all_guesses
            with col:
                st.button(
                    letter.upper(),
                    key=f"hangman_letter_{letter}",
                    on_click=_on_guess,
                    args=(letter,),
                    disabled=already_guessed or game.is_over,
                    use_container_width=True,
                )


def _render_hint_section(game: HangmanGame) -> None:
    """Render the hint button — available after HINT_TRIGGER_WRONG_COUNT wrong guesses.

    'Sometimes you need a little help from your friends.' — The Beatles
    (And sometimes that friend is a hard-coded reveal-one-letter function.)
    """
    wrong_until_hint = max(0, HINT_TRIGGER_WRONG_COUNT - game.wrong_count)

    if game.hint_letter is not None:
        # Hint already used — "That's all, folks!" — Porky Pig
        st.info(
            f"🔍 Hint already used: **'{game.hint_letter.upper()}'** was revealed.",
            icon="💡",
        )
    elif game.hint_available:
        st.button(
            "💡 Reveal Hint (1 free letter)",
            on_click=_on_hint,
            type="secondary",
        )
    elif not game.is_over:
        st.markdown(
            f'<small style="color:#8b949e">💡 Hint unlocks after '
            f'{wrong_until_hint} more wrong guess(es)</small>',
            unsafe_allow_html=True,
        )


def _render_feedback_message() -> None:
    """Display the last action feedback message if one exists.

    'With great feedback comes great improvement.' — Agile Manifesto, Spider-Man remix
    """
    message = st.session_state.get(SESSION_MESSAGE_KEY, "")
    kind = st.session_state.get(SESSION_MESSAGE_TYPE_KEY, "info")

    if not message:
        return

    if kind == "success":
        st.success(message)
    elif kind == "error":
        st.error(message)
    else:
        st.info(message)


def _render_game_over_reveal(game: HangmanGame) -> None:
    """Reveal the full word if the game is over and the player lost.

    'You can't handle the truth!' — Col. Jessup, A Few Good Men
    (Actually, you can. Here it is.)
    """
    if game.is_lost:
        st.markdown(
            f"""
            <div style="
                background:#1a1a2e;border:1px solid #ff7b72;
                border-radius:.75rem;padding:1.2rem;text-align:center;
                margin-top:1rem;
            ">
                <span style="color:#8b949e;font-size:.85rem;">The word was:</span><br>
                <span style="font-size:2rem;font-weight:700;
                             color:#ff7b72;letter-spacing:.3rem;">
                    {game.word.upper()}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Main render function — "This is the way." — Din Djarin, The Mandalorian
# ---------------------------------------------------------------------------
def render() -> None:
    """Render the complete Hangman game page.

    'It's dangerous to go alone! Take this.' — Old man, The Legend of Zelda
    (Here 'this' is a fully-functional Streamlit Hangman game.)
    """
    _boot_session_state()
    game = _get_game()

    # Page header
    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem">🪢 Hangman</h1>
            <p>
                Guess the pop-culture mystery word before the stick figure meets
                their fate. You have 6 wrong guesses. Choose wisely.
                <em>"The night is dark and full of terrors."</em> — Melisandre
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # New Game button — always available
    st.button("🔄 New Game", on_click=_on_new_game, type="primary")

    st.markdown("---")

    # Main layout: gallows on left, game controls on right
    col_gallows, col_game = st.columns([1, 2], gap="large")

    with col_gallows:
        st.subheader("⚰️ The Gallows")
        _render_gallows(game)

        # Wrong-guess counter — "How many fingers am I holding up?" — Riddler
        st.markdown(
            f'<p style="color:#8b949e;font-size:.85rem;text-align:center;">'
            f'{game.wrong_count} / {MAX_WRONG_GUESSES} wrong guesses</p>',
            unsafe_allow_html=True,
        )

    with col_game:
        st.subheader("🔡 The Mystery Word")
        _render_word_display(game)

        st.markdown("---")
        _render_guess_tracker(game)

        st.markdown("---")
        _render_feedback_message()

        if not game.is_over:
            _render_alphabet_buttons(game)
            st.markdown("---")
            _render_hint_section(game)
        else:
            _render_game_over_reveal(game)
            if game.is_won:
                st.balloons()

    # How-to section — "With great games come great instructions." — Uncle Ben
    with st.expander("📖 How to Play", expanded=False):
        st.markdown(
            f"""
            - Guess one letter at a time by clicking the alphabet buttons.
            - You have **{MAX_WRONG_GUESSES} wrong guesses** before the stick figure
              is fully drawn and the game ends.
            - After **{HINT_TRIGGER_WRONG_COUNT} wrong guesses**, a 💡 **Hint** button
              unlocks — click it to reveal one mystery letter for free (one hint per game).
            - Click **🔄 New Game** at any time to start fresh with a new word.
            - All words are from the **pop-culture multiverse** — films, books,
              TV shows, and games. *May the odds be ever in your favour.*
            """
        )
