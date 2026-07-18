"""Stability metrics. Pure functions, zero I/O, zero network.

Honours conventions preserved (METHODOLOGY_EXTRACTION.md §14.3): sets of IDs
without direction; all-pairs mean across repeats; a pair of two empty sets
scores 1.0. Goalpost extensions (DESIGN.md §4): effective n_pairs instead of
the honours ≤1-set fallback, same-decision pair filtering with discarded
fraction, coverage companions.
"""

from collections import Counter
from dataclasses import dataclass
from itertools import combinations

METRICS_VERSION = "0.1.0"


@dataclass(frozen=True)
class PairwiseStats:
    mean_jaccard: float | None
    n_pairs: int


@dataclass(frozen=True)
class SameDecisionResult:
    stats: PairwiseStats
    discarded_pair_fraction: float


@dataclass(frozen=True)
class DecisionStats:
    modal_decision: str | None
    modal_agreement: float | None
    n: int


@dataclass(frozen=True)
class CoverageCompanions:
    emptiness_rate: float
    mean_set_size: float
    empty_empty_pair_fraction: float


def jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    if not union:
        return 1.0
    return len(a & b) / len(union)


def pairwise_jaccard_stats(sets: list[set[str]]) -> PairwiseStats:
    pairs = list(combinations(sets, 2))
    if not pairs:
        return PairwiseStats(mean_jaccard=None, n_pairs=0)
    scores = [jaccard(a, b) for a, b in pairs]
    return PairwiseStats(mean_jaccard=sum(scores) / len(scores), n_pairs=len(scores))


def same_decision_pairwise_jaccard(
    sets: list[set[str]], decisions: list[str]
) -> SameDecisionResult:
    indices = list(combinations(range(len(sets)), 2))
    surviving = [(i, j) for i, j in indices if decisions[i] == decisions[j]]
    if not surviving:
        stats = PairwiseStats(mean_jaccard=None, n_pairs=0)
    else:
        scores = [jaccard(sets[i], sets[j]) for i, j in surviving]
        stats = PairwiseStats(
            mean_jaccard=sum(scores) / len(scores), n_pairs=len(scores)
        )
    discarded = (
        (len(indices) - len(surviving)) / len(indices) if indices else 0.0
    )
    return SameDecisionResult(stats=stats, discarded_pair_fraction=discarded)


def decision_stability(decisions: list[str]) -> DecisionStats:
    if not decisions:
        return DecisionStats(modal_decision=None, modal_agreement=None, n=0)
    modal_decision, modal_count = Counter(decisions).most_common(1)[0]
    return DecisionStats(
        modal_decision=modal_decision,
        modal_agreement=modal_count / len(decisions),
        n=len(decisions),
    )


def coverage_companions(sets: list[set[str]]) -> CoverageCompanions:
    n = len(sets)
    if n == 0:
        return CoverageCompanions(0.0, 0.0, 0.0)
    empties = sum(1 for s in sets if not s)
    pairs = list(combinations(sets, 2))
    empty_empty = sum(1 for a, b in pairs if not a and not b)
    return CoverageCompanions(
        emptiness_rate=empties / n,
        mean_set_size=sum(len(s) for s in sets) / n,
        empty_empty_pair_fraction=empty_empty / len(pairs) if pairs else 0.0,
    )


def direction_flip_rate(direction_maps: list[dict[str, str]]) -> float:
    """Honours definition: features seen with >1 distinct direction across
    repeats ÷ all features seen."""
    seen: dict[str, set[str]] = {}
    for mapping in direction_maps:
        for feature_id, direction in mapping.items():
            seen.setdefault(feature_id, set()).add(direction)
    if not seen:
        return 0.0
    flips = sum(1 for directions in seen.values() if len(directions) > 1)
    return flips / len(seen)


@dataclass(frozen=True)
class CaseAggregate:
    mean: float | None
    median: float | None
    iqr: tuple[float, float] | None
    n_included: int
    excluded: list[dict]


def _quantile(sorted_values: list[float], q: float) -> float:
    """Linear-interpolation quantile (matches statistics.quantiles n=4
    inclusive method for the quartile case)."""
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = q * (len(sorted_values) - 1)
    lower = int(position)
    fraction = position - lower
    upper = min(lower + 1, len(sorted_values) - 1)
    return sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction


def aggregate_cases(entries: list[dict], *, min_pairs: int) -> CaseAggregate:
    """Case → condition aggregation: unweighted mean plus median/IQR, with
    an effective-n_pairs eligibility floor; exclusions are listed, never
    silent (DESIGN.md §4, author amendment S3-3)."""
    included: list[float] = []
    excluded: list[dict] = []
    for entry in entries:
        case_id = entry.get("case_id")
        if entry.get("value") is None:
            excluded.append(
                {"case_id": case_id, "reason": "no scorable pairs"}
            )
        elif entry.get("n_pairs", 0) < min_pairs:
            excluded.append(
                {
                    "case_id": case_id,
                    "reason": f"n_pairs {entry.get('n_pairs', 0)} < {min_pairs}",
                }
            )
        else:
            included.append(entry["value"])

    if not included:
        return CaseAggregate(None, None, None, 0, excluded)

    ordered = sorted(included)
    return CaseAggregate(
        mean=sum(ordered) / len(ordered),
        median=_quantile(ordered, 0.5),
        iqr=(_quantile(ordered, 0.25), _quantile(ordered, 0.75)),
        n_included=len(ordered),
        excluded=excluded,
    )
