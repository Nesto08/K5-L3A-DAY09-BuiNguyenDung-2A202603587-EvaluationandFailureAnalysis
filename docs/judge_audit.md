# Judge audit

Chạy:

```bash
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 5
```

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | Có — đạt cả ba ngưỡng | Dùng có giám sát |
| helpful | 100 | 0.375 | 1.000 | 0.300 | Không — Kappa và Recall dưới ngưỡng | Loại khỏi gate tự động |

## ≥5 case audit thủ công

| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 (tone_ok) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Judge bỏ sót phản hồi tuyên bố đã hoàn tiền; cần đối chiếu rubric tone để kết luận độc lập về nội dung. |
| 2 | H-017 (tone_ok) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Judge chấp nhận phản hồi về khoản hoàn 25.000đ cho O-606, trái nhãn Human. |
| 3 | H-029 (tone_ok) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Reply yêu cầu khách hàng chờ và không nhắn thêm; Judge bỏ sót phản hồi được Human đánh FAIL. |
| 4 | H-042 (tone_ok) | FAIL | PASS | Human (nhãn tham chiếu) | False Positive. Judge đánh FAIL phản hồi thông báo hoàn 120.000đ và thời gian nhận tiền, trong khi Human đánh PASS. |
| 5 | H-051 (tone_ok) | FAIL | PASS | Human (nhãn tham chiếu) | False Positive. Judge đánh FAIL phản hồi thông báo hoàn 90.000đ, trái nhãn Human. |
| 6 | HL-015 (helpful) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Judge bỏ sót một phản hồi không đạt helpfulness theo nhãn chuẩn. |
| 7 | HL-016 (helpful) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Phản hồi xin lỗi và cảm ơn sự kiên nhẫn; cần kiểm tra liệu có hướng dẫn xử lý cụ thể hay không. |
| 8 | HL-020 (helpful) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Judge chấp nhận một phản hồi thông báo hoàn tiền dù Human đánh FAIL. |
| 9 | HL-028 (helpful) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Phản hồi xin lỗi lịch sự nhưng có thể thiếu thông tin hữu ích; cần xem toàn bộ reply. |
| 10 | HL-035 (helpful) | PASS | FAIL | Human (nhãn tham chiếu) | False Negative. Phản hồi xin lỗi khách hàng được Judge đánh PASS nhưng Human đánh FAIL. |

## Kết luận

### 1. Đánh giá tone_ok

- Confusion matrix: TP=24, FP=4, FN=6, TN=66.
- Precision=0.857, Recall=0.800, Cohen's Kappa=0.757.
- Tỷ lệ FAIL quan sát được: 0.280.
- Tỷ lệ FAIL sau hiệu chỉnh Rogan–Gladen: 0.300.
- **Quyết định:** đạt ngưỡng calibration; có thể sử dụng làm tín hiệu đánh giá tone, nhưng không thay thế kiểm tra bằng code với các quyết định tài chính và approval.

### 2. Đánh giá helpful

- Confusion matrix: TP=9, FP=0, FN=21, TN=70.
- Precision=1.000, Recall=0.300, Cohen's Kappa=0.375.
- Tỷ lệ FAIL quan sát được: 0.090.
- Tỷ lệ FAIL sau hiệu chỉnh Rogan–Gladen: 0.300.
- **Quyết định:** loại khỏi gate tự động do Recall và Kappa không đạt ngưỡng.

Judge `helpful` bỏ sót 21/30 trường hợp FAIL. Precision cao không bù đắp được khả năng phát hiện lỗi thấp.

### 3. Rủi ro còn lại

- Dữ liệu calibration sử dụng replay CSV công khai, chưa phải held-out độc lập.
- Các trường hợp bất đồng được phân loại theo nhãn Human; cần rubric và nội dung đầy đủ để đưa ra nhận định thủ công độc lập.
- Hiệu chỉnh Rogan–Gladen phụ thuộc vào ước lượng sensitivity và specificity từ tập calibration, có thể thay đổi khi phân phối dữ liệu thay đổi.
- Cần đánh giá lại trên dữ liệu mới có nhãn Human trước khi triển khai thực tế.
- Các kiểm tra về số tiền hoàn, approval và refund ledger phải dùng code grader thay vì chỉ dựa vào LLM Judge.