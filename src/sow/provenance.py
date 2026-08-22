"""Stage 2 -- parse authority metadata off each document, deterministically.

No model is involved. Every field is read from header lines that exist in the
corpus, and the line it was read from is retained so that a provenance decision
is itself citable.

Authority is several orthogonal axes, not one score. An unsigned addendum and an
internal chat message are not comparable on a single scale; collapsing them to a
number is exactly what produces a recency-only resolver that puts internal
negotiating posture into a client-facing document.
"""

from __future__ import annotations

import re
from datetime import date

from .config import Roster
from .models import (
    Audience,
    DocProvenance,
    DocStatus,
    Document,
    EngagementLabel,
    FieldEvidence,
    Instrument,
    Restriction,
)

_ISO_DAY = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_ISO_MONTH = re.compile(r"\b(\d{4})-(\d{2})\b")
_VERSION = re.compile(r"\bversion\s+(\d+)\b", re.IGNORECASE)

# A "**Key:**" header field, e.g. "**From:**", "**Date:**", "**Status:**".
# Deliberately does not match a chat export's "**[timestamp] speaker:**".
_METADATA_FIELD = re.compile(r"^\*\*[A-Z][A-Za-z /&'-]{1,20}:\*\*")

# "Superseded by X" means THIS document is superseded.
# "Supersedes X" means this document supersedes ANOTHER -- the opposite claim.
_SUPERSEDED_BY = re.compile(r"supersed(?:ed|es)\s+by\b", re.IGNORECASE)
_SUPERSEDES = re.compile(r"\bsupersedes\b(?!\s+by)", re.IGNORECASE)

_RESTRICTION_MARKERS: tuple[tuple[str, Restriction], ...] = (
    ("not for client distribution", "not_for_client_distribution"),
    ("do not circulate", "do_not_circulate"),
)

# Instrument classification, first match wins. Ordering matters: "all-hands
# notes" must be tested before the generic "notes" rule, and the SOW template
# must be matched by path before the "statement of work" rule sees its title.
_INSTRUMENT_RULES: tuple[tuple[str, str, Instrument], ...] = (
    ("path", "sow_template.md", "template"),
    ("h1", "msa", "executed_contract"),
    ("h1+executed", "statement of work", "executed_sow"),
    ("h1", "scope addendum", "unsigned_addendum"),
    ("h1", "working draft", "working_draft"),
    ("header", "do not circulate", "working_draft"),
    ("h1", "rate card", "policy"),
    ("h1", "policy", "policy"),
    ("h1", "playbook", "policy"),
    ("h1", "checklist", "policy"),
    ("h1", "onboarding", "policy"),
    ("h1", "post-mortem", "reference"),
    ("h1", "one-pager", "reference"),
    ("h1", "who we are", "reference"),
    ("h1", "all-hands", "internal_meeting"),
    ("h1", "chat export", "internal_chat"),
    ("h1", "email", "client_correspondence"),
    ("h1", "call transcript", "client_meeting"),
    ("h1", "notes", "working_draft"),
)

_AUDIENCE_BY_INSTRUMENT: dict[Instrument, Audience] = {
    "executed_contract": "client_facing",
    "executed_sow": "client_facing",
    "signed_addendum": "client_facing",
    "unsigned_addendum": "client_facing",
    "superseded_addendum": "client_facing",
    "client_correspondence": "client_facing",
    "client_meeting": "client_facing",
    "internal_meeting": "internal_only",
    "internal_chat": "internal_only",
    "working_draft": "internal_only",
    "policy": "standard",
    "template": "standard",
    "reference": "standard",
    # An unclassified instrument is treated as internal deliberation: the
    # conservative direction, since it bars sole support rather than granting it.
    "unknown": "internal_only",
}


