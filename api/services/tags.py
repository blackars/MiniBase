"""Convención de tags MiniBase: siempre Capitalizado.

canon_tag('fantasy') -> 'Fantasy'
canon_tag('general culture') -> 'General Culture'
canon_tag('sci-fi') -> 'Sci-Fi'
Siglas cortas en mayúsculas se respetan: 'AB!', 'D&D'.
Clave de deduplicación: key_tag() = colapsa espacios + casefold.
"""
import re


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", str(s or "").strip())


def key_tag(s: str) -> str:
    return collapse(s).casefold()


def canon_tag(s: str) -> str | None:
    c = collapse(s)
    if not c:
        return None
    words = []
    for w in c.split(" "):
        if w.isupper() and len(w) <= 4:
            words.append(w)  # siglas: AB!, D&D, RPG
        elif "-" in w:
            words.append("-".join(p[:1].upper() + p[1:].lower() for p in w.split("-")))
        else:
            words.append(w[:1].upper() + w[1:].lower())
    return " ".join(words)


JUNK_KEYS = {"", "nan", "none", "null", "n/a", "na", "-", "--", "sin dato",
             "sindato", "unknown", "desconocido", "pendiente"}


def is_junk(s: str) -> bool:
    """Basura que nunca debe volverse tag: vacíos, N/A, letras sueltas ('N/A'->'N','A')."""
    k = key_tag(s)
    return not k or len(k) < 2 or k in JUNK_KEYS
