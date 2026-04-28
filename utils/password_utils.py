"""Password generation utilities — powered by cryptographic secrets.

'The strength of the Tower of Barad-dûr lies not in its walls, but in its
password policy.' — Sauron (probably), The Lord of the Rings

All randomness here uses the `secrets` module — cryptographically secure,
OS-backed entropy. The `random` module is strictly forbidden in this realm.
"""

import secrets
import string
from enum import Enum

# ---------------------------------------------------------------------------
# Character pools — the Four Nations of the alphabet
# ---------------------------------------------------------------------------
LOWERCASE_RUNES: str = string.ascii_lowercase   # e.g. 'abcdefghijklmnopqrstuvwxyz'
UPPERCASE_RUNES: str = string.ascii_uppercase   # e.g. 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGIT_RUNES: str = string.digits                # '0123456789'
# Symbols: exclude backslash and backtick to avoid shell/string injection issues
SYMBOL_RUNES: str = "!@#$%^&*()-_=+[]{}|;:,.<>?"

# ---------------------------------------------------------------------------
# Safety bounds — "size matters not" said Yoda, but he was wrong about passwords
# ---------------------------------------------------------------------------
MIN_PASSWORD_LENGTH: int = 8
MAX_PASSWORD_LENGTH: int = 128


# ---------------------------------------------------------------------------
# Strength tiers — ranked like Pokémon evolutions, but for security
# ---------------------------------------------------------------------------
class VaultStrength(Enum):
    """Password strength levels, named after iconic power tiers."""

    MUGGLE = "Weak"           # Harry Potter: ordinary, no magic
    PADAWAN = "Fair"          # Star Wars: trained, but not there yet
    JEDI_KNIGHT = "Strong"    # Star Wars: certified badass
    CHOSEN_ONE = "Very Strong"  # The Matrix / Star Wars crossover dream tier


# Minimum score thresholds for each strength tier
_STRENGTH_THRESHOLDS: dict[VaultStrength, int] = {
    VaultStrength.CHOSEN_ONE: 4,
    VaultStrength.JEDI_KNIGHT: 3,
    VaultStrength.PADAWAN: 2,
}


def forge_the_one_password(
    length: int,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """Forge the One Password to rule them all — securely.

    'One password to rule them all, one password to find them,
     one password to bring them all and in the darkness bind them.'
     — Tolkien (adapted), The Fellowship of the Ring

    Uses `secrets.choice()` for cryptographically secure random selection.
    Guarantees at least one character from each enabled character set, then
    fills remaining slots from the full combined pool. The result is shuffled
    with `secrets.SystemRandom` to eliminate position bias.

    Args:
        length: Desired password length. Clamped to [MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH].
        use_lowercase: Include lowercase letters.
        use_uppercase: Include uppercase letters.
        use_digits: Include numeric digits.
        use_symbols: Include special symbols.

    Returns:
        A cryptographically secure random password string.

    Raises:
        ValueError: If no character set is selected (the password would be empty).
    """
    # Assemble the fellowship of character sets
    active_pools: list[str] = []
    if use_lowercase:
        active_pools.append(LOWERCASE_RUNES)
    if use_uppercase:
        active_pools.append(UPPERCASE_RUNES)
    if use_digits:
        active_pools.append(DIGIT_RUNES)
    if use_symbols:
        active_pools.append(SYMBOL_RUNES)

    # "You shall not pass" — a password with no character set
    if not active_pools:
        raise ValueError(
            "At least one character set must be selected. "
            "Even Gandalf needs a staff."
        )

    # Clamp length: not too short, not too long — the Goldilocks zone of security
    clamped_length = max(MIN_PASSWORD_LENGTH, min(length, MAX_PASSWORD_LENGTH))

    # Phase 1: Guarantee at least one character from each selected pool
    # This ensures we never accidentally skip an entire character class
    guaranteed_chars: list[str] = [
        secrets.choice(pool) for pool in active_pools
    ]

    # Phase 2: Fill the rest from the full combined pool
    # "Resistance is futile" — every remaining slot will be randomised
    full_pool = "".join(active_pools)
    fill_count = clamped_length - len(guaranteed_chars)
    filler_chars: list[str] = [
        secrets.choice(full_pool) for _ in range(fill_count)
    ]

    all_chars = guaranteed_chars + filler_chars

    # Phase 3: Shuffle using SystemRandom (backed by os.urandom) to destroy
    # the guaranteed-chars positional pattern — no One Ring fingerprints
    # "Shuffle. Everything. Always." — Jason Bourne (paraphrased)
    rng = secrets.SystemRandom()
    rng.shuffle(all_chars)

    return "".join(all_chars)


def measure_password_strength(password: str) -> VaultStrength:
    """Assess the strength of a password — no X-ray vision required.

    'With great password entropy comes great account security.' — Uncle Ben
    (Spider-Man, probably, if he worked in InfoSec)

    Scores the password based on length and character-set diversity:
    - +1 point per character set present (lowercase, uppercase, digits, symbols)
    - +1 point if length >= 16
    - +1 point if length >= 32

    This is a heuristic strength indicator, NOT an entropy calculator.

    Args:
        password: The password string to evaluate.

    Returns:
        A VaultStrength enum value representing the password's strength tier.
    """
    if not password:
        return VaultStrength.MUGGLE

    score = 0

    # Award points for character diversity — the Infinity Stones of password strength
    if any(ch in LOWERCASE_RUNES for ch in password):
        score += 1
    if any(ch in UPPERCASE_RUNES for ch in password):
        score += 1
    if any(ch in DIGIT_RUNES for ch in password):
        score += 1
    if any(ch in SYMBOL_RUNES for ch in password):
        score += 1

    # Length bonuses — "go big or go home" (Kirk, probably)
    if len(password) >= 16:  # noqa: PLR2004
        score += 1
    if len(password) >= 32:  # noqa: PLR2004
        score += 1

    # Map score to strength tier — "It's over, Anakin. I have the high ground."
    for tier, threshold in _STRENGTH_THRESHOLDS.items():
        if score >= threshold:
            return tier

    return VaultStrength.MUGGLE