def header_block(doc: Document) -> list[tuple[int, str]]:
    """The document's metadata preamble, with 1-based line numbers.

    The preamble is the contiguous run of non-blank lines from the top. Email
    threads put their metadata after a ``---`` fence, so if the next non-blank
    line after that run is a fence, the run following it is included too.

    Scanning must stop there. Reading a fixed number of lines instead bleeds
    into body text -- the sales playbook's fourth guardrail contains the phrase
    "the executed MSA always wins", which a naive scan reads as the playbook
    itself being an executed instrument.
    """
    out: list[tuple[int, str]] = []
    lines = doc.lines
    i = 0
    n = len(lines)

    for _block in range(2):
        while i < n and not lines[i].strip():
            i += 1
        if out:
            # A second run counts as metadata only behind a horizontal rule, or
            # when it opens with a "**Key:**" field. The bracketed timestamps of
            # a chat export ("**[2026-08-18 16:40] alicia.fontaine:**") fail that
            # shape deliberately: one of those messages says "out for signature",
            # which would otherwise be read as the export's own lifecycle status.
            if i >= n:
                break
            stripped = lines[i].strip()
            if stripped not in ("---", "***", "___"):
                if not _METADATA_FIELD.match(stripped):
                    break
            else:
                i += 1
                while i < n and not lines[i].strip():
                    i += 1
        while i < n and lines[i].strip():
            out.append((i + 1, lines[i]))
            i += 1

    return out


# --------------------------------------------------------------------------- #
# Engagement
# --------------------------------------------------------------------------- #


def _subject_label(text: str, roster: Roster) -> tuple[str, str]:
    """Label one subject signal -- a title line or a filename stem.

    Only the signal text is considered. Body text deliberately gets no vote: the
    Harding chat export names Northgate in a message, and must still be admitted
    as Harding evidence.
    """
    lowered = text.lower()
    hits = sorted(
        name
        for name, aliases in roster.clients.items()
        if any(alias in lowered for alias in aliases)
    )
    if len(hits) > 1:
        return "AMBIGUOUS", f"names multiple clients ({', '.join(hits)})"
    if len(hits) == 1:
        return hits[0], f"names client '{hits[0]}'"
    if any(marker in lowered for marker in roster.company_markers):
        return "company", "names the company and no client"
    return "company", "names no client"


def classify_engagement(
    doc: Document, roster: Roster
) -> tuple[EngagementLabel, str, str | None]:
    """Decide which engagement a document is about.

    Two independent signals -- the H1 title and the filename stem -- must agree.
    A client-roster hit on either signal beats a bare company default; genuine
    disagreement, a multi-client subject, or a missing title yields AMBIGUOUS.

    The failure mode is exclusion: an AMBIGUOUS document never enters the
    evidence pool.

    Returns:
        (label, reason, source_line) where source_line is the H1 if present.
    """
    h1 = doc.h1
    if h1 is None:
        return "AMBIGUOUS", "no H1 title line; document subject cannot be established", None

    title_label, title_reason = _subject_label(h1, roster)
    stem_label, stem_reason = _subject_label(doc.path.stem, roster)
    h1_line = f"# {h1}"

    if title_label == "AMBIGUOUS":
        return "AMBIGUOUS", f"title {title_reason}", h1_line
    if stem_label == "AMBIGUOUS":
        return "AMBIGUOUS", f"filename {stem_reason}", h1_line

    if title_label == stem_label:
        return title_label, f"title and filename agree: {title_reason}", h1_line  # type: ignore[return-value]
    if title_label == "company":
        return stem_label, f"filename {stem_reason}; title named no client", h1_line  # type: ignore[return-value]
    if stem_label == "company":
        return title_label, f"title {title_reason}; filename named no client", h1_line  # type: ignore[return-value]

    return (
        "AMBIGUOUS",
        f"signals disagree: title -> {title_label}, filename -> {stem_label}",
        h1_line,
    )


# --------------------------------------------------------------------------- #
# Instrument, audience, restriction, status, date
# --------------------------------------------------------------------------- #


