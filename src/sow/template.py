"""Stage 6 -- parse the SOW template into sections and required elements.

The template does not only name its sections; the guidance prose under each
heading enumerates what that section must contain. Section 12 reads "How
deliverables are accepted, by whom, and within what window", which yields three
requirements -- and the middle one, the client-side acceptance authority, is
never satisfied anywhere in the corpus.

Parsing that list at run time is what makes insufficiency detection evidence-led.
The alternative, a hand-written checklist of things to look for, would only ever
find gaps that were anticipated while writing it.
"""

from __future__ import annotations

import re

from .config import ConfigError
from .models import Document, SectionSpec

_SECTION = re.compile(r"^##\s+(\d+)\.\s+(.*?)\s*$")
_SUBSECTION = re.compile(r"^###\s+[\d.]*\s*(.*?)\s*$")
_TABLE_PREFIX = re.compile(r"^table:\s*", re.IGNORECASE)


def parse_template(doc: Document) -> list[SectionSpec]:
    """Parse the SOW template into ordered section specifications.

    Raises:
        ConfigError: if the template contains no numbered sections, which would
            silently yield a zero-section draft.
    """
    sections: list[SectionSpec] = []
    current: dict[str, object] | None = None

    for line in doc.lines:
        section_match = _SECTION.match(line)
        if section_match:
            if current:
                sections.append(_finalise(current))
            current = {
                "section_id": int(section_match.group(1)),
                "title": section_match.group(2),
                "guidance": [],
                "subsections": [],
            }
            continue

        if current is None:
            continue

        sub_match = _SUBSECTION.match(line)
        if sub_match:
            current["subsections"].append(sub_match.group(1))  # type: ignore[union-attr]
            continue

        stripped = line.strip()
        if stripped and not stripped.startswith(("#", ">")):
            current["guidance"].append(stripped)  # type: ignore[union-attr]

    if current:
        sections.append(_finalise(current))

    if not sections:
        raise ConfigError(
            f"{doc.doc_id}: no '## N. Title' sections found; the template cannot be parsed"
        )

    return sections


def _finalise(raw: dict[str, object]) -> SectionSpec:
    """Build a SectionSpec, deriving required elements from its guidance."""
    guidance = " ".join(raw["guidance"])  # type: ignore[arg-type]
    subsections: list[str] = list(raw["subsections"])  # type: ignore[arg-type]

    elements = split_requirements(guidance)
    # Where a section is defined by its subsections rather than by prose -- as
    # Scope of Work is, by In Scope and Out of Scope -- those are the elements.
    for sub in subsections:
        if not any(sub.lower() in e.lower() for e in elements):
            elements.insert(subsections.index(sub), sub)

    return SectionSpec(
        section_id=int(raw["section_id"]),  # type: ignore[arg-type]
        title=str(raw["title"]),
        guidance=guidance,
        required_elements=elements,
        subsections=subsections,
    )


def split_requirements(guidance: str) -> list[str]:
    """Split guidance prose into the elements a section must cover.

    Splits on semicolons, commas and " and " at bracket depth zero, so a
    parenthetical enumeration such as "staffing (role, allocation)" stays intact
    as one requirement rather than fragmenting into two.
    """
    text = _TABLE_PREFIX.sub("", guidance.strip())
    parts: list[str] = []
    buf: list[str] = []
    depth = 0
    i = 0

    while i < len(text):
        char = text[i]
        if char in "([":
            depth += 1
        elif char in ")]":
            depth = max(0, depth - 1)

        if depth == 0:
            if char in ";,":
                parts.append("".join(buf))
                buf = []
                i += 1
                continue
            if text[i : i + 5].lower() == " and ":
                parts.append("".join(buf))
                buf = []
                i += 5
                continue

        buf.append(char)
        i += 1

    parts.append("".join(buf))
    return [p for p in (part.strip(" .;,") for part in parts) if p]
