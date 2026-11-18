"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """TP/FP/FN/TN, with FAIL as the positive class."""
    if len(human) != len(judge):
        raise ValueError("Human and judge labels must have equal lengths")

    cm = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}

    for h, j in zip(human, judge):
        h = h.strip().upper()
        j = j.strip().upper()

        if h not in ("PASS", "FAIL") or j not in ("PASS", "FAIL"):
            raise ValueError(f"Invalid labels: human={h}, judge={j}")

        if h == "FAIL" and j == "FAIL":
            cm["tp"] += 1
        elif h == "PASS" and j == "FAIL":
            cm["fp"] += 1
        elif h == "FAIL" and j == "PASS":
            cm["fn"] += 1
        else:
            cm["tn"] += 1

    return cm


def precision_recall(
    human: Sequence[str],
    judge: Sequence[str],
) -> tuple[float, float]:
    """Precision and recall for detecting FAIL."""
    cm = confusion(human, judge)

    tp = cm["tp"]
    fp = cm["fp"]
    fn = cm["fn"]

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """Agreement beyond chance, with FAIL as positive."""
    cm = confusion(human, judge)

    tp = cm["tp"]
    fp = cm["fp"]
    fn = cm["fn"]
    tn = cm["tn"]

    n = tp + fp + fn + tn
    if n == 0:
        raise ValueError("Kappa undefined for empty labels")

    # Observed agreement.
    p_o = (tp + tn) / n

    # Expected agreement by chance.
    human_fail = (tp + fn) / n
    judge_fail = (tp + fp) / n

    human_pass = (tn + fp) / n
    judge_pass = (tn + fn) / n

    p_e = (
        human_fail * judge_fail
        + human_pass * judge_pass
    )

    if abs(1.0 - p_e) < 1e-12:
        raise ValueError("Kappa undefined when expected agreement is 1")

    return (p_o - p_e) / (1.0 - p_e)


def rogan_gladen(
    observed_rate: float,
    sensitivity: float,
    specificity: float,
) -> float:
    """Estimate true FAIL prevalence after correcting judge errors."""
    if not all(
        0.0 <= x <= 1.0
        for x in (observed_rate, sensitivity, specificity)
    ):
        raise ValueError("Rates must be between 0 and 1")

    denominator = sensitivity + specificity - 1.0

    if abs(denominator) < 1e-12:
        raise ValueError("Rogan-Gladen undefined: judge has no usable discrimination")

    corrected = (
        observed_rate + specificity - 1.0
    ) / denominator

    return max(0.0, min(1.0, corrected))




def paired_bootstrap(
    a: Sequence[float],
    b: Sequence[float],
    *,
    n_resamples: int = 1000,
    rng: int = 2027,
    confidence: float = 0.95,
) -> tuple[float, float, float]:
    """Paired bootstrap confidence interval for mean(a) - mean(b).

    a[i] and b[i] must represent the same evaluation item.
    Returns (mean_difference, lower_bound, upper_bound).
    """
    import numpy as np
    from scipy.stats import bootstrap

    if len(a) != len(b):
        raise ValueError("Paired samples must have equal lengths")

    if len(a) == 0:
        raise ValueError("Samples cannot be empty")

    if n_resamples <= 0:
        raise ValueError("n_resamples must be positive")

    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")

    arr_a = np.asarray(a, dtype=float)
    arr_b = np.asarray(b, dtype=float)

    if np.array_equal(arr_a, arr_b):
        return (0.0, 0.0, 0.0)

    difference = float(np.mean(arr_a) - np.mean(arr_b))

    result = bootstrap(
        (arr_a, arr_b),
        statistic=lambda x, y: np.mean(x) - np.mean(y),
        paired=True,
        vectorized=False,
        n_resamples=n_resamples,
        confidence_level=confidence,
        method="percentile",
        rng=np.random.default_rng(rng),
    )

    return (
        difference,
        float(result.confidence_interval.low),
        float(result.confidence_interval.high),
    )


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
