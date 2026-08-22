"""Stage 5 -- lexical retrieval index, plus the contamination tripwire set.

BM25 rather than embeddings. At roughly 34KB the whole corpus fits in a single
context window, so embeddings buy no recall here; they would add a dependency, a
network round-trip and run-to-run nondeterminism. The decisive reason is
narrower: a similarity score can only make another client's document unlikely,
never impossible. The engagement boundary is enforced structurally, before this
index is consulted (see ``sow.admission``), and lexical scoring only orders what
survives that boundary.

Zero third-party dependencies, so retrieval is exactly reproducible and the
recall tests run offline with no API key.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from .models import Chunk

_TOKEN = re.compile(r"[a-z0-9][a-z0-9'\-]*")

# Deliberately small. Aggressive stopping would drop "out" from "out of scope"
# and "no" from "no client".
_STOPWORDS = frozenset(
    """
    a an and are as at be been but by for from had has have he her his i if in into is it
    its of on or our ours she that the their them there these they this to was were what when
    which who will with would you your
    """.split()
)

# Calendar and generic vocabulary that survives the tripwire's set difference by
# accident rather than because it identifies another engagement.
_TRIPWIRE_STOPLIST = frozenset(
    """
    Jan Feb Mar Apr Jun Jul Aug Sep Sept Oct Nov Dec January February March April
    May June July August September October November December Monday Tuesday
    Wednesday Thursday Friday Saturday Sunday Tuesdays Thursdays
    CFO CTO CEO COO VP IT HR QA PM ERP VPN API APIs SOW MSA UAT
    Layer Operations Facilitator Distribution Overview Scope Timeline Team
    """.split()
)

# Capitalised word not at the start of a line or sentence.
_PROPER = re.compile(r"(?<![.!?|#*>\-]\s)(?<!^)\b([A-Z][a-zA-Z]{2,})\b", re.MULTILINE)


def stem(word: str) -> str:
    """Strip regular plurals only.

    Deliberately not a full stemmer: over-stemming conflates terms this corpus
    keeps distinct. Plurals alone matter because the template's guidance is
    written in the plural ("Rates", "payment terms") while the sources are
    written in the singular -- the 2026 rate card's table header says "Hourly
    rate", so without this the query term "rates" never matches the rate table
    at all, and section 8 is assembled without any actual rates in its pool.

    Words ending -ss, -us and -is are left alone, so "business", "status" and
    "analysis" survive intact.
    """
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("s") and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


def tokenize(text: str) -> list[str]:
    """Lowercase, stopped and plural-normalised tokens.

    Numbers survive deliberately: "105", "2400" and "45" are the disputed values
    in this corpus.
    """
    return [stem(t) for t in _TOKEN.findall(text.lower()) if t not in _STOPWORDS]


class Bm25Index:
    """Okapi BM25 over chunk text. Hand-rolled to keep the dependency list empty."""

    def __init__(
        self,
        chunks: list[Chunk],
        retrieval_texts: list[str] | None = None,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        """Build the index.

        Args:
            retrieval_texts: what to index per chunk, parallel to ``chunks``.
                Defaults to the chunk text itself. Callers pass an enriched
                field -- document title plus heading path plus text -- because a
                rate card's table body scores almost nothing against the query
                "rates" while its title, "Standard Rate Card 2026", scores well.
                Citation text still comes from ``Chunk.text``, which stays
                verbatim.
        """
        if not chunks:
            raise ValueError("cannot build an index over zero chunks")
        if retrieval_texts is not None and len(retrieval_texts) != len(chunks):
            raise ValueError("retrieval_texts must be parallel to chunks")
        self.chunks = chunks
        self.k1 = k1
        self.b = b

        fields = retrieval_texts if retrieval_texts is not None else [c.text for c in chunks]
        self._tokens: list[list[str]] = [tokenize(t) for t in fields]
        self._freqs: list[Counter[str]] = [Counter(t) for t in self._tokens]
        self._lengths: list[int] = [len(t) for t in self._tokens]
        self._avg_len = sum(self._lengths) / len(self._lengths) if self._lengths else 0.0

        doc_freq: Counter[str] = Counter()
        for tokens in self._tokens:
            doc_freq.update(set(tokens))

        n = len(chunks)
        self._idf = {
            term: math.log(1.0 + (n - df + 0.5) / (df + 0.5)) for term, df in doc_freq.items()
        }

    def search(
        self, query: str, top_k: int, allowed: set[str] | None = None
    ) -> list[tuple[Chunk, float]]:
        """Rank chunks against a query.

        Args:
            allowed: if given, only these chunk ids may be returned. This is a
                second, redundant guard -- the index is normally built over
                admitted chunks only.
        """
        terms = tokenize(query)
        if not terms:
            return []

        scored: list[tuple[Chunk, float]] = []
        for idx, chunk in enumerate(self.chunks):
            if allowed is not None and chunk.chunk_id not in allowed:
                continue
            score = self._score(idx, terms)
            if score > 0.0:
                scored.append((chunk, score))

        scored.sort(key=lambda pair: (-pair[1], pair[0].chunk_id))
        return scored[:top_k]

    def _score(self, idx: int, terms: list[str]) -> float:
        """BM25 score of one chunk against query terms."""
        freqs = self._freqs[idx]
        length = self._lengths[idx]
        norm = self.k1 * (1 - self.b + self.b * (length / self._avg_len)) if self._avg_len else self.k1

        total = 0.0
        for term in terms:
            tf = freqs.get(term, 0)
            if not tf:
                continue
            total += self._idf.get(term, 0.0) * (tf * (self.k1 + 1)) / (tf + norm)
        return total


def build_tripwire_terms(
    admitted_docs_text: dict[str, str], excluded_docs_text: dict[str, str]
) -> list[str]:
    """Proper nouns that occur only in excluded documents.

    Derived by set difference rather than hand-authored, then filtered against a
    calendar and generic stoplist.

    This check is advisory, not the guarantee. It cannot catch "Northgate" or
    "105", both of which also appear inside admitted Harding documents -- the
    first in a chat message, the second in the retracted passage of the scoping
    call. Those are conflicts to be detected from evidence, not contamination to
    be filtered. The structural guarantee is that every citation must resolve to
    an admitted chunk.

    The admitted side must include the SOW template even though the template is
    never evidence. Without it, "Milestones" and "Objectives" appear only in
    another client's executed SOW and become tripwire terms -- so the check would
    fire on any draft that uses the section headings it was told to use.
    """
    admitted_text = "\n".join(admitted_docs_text.values())
    admitted_lower = set(tokenize(admitted_text))
    admitted_proper = set(_PROPER.findall(admitted_text))

    excluded_proper: set[str] = set()
    for text in excluded_docs_text.values():
        excluded_proper.update(_PROPER.findall(text))

    return sorted(
        term
        for term in excluded_proper - admitted_proper
        if term not in _TRIPWIRE_STOPLIST and stem(term.lower()) not in admitted_lower
    )
