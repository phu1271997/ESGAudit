# 🧪 Kịch bản kiểm thử luồng nghiệp vụ trên GenLayer Studio (test_flow)

Tài liệu này chứa hướng dẫn chi tiết về 7 kịch bản kiểm thử thực tế trên giao diện debug của GenLayer Studio nhằm giả lập đầy đủ các khía cạnh nghiệp vụ của hệ thống **ESGAudit**.

---

## 📋 Kịch bản 1: Kiểm toán thành công (Happy Path - GREEN verified)
* **Mục tiêu**: Xác thực quy trình kiểm toán một công ty xanh thực tế (ví dụ: Patagonia, Ørsted) và nhận được chứng nhận GREEN VERIFIED.
* **Các bước thực hiện**:
  1. Gọi hàm `register_company("Patagonia")` bằng tài khoản doanh nghiệp.
  2. Gọi `submit_audit(company_name="Patagonia", report_url="https://www.patagonia.com/environmental-responsibility-report.html", evidence_urls='["https://www.verra.org/registry/patagonia-carbon-offsets-02", "https://www.greenpeace.org/usa/reports/patagonia-supply-chain-2025", "https://www.cdp.net/en/companies/patagonia"]', audit_scope="ALL", fee_paid=2000)`.
  3. Kiểm tra xem giao dịch có sinh ra `audit_id` (ví dụ: `0`) không.
  4. Gọi hàm `trigger_ai_audit(0)`. Theo dõi logs giao dịch.
* **Kết quả kỳ vọng**:
  * AI trả về phán quyết JSON có `"verdict": "GREEN_VERIFIED"` với số điểm từ 85 - 95.
  * Hợp đồng tự động thêm Patagonia vào danh sách `verified_companies`.
  * Huy hiệu GREEN được ghi nhận on-chain cho Patagonia.

---

## 📋 Kịch bản 2: Phát hiện tẩy xanh (Greenwashing detection)
* **Mục tiêu**: Đánh giá báo cáo của một tập đoàn dầu khí lớn có hành vi tẩy xanh và phát cảnh báo RED.
* **Các bước thực hiện**:
  1. Gửi báo cáo của Shell bằng cách gọi `submit_audit(company_name="Shell plc", report_url="https://www.shell.com/sustainability/reports/annual-report-2025.html", evidence_urls='["https://www.reuters.com/business/sustainable-business/shell-court-case-appeals-ruling-2026", "https://www.greenpeace.org.uk/news/shell-greenwashing-complaint-advertising-standards", "https://www.sec.gov/edgar/shell-2025-filing"]', audit_scope="ALL", fee_paid=2000)`.
  2. Nhận `audit_id` (ví dụ: `1`).
  3. Gọi hàm `trigger_ai_audit(1)`.
* **Kết quả kỳ vọng**:
  * AI Consensus phát hiện Shell che giấu Scope 3 emissions và sử dụng từ ngữ mơ hồ.
  * Trả về JSON có `"verdict": "RED_GREENWASHING"`, điểm số < 45.
  * Xuất hiện các thẻ cảnh báo `"MISSING_SCOPE3"` và `"VAGUE_LANGUAGE"` trong mảng `greenwashing_indicators`.
  * Hợp đồng không đưa Shell vào danh sách xanh.

---

## 📋 Kịch bản 3: Chứng chỉ có điều kiện (Yellow conditional)
* **Mục tiêu**: Đánh giá doanh nghiệp công nghệ lớn có báo cáo tương đối tốt nhưng thiếu kiểm toán bên thứ ba độc lập hoặc thiếu một số chỉ báo chuỗi cung ứng.
* **Các bước thực hiện**:
  1. Gọi `submit_audit` cho Tesla với các liên kết tương ứng.
  2. Gọi `trigger_ai_audit(audit_id)`.
* **Kết quả kỳ vọng**:
  * Trả về điểm số trong khoảng 50 - 79 với `"verdict": "YELLOW_CONDITIONAL"`.
  * AI đưa ra khuyến nghị cải thiện cụ thể (Ví dụ: "Yêu cầu thực hiện kiểm toán độc lập bên thứ 3 đối với chuỗi cung ứng cobalt").

