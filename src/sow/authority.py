"""The authority policy: when a disagreement resolves, and when it must not.

Authority is a partial order, not a score. The rules below are applied in order
and any of them may decline to produce a winner, which is the point -- a policy
that always resolves is just a recency sort with extra steps.

Rules:

1. A superseded document cannot support an assertion. It stays retrievable so
   the draft can report what it said.
2. If one value is supported *only* by internal deliberation and a competing
   value has non-internal support, the disagreement does not resolve. The two
   are not rival readings of the same evidence -- one is what the client stated,
   the other is what Blaugarnet would like to negotiate. Asserting either would
   claim an agreement the evidence does not establish.
3. Otherwise the strongest instrument wins: an executed contract outranks a
   meeting, which outranks an internal note.
4. Where instrument and audience are equal, the most recent wins.
5. Anything else is a conflict, rendered with both values and their citations.

Rule 2 is what keeps "write it my way in the draft, we'll negotiate" out of a
client-facing SOW, without the policy knowing that any such sentence exists.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import Claim, DocProvenance, Instrument, Position

# Lower is stronger. Superseded and unclassified instruments sit below
# everything so they can never win a comparison outright.
INSTRUMENT_RANK: dict[Instrument, int] = {
    "executed_contract": 0,
    "executed_sow": 1,
    "signed_addendum": 1,
    "unsigned_addendum": 2,
    "client_correspondence": 3,
    "client_meeting": 3,
    "policy": 4,
    "template": 4,
    "reference": 4,
    "internal_meeting": 5,
    "internal_chat": 5,
    "working_draft": 5,
    "superseded_addendum": 9,
    "unknown": 9,
}


@dataclass(frozen=True)
class Resolution:
    """Outcome of applying the policy to one fact key."""

    fact_key: str
    positions: list[Position]
    winner: Position | None
    reason: str
    resolved: bool

    @property
    def contested(self) -> bool:
        """True when more than one distinct value survives as support."""
        return len(self.positions) > 1


def build_positions(claims: list[Claim], provs: dict[str, DocProvenance]) -> list[Position]:
    """Group claims by normalised value into positions, with their support."""
    grouped: dict[str, list[Claim]] = {}
    for claim in claims:
        grouped.setdefault(claim.value_norm, []).append(claim)

    positions: list[Position] = []
    for value_norm, members in grouped.items():
        doc_ids = sorted({c.doc_id for c in members})
        instruments = sorted({provs[d].instrument for d in doc_ids})
        audiences = sorted({provs[d].audience for d in doc_ids})
        dates = [provs[d].doc_date for d in doc_ids if provs[d].doc_date]
        positions.append(
            Position(
                value=members[0].value,
                value_norm=value_norm,
                claim_ids=[c.claim_id for c in members],
                doc_ids=doc_ids,
                audiences=audiences,
                instruments=instruments,
                best_rank=min(INSTRUMENT_RANK.get(provs[d].instrument, 9) for d in doc_ids),
                latest_date=max(dates) if dates else None,
                internal_only=all(provs[d].audience == "internal_only" for d in doc_ids),
            )
        )

    positions.sort(key=lambda p: (p.best_rank, p.value_norm))
    return positions


def resolve(
    fact_key: str, claims: list[Claim], provs: dict[str, DocProvenance]
) -> Resolution:
    """Apply the authority policy to every claim about one fact."""
    supporting = [c for c in claims if provs[c.doc_id].status != "superseded"]
    superseded_only = bool(claims) and not supporting

    if superseded_only:
        return Resolution(
            fact_key=fact_key,
            positions=build_positions(claims, provs),
            winner=None,
            reason="every supporting document is superseded; cannot support an assertion",
            resolved=False,
        )

    positions = build_positions(supporting, provs)

    if len(positions) == 1:
        return Resolution(
            fact_key=fact_key,
            positions=positions,
            winner=positions[0],
            reason="single value; no disagreement",
            resolved=True,
        )

    # Rule 2 -- an unagreed internal position against anything else.
    internal = [p for p in positions if p.internal_only]
    external = [p for p in positions if not p.internal_only]
    if internal and external:
        return Resolution(
            fact_key=fact_key,
            positions=positions,
            winner=None,
            reason=(
                "one value is supported only by internal documents while another has "
                "client-facing or standard support; the disagreement is unresolved "
                "between the parties, not merely between sources"
            ),
            resolved=False,
        )

    # Rule 3 -- strongest instrument, if it is strictly strongest.
    best = min(p.best_rank for p in positions)
    strongest = [p for p in positions if p.best_rank == best]
    if len(strongest) == 1:
        return Resolution(
            fact_key=fact_key,
            positions=positions,
            winner=strongest[0],
            reason=(
                f"resolved by instrument: {', '.join(strongest[0].instruments)} "
                f"outranks the competing sources"
            ),
            resolved=True,
        )

    # Rule 4 -- recency, but only among equals.
    audiences = {tuple(p.audiences) for p in strongest}
    dated = [p for p in strongest if p.latest_date]
    if len(audiences) == 1 and len(dated) == len(strongest):
        newest = max(p.latest_date for p in dated)  # type: ignore[type-var]
        latest = [p for p in dated if p.latest_date == newest]
        if len(latest) == 1:
            return Resolution(
                fact_key=fact_key,
                positions=positions,
                winner=latest[0],
                reason=(
                    f"resolved by recency within equal instrument and audience: "
                    f"{newest.isoformat()}"
                ),
                resolved=True,
            )

    return Resolution(
        fact_key=fact_key,
        positions=positions,
        winner=None,
        reason="competing values of equal authority; the policy declines to choose",
        resolved=False,
    )


def is_provisional(position: Position, provs: dict[str, DocProvenance]) -> bool:
    """True when a value rests only on instruments that are not yet executed."""
    return all(provs[d].status == "out_for_signature" for d in position.doc_ids)
