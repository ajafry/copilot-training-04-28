"""Password Generator page — because 'password123' is not acceptable.

'I find your lack of entropy... disturbing.' — Darth Vader, probably,
after reviewing your IT team's password policy.
"""

import streamlit as st

from utils.password_utils import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    VaultStrength,
    forge_the_one_password,
    measure_password_strength,
)

# ---------------------------------------------------------------------------
# Constants — no magic numbers; even Dumbledore had a grimoire
# ---------------------------------------------------------------------------
DEFAULT_PASSWORD_LENGTH: int = 16
STRENGTH_BADGE_STYLES: dict[VaultStrength, tuple[str, str]] = {
    VaultStrength.MUGGLE:      ("#ff4b4b", "🔴"),
    VaultStrength.PADAWAN:     ("#ffa500", "🟠"),
    VaultStrength.JEDI_KNIGHT: ("#58a6ff", "🔵"),
    VaultStrength.CHOSEN_ONE:  ("#3dd68c", "🟢"),
}


def _render_strength_badge(password: str) -> None:
    """Render a colour-coded strength badge for the given password.

    'Know thy enemy — and know thyself.' — Sun Tzu, The Art of War
    (Also applicable to knowing your password entropy.)
    """
    if not password:
        return

    strength = measure_password_strength(password)
    colour, dot = STRENGTH_BADGE_STYLES[strength]

    st.markdown(
        f"""
        <div style="
            display:inline-flex;align-items:center;gap:.5rem;
            background:#161b22;border:1px solid {colour};
            border-radius:.5rem;padding:.4rem .9rem;margin-top:.5rem;
        ">
            <span style="font-size:1rem">{dot}</span>
            <span style="color:{colour};font-weight:600;font-size:.95rem;">
                Strength: {strength.value}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    """Render the Password Generator page.

    'Mission: Impossible — generate a secure password manually.
     Mission: Accomplished — let the machine do it.' — Ethan Hunt (reimagined)
    """
    st.markdown(
        """
        <div class="hero" style="padding:2rem">
            <h1 style="font-size:2rem">
                <i class="bi bi-shield-lock"></i>&nbsp; Password Generator
            </h1>
            <p>
                Cryptographically secure passwords — powered by
                <code>secrets</code>, not <code>random</code>.
                Even Q from MI6 would approve.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------------------------
    # Session state initialisation — "Initialising T-800…" — The Terminator
    # -----------------------------------------------------------------------
    if "generated_password" not in st.session_state:
        st.session_state.generated_password = ""
    if "pw_error" not in st.session_state:
        st.session_state.pw_error = ""

    # -----------------------------------------------------------------------
    # Controls layout
    # -----------------------------------------------------------------------
    col_controls, col_output = st.columns([1, 1], gap="large")

    with col_controls:
        st.subheader("⚙️ Configuration")

        password_length = st.slider(
            "Password Length",
            min_value=MIN_PASSWORD_LENGTH,
            max_value=MAX_PASSWORD_LENGTH,
            value=DEFAULT_PASSWORD_LENGTH,
            step=1,
            help=(
                f"Choose a length between {MIN_PASSWORD_LENGTH} "
                f"and {MAX_PASSWORD_LENGTH} characters."
            ),
        )

        st.markdown("**Character Sets**")

        # "Assemble!" — Nick Fury, The Avengers
        use_lowercase = st.checkbox("Lowercase letters  (a–z)", value=True)
        use_uppercase = st.checkbox("Uppercase letters  (A–Z)", value=True)
        use_digits    = st.checkbox("Digits  (0–9)", value=True)
        use_symbols   = st.checkbox("Symbols  (!@#$…)", value=True)

        no_charset_selected = not any(
            [use_lowercase, use_uppercase, use_digits, use_symbols]
        )

        if no_charset_selected:
            st.warning(
                "⚠️ Select at least one character set. "
                "Even Gandalf needs *some* material to work with.",
                icon="🧙",
            )

        # "Engage!" — Captain Picard, Star Trek: TNG
        generate_clicked = st.button(
            "⚡ Generate Password",
            disabled=no_charset_selected,
            use_container_width=True,
            type="primary",
        )

        if generate_clicked:
            try:
                st.session_state.generated_password = forge_the_one_password(
                    length=password_length,
                    use_lowercase=use_lowercase,
                    use_uppercase=use_uppercase,
                    use_digits=use_digits,
                    use_symbols=use_symbols,
                )
                st.session_state.pw_error = ""
            except ValueError as dark_side_incident:
                # "The dark side of the Force is a pathway to many abilities
                #  some consider to be unnatural." — Palpatine
                st.session_state.pw_error = str(dark_side_incident)
                st.session_state.generated_password = ""

    # -----------------------------------------------------------------------
    # Output panel
    # -----------------------------------------------------------------------
    with col_output:
        st.subheader("🔐 Your Password")

        if st.session_state.pw_error:
            st.error(st.session_state.pw_error)

        elif st.session_state.generated_password:
            the_chosen_password = st.session_state.generated_password

            # Display in st.code() — built-in copy button, no clipboard hacks needed
            # "Here's looking at you, kid." — Casablanca (the copy button is the kid)
            st.code(the_chosen_password, language=None)

            _render_strength_badge(the_chosen_password)

            st.markdown("---")
            st.markdown(
                """
                <small style="color:#8b949e">
                💡 <strong>Tip:</strong> Click the copy icon above to copy your password.
                Never store it in plain text — use a password manager.
                </small>
                """,
                unsafe_allow_html=True,
            )

        else:
            # Placeholder before first generation
            st.markdown(
                """
                <div style="
                    background:#0d1117;border:1px dashed #30363d;
                    border-radius:.75rem;padding:2rem;text-align:center;
                    color:#8b949e;
                ">
                    <span style="font-size:2rem">🔒</span><br>
                    <span>Configure your settings and click <strong>Generate Password</strong>.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # -----------------------------------------------------------------------
    # Security notes — because Uncle Ben said so
    # -----------------------------------------------------------------------
    with st.expander("🛡️ Security Notes", expanded=False):
        st.markdown(
            """
            - **`secrets` module**: All randomness uses Python's `secrets` module, backed
              by `os.urandom()` — cryptographically secure, suitable for passwords and tokens.
            - **No `random` module**: The standard `random` module is *not* used here — it is
              a PRNG, not suitable for security-sensitive data.
            - **Character set guarantee**: At least one character from each selected set is
              always included, then the remainder is filled and shuffled to eliminate bias.
            - **Symbols curated**: The symbol set excludes `\\` and `` ` `` to reduce risk of
              injection issues in shells and configuration files.
            - **Passwords are not stored**: This page generates passwords in-memory only.
              They are never logged, transmitted, or persisted.
            - **Recommendation**: Use a reputable password manager (e.g. Bitwarden, 1Password)
              to store generated passwords securely.
            """
        )
