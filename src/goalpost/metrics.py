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

METRICS_VERSION = "0.2.0"
BINARY_DIRECTIONS = frozenset({"positive", "negative"})


@dataclass(frozen=True)
class PairwiseStats:
    mean_jaccard: float | None
    n_pairs: int


@dataclass(frozen=True)
class SameDecisionResult:
    stats: PairwiseStats
    discarded_pair_fraction: float | None


@dataclass(frozen=True)
class DecisionStats:
    modal_decision: str | None
    modal_agreement: float | None
    n: int


@dataclass(frozen=True)
class CoverageCompanions:
    emptiness_rate: float | None
    mean_set_size: float | None
    empty_empty_pair_fraction: float | None


@dataclass(frozen=True)
class TopicDirectionStats:
    """Legacy per-case topic reversal incidence and its denominator."""

    rate: float | None
    n_topics: int
    n_reversal_topics: int


@dataclass(frozen=True)
class DirectionPairStats:
    """Opposite-direction rate with every eligibility count exposed."""

    rate: float | None
    n_opposite_direction_comparisons: int
    n_unambiguous_shared_topic_comparisons: int
    n_ambiguous_shared_topic_comparisons: int
    n_contributing_run_pairs: int
    n_same_decision_run_pairs: int


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
        (len(indices) - len(surviving)) / len(indices) if indices else None
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
        return CoverageCompanions(None, None, None)
    empties = sum(1 for s in sets if not s)
    pairs = list(combinations(sets, 2))
    empty_empty = sum(1 for a, b in pairs if not a and not b)
    return CoverageCompanions(
        emptiness_rate=empties / n,
        mean_set_size=sum(len(s) for s in sets) / n,
        empty_empty_pair_fraction=empty_empty / len(pairs) if pairs else None,
    )


def _direction_set(value: str | set[str]) -> set[str]:
    return {value} if isinstance(value, str) else set(value)


def direction_flip_rate(
    direction_maps: list[dict[str, str | set[str]]],
) -> float:
    """Compatibility scalar for Goalpost v0.1's topic denominator.

    New metrics artifacts use :func:`legacy_topic_reversal_incidence_stats` so
    the denominator and its size cannot be mistaken for run pairs. The scalar
    remains for compatibility with pre-0.2.0 callers.
    """
    stats = legacy_topic_reversal_incidence_stats(direction_maps)
    return stats.rate if stats.rate is not None else 0.0


def legacy_topic_reversal_incidence_stats(
    direction_maps: list[dict[str, str | set[str]]],
) -> TopicDirectionStats:
    """Share of distinct topics that take more than one direction.

    This preserves Goalpost v0.1's operationalisation as a labelled secondary
    measure. The dissertation evidence did not specify its denominator. It is
    not a count of run pairs or topic-in-run-pair comparisons.
    """
    seen: dict[str, set[str]] = {}
    for mapping in direction_maps:
        for feature_id, directions in mapping.items():
            seen.setdefault(feature_id, set()).update(_direction_set(directions))
    if not seen:
        return TopicDirectionStats(
            rate=None,
            n_topics=0,
            n_reversal_topics=0,
        )
    flips = sum(1 for directions in seen.values() if len(directions) > 1)
    return TopicDirectionStats(
        rate=flips / len(seen),
        n_topics=len(seen),
        n_reversal_topics=flips,
    )


def shared_topic_direction_disagreement(
    direction_maps: list[dict[str, set[str]]], decisions: list[str]
) -> DirectionPairStats:
    """Opposite-direction rate over unambiguous shared-topic comparisons.

    For every same-decision scored-run pair, a topic present in both runs is
    scorable only when each run assigns it exactly one direction. Mixed-sign
    topic states are retained and counted as ambiguous exclusions rather than
    resolved by item order. A run pair contributes to the effective-pair floor
    only if it supplies at least one unambiguous shared-topic comparison.
    """
    if len(direction_maps) != len(decisions):
        raise ValueError("direction_maps and decisions must have equal length")

    comparisons = disagreements = ambiguous = 0
    same_decision_run_pairs = contributing_run_pairs = 0
    for left, right in combinations(range(len(direction_maps)), 2):
        if decisions[left] != decisions[right]:
            continue
        same_decision_run_pairs += 1
        shared_topics = direction_maps[left].keys() & direction_maps[right].keys()
        contributed = False
        for topic in shared_topics:
            left_directions = _direction_set(direction_maps[left][topic])
            right_directions = _direction_set(direction_maps[right][topic])
            if (
                len(left_directions) != 1
                or len(right_directions) != 1
                or not left_directions <= BINARY_DIRECTIONS
                or not right_directions <= BINARY_DIRECTIONS
            ):
                ambiguous += 1
                continue
            contributed = True
            comparisons += 1
            disagreements += left_directions != right_directions
        if contributed:
            contributing_run_pairs += 1

    return DirectionPairStats(
        rate=disagreements / comparisons if comparisons else None,
        n_opposite_direction_comparisons=disagreements,
        n_unambiguous_shared_topic_comparisons=comparisons,
        n_ambiguous_shared_topic_comparisons=ambiguous,
        n_contributing_run_pairs=contributing_run_pairs,
        n_same_decision_run_pairs=same_decision_run_pairs,
    )


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
