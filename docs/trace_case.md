# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 55
python -m lab9.trace_case --shape fixed --claim C-002 --seed 55   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Mẫu điền (mỗi nhóm 1 case, lấy từ trial đang fail trong report)

| Trường | Nội dung |
| :--- | :--- |
| Trial | `seeded_regression C-002@55`. Run ID chưa được xác minh từ report. |
| Triệu chứng | Grader FAIL: `status resolved != denied`. Reply thông báo hoàn 20.000đ; ledger thực tế ghi một refund 20.000đ, trong khi nhãn yêu cầu 0đ. |
| Bước sai đầu tiên | Event **3 — `model_override`** — `{"delay_days": 5}`. |
| Vì sao là bước *đầu tiên* | Event 1 `handoff` giao nhiệm vụ; event 2 `investigator` tra cứu đơn hàng. Event 3 lần đầu xuất hiện việc ghi đè ngày giao trễ bằng thông tin từ ticket, dẫn đến `quote` 20.000đ ở event 4. |
| Failure mode | **FM-03 — `ticket_trust`** |
| Đối chứng | `fixed C-002@55`: không có `model_override`; event 3 `quote` trả 0đ với `reason = no_entitlement`. Grader PASS, `status = denied`, ledger = 0đ. |
| Regression test | `tests/test_lab9_ticket_trust_regression.py::test_c002_ticket_trust_seed55` — **PASSED**. Test xác nhận `seeded_regression` FAIL và `fixed` PASS. |
| Chưa chắc chắn | Chưa có run ID từ report; output trace rút gọn chưa chứng minh toàn bộ logic nội bộ của Agent. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.