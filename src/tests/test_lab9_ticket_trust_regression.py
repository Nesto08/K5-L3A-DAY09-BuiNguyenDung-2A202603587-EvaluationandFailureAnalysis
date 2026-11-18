
"""M1 regression test: ticket must not override verified order data."""

import subprocess
import sys



def run_trace(shape: str, claim: str = "C-002", seed: int = 55) -> str:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "lab9.trace_case",
            "--shape", shape,
            "--claim", claim,
            "--seed", str(seed),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return result.stdout


def test_c002_ticket_trust_seed55():
    """Regression variant fails; fixed variant passes the Lab 8 grader."""
    broken = run_trace("seeded_regression")
    fixed = run_trace("fixed")

    # The regression must be detectable.
    assert "grader: FAIL" in broken
    assert "status resolved != denied" in broken
    assert "model_override" in broken
    assert '"delay_days": 5' in broken
    assert "ledger=20000" in broken

    # The fixed version must satisfy the expected outcome.
    assert "grader: PASS" in fixed
    assert "result=denied" in fixed
    assert "label=denied" in fixed
    assert "ledger=0" in fixed
    assert "unexpected ledger rows: 0" in fixed
    assert "model_override" not in fixed



def test_c007_denied_reply_regression():
    broken = run_trace("seeded_regression", "C-007")
    fixed = run_trace("fixed", "C-007")

    assert "grader: FAIL" in broken
    assert "result=resolved" in broken
    assert "label=denied" in broken
    assert "ledger=0" in broken
    assert "đã hoàn 35.000đ" in broken

    assert "grader: PASS" in fixed
    assert "result=denied" in fixed
    assert "ledger=0" in fixed


def test_c014_double_deduction_regression():
    broken = run_trace("seeded_regression", "C-014")
    fixed = run_trace("fixed", "C-014")

    assert "grader: FAIL (proposal_mismatch)" in broken
    assert "ledger=90000" in broken
    assert "label=120000" in broken

    assert "grader: PASS" in fixed
    assert "ledger=120000" in fixed
    assert "label=120000" in fixed