def classify_instrument(doc: Document) -> tuple[Instrument, str, str | None]:
    """Classify what kind of document this is, by title and header markers."""
    h1 = (doc.h1 or "").lower()
    header = " \n".join(line for _, line in header_block(doc)).lower()

    for scope, needle, instrument in _INSTRUMENT_RULES:
        if scope == "path":
            if doc.doc_id == needle:
                return instrument, f"path is {needle}", None
        elif scope == "h1":
            if needle in h1:
                # A transcript that announces itself as internal is internal.
                if instrument == "client_meeting" and "internal" in (h1 + header):
                    return "internal_meeting", "title marks the transcript internal", doc.h1
                return instrument, f"title contains '{needle}'", doc.h1
        elif scope == "h1+executed":
            if needle in h1 and "executed" in header:
                return instrument, f"title contains '{needle}' and header says executed", doc.h1
        elif scope == "header":
            if needle in header:
                return instrument, f"header contains '{needle}'", None

    return "unknown", "no instrument rule matched title or header", doc.h1


def classify_restriction(doc: Document) -> tuple[Restriction, str, str | None, int | None]:
    """Detect an explicit restriction on client distribution."""
    for line_no, line in header_block(doc):
        lowered = line.lower()
        for marker, restriction in _RESTRICTION_MARKERS:
            if marker in lowered:
                return restriction, f"header states '{marker}'", line, line_no
    return "none", "no distribution restriction in header", None, None


def classify_audience(instrument: Instrument, restriction: Restriction) -> tuple[Audience, str]:
    """Decide how this document may support client-facing assertive text.

    An explicit distribution restriction always forces ``internal_only``,
    whatever the instrument class says.
    """
    if restriction != "none":
        return "internal_only", f"distribution restricted ({restriction})"
    audience = _AUDIENCE_BY_INSTRUMENT[instrument]
    return audience, f"instrument '{instrument}' is {audience}"


def classify_status(
    doc: Document, doc_date: date | None
) -> tuple[DocStatus, str, str | None, int | None]:
    """Read declared lifecycle status off the header preamble.

    Supersession declared by a *different* document is applied later, by
    :func:`apply_supersession`. A document carrying a date but no lifecycle
    marker is ``current``; one carrying neither is ``unknown`` and is reported
    rather than assumed current.
    """
    for line_no, line in header_block(doc):
        lowered = line.lower()
        if _SUPERSEDED_BY.search(lowered):
            return "superseded", "header states it is superseded", line, line_no
        if "out for signature" in lowered:
            return "out_for_signature", "header states out for signature", line, line_no
        if "incomplete" in lowered or "do not circulate" in lowered:
            return "draft_incomplete", "header marks the draft incomplete", line, line_no
        if "executed" in lowered:
            return "executed", "header states executed", line, line_no

    if doc_date is not None:
        return "current", "dated, with no lifecycle marker in the header", None, None

    return "unknown", "no lifecycle marker and no date in the header", None, None


def parse_doc_date(doc: Document) -> tuple[date | None, str, str | None, int | None]:
    """Parse the document's own date from its header, title, or filename.

    Month-precision dates (``2026-03``) are normalised to the first of the month
    and the reduced precision is recorded, never silently presented as a day.
    Returns None when no date exists -- a missing date is reported, not invented.
    """
    candidates: list[tuple[int | None, str]] = [(n, l) for n, l in header_block(doc)]
    if doc.h1:
        candidates.append((1, doc.h1))
    candidates.append((None, doc.path.stem))

    for line_no, line in candidates:
        m = _ISO_DAY.search(line)
        if m:
            y, mo, d = (int(g) for g in m.groups())
            return date(y, mo, d), "day-precision date in header", line, line_no

    for line_no, line in candidates:
        m = _ISO_MONTH.search(line)
        if m:
            y, mo = (int(g) for g in m.groups())
            return (
                date(y, mo, 1),
                "month-precision date normalised to first of month",
                line,
                line_no,
            )

    return None, "no date found in header, title or filename", None, None


