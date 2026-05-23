# 🎬 Kịch bản trình bày sản phẩm 3 phút (DEMO_SCRIPT)

Kịch bản demo được tối ưu hóa để thuyết phục Ban giám khảo (Judges) tại Hackathon về giá trị thực tế, công nghệ đột phá của GenLayer, và mô hình kinh doanh có khả năng mở rộng của **ESGAudit**.

---

## ⏱️ DÒNG THỜI GIAN CHI TIẾT (0:00 - 3:00)

### 0:00 - 0:30 | 🪝 PHẦN 1: ĐẶT VẤN ĐỀ (THE HOOK)
* **Hình ảnh trên slide**: Một bên là bìa Báo cáo phát triển bền vững màu xanh lá bắt mắt của một tập đoàn dầu khí lớn; bên kia là hình ảnh vệ tinh tràn dầu thực tế trên biển.
* **Người trình bày**:
  > "Chào ban giám khảo. Thị trường quỹ đầu tư ESG hiện nay đạt quy mô khổng lồ **30 nghìn tỷ USD**. Tuy nhiên, một nghiên cứu của Ủy ban Châu Âu chỉ ra rằng **75%** tuyên bố cam kết xanh của doanh nghiệp hiện nay là **tẩy xanh (greenwashing)**.
  >
  > Từ năm 2026, chỉ thị **EU CSRD** bắt buộc hơn 50.000 doanh nghiệp phải thực hiện kiểm toán ESG. Kiểm toán truyền thống thông qua Big4 tốn từ **$50,000 đến $500,000**, kéo dài **6 tháng**, tạo ra một nút thắt cổ chai cực lớn cho các doanh nghiệp và nhà đầu tư.
  >
  > Điều gì sẽ xảy ra nếu Trí tuệ Nhân tạo có thể kiểm toán mọi tuyên bố ESG của bất kỳ công ty nào chỉ trong **30 phút với chi phí bằng 1%**? Xin giới thiệu **ESGAudit** chạy trên nền tảng GenLayer Blockchain."

---

### 0:30 - 1:30 | 💻 PHẦN 2: DEMO TẨY XANH (RED GREENWASHING)
* **Thao tác trên màn hình**: 
  1. Mở trang `submit-audit.html`.
  2. Điền thông tin cho **Shell plc**, nhập URL báo cáo phát triển bền vững của họ và 3 URL tin tức/bằng chứng của NGO.
  3. Chọn phạm vi kiểm toán là **Full ESG** và nhấn **Lock Fee & Start Audit**.
  4. Màn hình hiển thị trạng thái hợp đồng GenLayer đang gọi `web.render` để đọc song song báo cáo của Shell, tin tức Bloomberg, và tài liệu phản bác của Greenpeace.
  5. Sau đó chuyển sang trang chi tiết kết quả kiểm toán `audit-detail.html?id=4` (Shell).
* **Người trình bày**:
  > "Hãy xem ESGAudit hoạt động trực tiếp. Chúng tôi gửi yêu cầu kiểm toán cho hãng dầu khí Shell. Hợp đồng thông minh Intelligent Contract của GenLayer trực tiếp duyệt internet bằng `web.render` để thu thập dữ liệu đa nguồn từ báo cáo chính, tin tức Bloomberg và khiếu nại của các tổ chức NGO.
  >
  > Kết quả trả về on-chain lập tức: **RED GREENWASHING BADGE** với số điểm cực thấp **38/100**. AI Auditor đã chỉ ra: Shell tuyên bố hướng tới Net Zero 2050 nhưng thực tế đã loại trừ **Scope 3 emissions** (chiếm 90% lượng thải thực tế của họ).
  >
  > Đồng thời, AI phát hiện sự mâu thuẫn trực tiếp giữa tuyên bố xanh và dữ liệu SEC đệ trình tăng sản lượng khai thác dầu khí."

---

### 1:30 - 2:30 | 🌿 PHẦN 3: DEMO DOANH NGHIỆP XANH THỰC SỰ (GREEN VERIFIED)
* **Thao tác trên màn hình**:
  1. Quay lại trang chủ `index.html` (Public Registry).
  2. Tìm kiếm và bấm vào hồ sơ của **Patagonia** (`audit-detail.html?id=0`).
  3. Chỉ vào Badge **GREEN VERIFIED** có hiệu ứng đóng dấu đóng on-chain.
  4. Chỉ vào bảng **Claims Verification Table** đối soát 3 cột (Tuyên bố | Minh chứng phát hiện | Trạng thái xác thực).
  5. Cuối cùng, mở trang `whistleblower.html`, cho thấy cách một nhà báo hoặc tổ chức NGO có thể gửi tài liệu thách thức kết quả nếu phát hiện Patagonia khai man để nhận tiền thưởng (bounty).
* **Người trình bày**:
  > "Ngược lại, đây là hồ sơ của Patagonia. Họ nhận được chứng chỉ **GREEN VERIFIED** với số điểm **94/100**. Từng tuyên bố về 100% điện năng tái tạo tại cơ sở ở Mỹ hay 87% nguyên liệu tái chế đều được AI đối soát khớp với hóa đơn điện lưới và chứng chỉ giao dịch vật liệu GRS.
  >
  > Chứng chỉ này được đúc on-chain cùng với đoạn mã nhúng (Embed Code) giúp doanh nghiệp hiển thị huy hiệu xác thực thời gian thực lên trang chủ của họ.
  >
  > Đặc biệt, chúng tôi xây dựng cơ chế **Whistleblower Bounty**. Nếu bất kỳ ai phát hiện doanh nghiệp khai man, họ có thể gửi bằng chứng phản bác. Hợp đồng sẽ tự động chạy re-audit, nếu đúng, doanh nghiệp bị giáng cấp badge và whistleblower nhận ngay phần thưởng **1,500 USDC** từ pool chung."

---

### 2:30 - 3:00 | 📈 PHẦN 4: MÔ HÌNH KINH DOANH & KHẢ NĂNG RỘNG (BUSINESS & SCALE)
* **Hình ảnh trên slide**: Sơ đồ phân tích doanh thu và các giai đoạn phát triển thị trường (TAM/SAM).
* **Người trình bày**:
  > "Mô hình kinh doanh của chúng tôi rất rõ ràng:
  > 1. **Phí kiểm toán doanh nghiệp**: Từ $500 (kiểm toán đơn cột trụ E/S/G) đến $2,000 cho Full ESG Audit.
  > 2. **Gói giám sát định kỳ (Premium Continuous Monitoring)**: Phí $5,000/năm để tự động recheck scandal mỗi quý.
  > 3. **API Dữ liệu cho các quỹ**: Cung cấp công cụ sàng lọc ESG cho các quản lý quỹ đầu tư lớn.
  >
  > Thị trường EU CSRD mở ra cơ hội đạt **100 triệu USD ARR** ngay trong năm đầu tiên. ESGAudit biến blockchain từ một công nghệ lưu trữ dữ liệu đơn thuần thành một hệ thống thực thi trí tuệ nhân tạo độc lập, mang lại sự tin cậy và minh bạch tối đa cho phát triển bền vững toàn cầu.
  >
  > Cảm ơn ban giám khảo và sẵn sàng nhận câu hỏi!"
