# 🌿 Các Khung Tiêu Chuẩn ESG & Diễn Giải Thuật Ngữ (ESG_FRAMEWORK)

Tài liệu này giải thích các tiêu chuẩn ESG quốc tế (GRI, SASB, TCFD) mà hệ thống AI của **ESGAudit** dùng để đối chiếu khi đánh giá hồ sơ doanh nghiệp.

---

## 📋 1. Diễn giải 3 Khung tiêu chuẩn ESG chính

### GRI (Global Reporting Initiative) — Tiêu chuẩn Tác động
* **Mô tả**: Đây là khung tiêu chuẩn kiểm toán ESG phổ biến nhất thế giới. GRI tập trung vào việc đo lường **tác động của doanh nghiệp đối với nền kinh tế, môi trường và con người**.
* **AI đối soát chỉ số**:
  * Các chỉ số về lượng phát thải trực tiếp (GRI 305).
  * Tiêu thụ năng lượng, đa dạng sinh học và nguồn nước sạch.
  * Phúc lợi lao động, tỷ lệ tai nạn nghề nghiệp và bình đẳng cơ hội.

### SASB (Sustainability Accounting Standards Board) — Tiêu chuẩn Tài chính
* **Mô tả**: SASB được chia nhỏ chi tiết theo **77 ngành công nghiệp khác nhau**. SASB tập trung vào các vấn đề ESG có **khả năng tác động trực tiếp đến tình hình tài chính** của doanh nghiệp.
* **AI đối soát chỉ số**:
  * Rủi ro chuỗi cung ứng lithium đối với hãng xe điện EV.
  * Chi phí tuân thủ quản lý chất thải nguy hại của hãng điện tử.
  * Rủi ro dữ liệu người dùng đối với các công ty công nghệ SaaS.

### TCFD (Task Force on Climate-related Financial Disclosures) — Tiêu chuẩn Rủi ro Khí hậu
* **Mô tả**: TCFD tập trung hoàn toàn vào việc giúp các nhà đầu tư hiểu được **công ty quản lý các rủi ro liên quan đến biến đổi khí hậu như thế nào** thông qua 4 cột trụ: Quản trị (Governance), Chiến lược (Strategy), Quản lý Rủi ro (Risk Management), và Chỉ số & Mục tiêu (Metrics and Targets).
* **AI đối soát chỉ số**:
  * Dự báo thiệt hại của nhà máy ven biển khi nước biển dâng.
  * Mục tiêu cắt giảm khí nhà kính và tỷ lệ carbon bù đắp.

---

## 📖 2. Thuật ngữ cốt lõi (Glossary)

### Scope 1, 2, 3 Emissions là gì?
* **Scope 1 (Phát thải trực tiếp)**: Khí thải sinh ra trực tiếp từ các nguồn sở hữu bởi công ty (ví dụ: khói lò hơi, khí thải từ xe tải chở hàng của hãng).
* **Scope 2 (Phát thải gián tiếp từ năng lượng)**: Khí thải gián tiếp từ việc tiêu thụ điện, nhiệt, hơi nước mà doanh nghiệp mua từ công ty điện lực.
* **Scope 3 (Phát thải chuỗi giá trị - Rất quan trọng)**: Toàn bộ lượng khí thải gián tiếp xảy ra trong chuỗi cung ứng của công ty (từ việc khai thác nguyên liệu thô của nhà cung cấp) cho đến quá trình tiêu thụ sản phẩm của người dùng cuối (ví dụ: lượng xăng xe chạy cho xe của hãng sản xuất ra).
  * *Lưu ý*: Scope 3 thường chiếm **80% - 95%** lượng khí thải của doanh nghiệp, nhưng thường bị che giấu hoặc bỏ qua (đây là chỉ dấu tẩy xanh lớn nhất).

### Materiality (Tính trọng yếu) & Double Materiality (Tính trọng yếu kép)
* **Materiality**: Một vấn đề được coi là trọng yếu nếu việc công bố nó ảnh hưởng đến quyết định kinh tế của nhà đầu tư.
* **Double Materiality (Trọng yếu kép)**: Yêu cầu của EU CSRD, bắt buộc công ty báo cáo hai chiều:
  1. Biến đổi khí hậu ảnh hưởng thế nào đến tài chính công ty (Outside-in).
  2. Hoạt động của công ty ảnh hưởng thế nào đến môi trường và xã hội (Inside-out).

### Carbon Offsets (Bù đắp Carbon) & Additionality (Tính bổ sung)
* **Carbon Offset**: Việc doanh nghiệp mua chứng chỉ carbon (ví dụ: dự án trồng rừng) để bù trừ cho lượng phát thải của mình nhằm tuyên bố đạt "Carbon Neutral".
* **Additionality**: Dự án bù đắp carbon chỉ có giá trị thực tế nếu lượng khí thải giảm đi **là nhờ có nguồn tiền tài trợ của dự án**, chứ không phải là lượng cây tự nhiên sẵn có được quây rào lại để bán chứng chỉ (tình trạng bán chứng chỉ ma).

---

## 🔗 3. Liên kết tài liệu chính thức (Official Standards)

* **GRI Standards**: [https://www.globalreporting.org/how-to-use-the-gri-standards](https://www.globalreporting.org/how-to-use-the-gri-standards)
* **SASB Standards Reference**: [https://sasb.org/standards](https://sasb.org/standards)
* **TCFD Recommendations**: [https://www.fsb-tcfd.org](https://www.fsb-tcfd.org)
* **European CSRD Regulation**: [https://finance.ec.europa.eu/capital-markets-union-and-financial-services/corporate-reporting/corporate-sustainability-reporting](https://finance.ec.europa.eu/capital-markets-union-and-financial-services/corporate-reporting/corporate-sustainability-reporting)