# --------------------------------------------------------------------------- #
# Assembly
# --------------------------------------------------------------------------- #


def build_provenance(doc: Document, roster: Roster) -> DocProvenance:
    """Parse the full provenance record for one document."""
    engagement, eng_reason, eng_line = classify_engagement(doc, roster)
    instrument, inst_reason, inst_line = classify_instrument(doc)
    restriction, restr_reason, restr_line, restr_no = classify_restriction(doc)
    audience, aud_reason = classify_audience(instrument, restriction)
    doc_date, date_reason, date_line, date_no = parse_doc_date(doc)
    status, status_reason, status_line, status_no = classify_status(doc, doc_date)

    evidence = [
        FieldEvidence(
            field="engagement", value=engagement, reason=eng_reason, source_line=eng_line
        ),
        FieldEvidence(
            field="instrument", value=instrument, reason=inst_reason, source_line=inst_line
        ),
        FieldEvidence(
            field="restriction",
            value=restriction,
            reason=restr_reason,
            source_line=restr_line,
            line_no=restr_no,
        ),
        FieldEvidence(field="audience", value=audience, reason=aud_reason),
        FieldEvidence(
            field="status",
            value=status,
            reason=status_reason,
            source_line=status_line,
            line_no=status_no,
        ),
        FieldEvidence(
            field="doc_date",
            value=doc_date.isoformat() if doc_date else "none",
            reason=date_reason,
            source_line=date_line,
            line_no=date_no,
        ),
    ]

    return DocProvenance(
        doc_id=doc.doc_id,
        engagement=engagement,
        instrument=instrument,
        audience=audience,
        status=status,
        restriction=restriction,
        doc_date=doc_date,
        evidence=evidence,
    )


def apply_supersession(
    docs: list[Document], provs: dict[str, DocProvenance]
) -> list[str]:
    """Mark documents superseded by a *later version of the same document*.

    Scope Addendum v1 does not say it is superseded -- only v2 says it supersedes
    v1. Supersession is therefore a cross-document fact: documents are grouped by
    their exact H1 title, and where any member of a group declares "Supersedes",
    every lower-numbered version in that group is marked superseded.

    Mutates ``provs`` in place. Returns human-readable notes for the trace.
    """
    by_title: dict[str, list[Document]] = {}
    for doc in docs:
        if doc.h1:
            by_title.setdefault(doc.h1.strip(), []).append(doc)

    notes: list[str] = []
    for title, group in by_title.items():
        if len(group) < 2:
            continue

        versions: dict[str, int] = {}
        declares: list[str] = []
        for doc in group:
            header = " \n".join(line for _, line in header_block(doc))
            m = _VERSION.search(header)
            if m:
                versions[doc.doc_id] = int(m.group(1))
            if _SUPERSEDES.search(header):
                declares.append(doc.doc_id)

        if not declares or len(versions) < 2:
            continue

        newest = max(versions.values())
        for doc_id, version in versions.items():
            if version < newest and provs[doc_id].status != "superseded":
                prov = provs[doc_id]
                prov.status = "superseded"
                prov.evidence.append(
                    FieldEvidence(
                        field="status",
                        value="superseded",
                        reason=(
                            f"version {version} of '{title}'; version {newest} "
                            f"({', '.join(declares)}) declares it supersedes an earlier version"
                        ),
                    )
                )
                notes.append(
                    f"{doc_id}: marked superseded by {', '.join(declares)} "
                    f"(v{version} < v{newest})"
                )

    # Instrument refinement now that lifecycle status is final.
    for prov in provs.values():
        if prov.instrument in ("unsigned_addendum", "signed_addendum", "superseded_addendum"):
            if prov.status == "superseded":
                prov.instrument = "superseded_addendum"
            elif prov.status == "out_for_signature":
                prov.instrument = "unsigned_addendum"
            else:
                prov.instrument = "signed_addendum"

    return notes