---

## 📋 Kịch bản 4: Whistleblower Thổi còi thử thách (Whistleblower challenge)
* **Mục tiêu**: Kiểm tra tính năng phản biện từ cộng đồng. Một tổ chức phi chính phủ gửi bằng chứng chứng minh doanh nghiệp khai man và cập nhật lại badge on-chain.
* **Các bước thực hiện**:
  1. Giả sử Apple trước đó có chứng chỉ GREEN (hoặc YELLOW cao).
  2. Một Whistleblower gọi `submit_challenge(audit_id=3, evidence_url="https://www.financialtimes.com/content/apple-supply-chain-carbon-credits", reason="Bằng chứng từ báo chí chỉ ra các chứng chỉ carbon của Apple là trùng lặp và không có tính bổ sung (additionality).")`.
  3. Hệ thống trả về `challenge_id` (ví dụ: `0`).
  4. Gọi hàm `process_challenge(0)`.
* **Kết quả kỳ vọng**:
  * AI Recheck xác nhận bằng chứng phản bác là đúng sự thật (`challenge_valid: true`).
  * Điểm số của Apple bị giảm đi và badge chuyển từ GREEN sang YELLOW hoặc RED.
  * Whistleblower nhận được thưởng USDC (bounty) từ pool.

---

## 📋 Kịch bản 5: Kiểm toán đơn cột trụ (Single pillar audit)
* **Mục tiêu**: Doanh nghiệp chỉ muốn kiểm toán khía cạnh Quản trị (Governance) để giảm chi phí gas và phí dịch vụ.
* **Các bước thực hiện**:
  1. Gọi `submit_audit` với tham số `audit_scope="G"`.
  2. Gọi `trigger_ai_audit(audit_id)`.
* **Kết quả kỳ vọng**:
  * AI chỉ đánh giá các tiêu chí liên quan đến cấu trúc hội đồng quản trị, lương ban điều hành và phòng chống tham nhũng.
  * Các trường chấm điểm củaEnvironmental và Social được để mặc định hoặc bằng 0.

---

## 📋 Kịch bản 6: Giám sát liên tục định kỳ (Continuous monitoring)
* **Mục tiêu**: Kiểm tra tính năng tự động quét thông tin hàng quý đối với các doanh nghiệp trả phí Premium.
* **Các bước thực hiện**:
  1. Doanh nghiệp gọi `subscribe_continuous_monitoring(company_name="Patagonia", months=12)`.
  2. Xác minh xem Patagonia có được lưu trữ thời gian hết hạn tương ứng trong storage `audit_subscription` không.
  3. Giả lập một quý trôi qua, gọi `trigger_quarterly_recheck("Patagonia")`.
* **Kết quả kỳ vọng**:
  * Hệ thống tự động cào tin tức mới nhất về Patagonia. Do không phát hiện scandal nghiêm trọng, trạng thái giữ nguyên.

---

## 📋 Kịch bản 7: Xử lý sự cố mạng (Graceful handling of paywalled/failed sources)
* **Mục tiêu**: Kiểm tra độ bền vững (robustness) của hợp đồng khi một trong số các URL minh chứng bị chặn hoặc lỗi đường truyền.
* **Các bước thực hiện**:
  1. Gửi audit với một URL lỗi (Ví dụ: `https://www.nonexistent-domain-123.com/report.html` hoặc link Financial Times bị chặn tường phí).
  2. Gọi `trigger_ai_audit()`.
* **Kết quả kỳ vọng**:
  * Hợp đồng không bị crash (không dừng giao dịch đột ngột). Vòng lặp đọc dữ liệu bắt được lỗi của URL bị hỏng qua cấu trúc `try-except` trong hàm leader.
  * Các nguồn khác vẫn được AI đọc và phân tích bình thường.
  * AI ghi nhận nguồn lỗi vào báo cáo hoặc giảm nhẹ điểm tin cậy `confidence_score`.
