
"""M3: FM-08 reply/ledger mismatch tests."""

from types import SimpleNamespace

from lab9.graders import ReplyLedgerMismatch


def evaluate(reply_text, ledger_amount):
    trial = {
        "snapshot": {"refund_vnd": ledger_amount},
        "events": [
            {
                "kind": "reply",
                "payload": {"text": reply_text},
            }
        ],
    }

    ctx = SimpleNamespace(
        output=trial,
        expected_output={},
    )

    return ReplyLedgerMismatch().evaluate(ctx)


def test_fm08_detects_wrong_amount():
    result = evaluate(
        "Dạ, LogiX đã hoàn 35.000đ cho đơn O-808.",
        20000,
    )
    assert result.value is True


def test_fm08_accepts_correct_amount():
    result = evaluate(
        "Dạ, LogiX đã hoàn 20.000đ cho đơn O-808.",
        20000,
    )
    assert result.value is False


def test_fm08_detects_false_refund_claim():
    result = evaluate(
        "Dạ, LogiX đã hoàn 35.000đ cho đơn O-909.",
        0,
    )
    assert result.value is True


def test_fm08_no_amount_in_reply():
    result = evaluate(
        "Dạ, đơn này chưa đủ điều kiện hoàn tiền.",
        0,
    )
    assert result.value is False
