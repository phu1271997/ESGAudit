# 🌿 ESGAudit — AI-Powered ESG Verification & Greenwashing Detection on GenLayer

```text
 _____ ____   ____    _              _ _ _
| ____/ ___| / ___|  / \  _   _  __| (_) |_
|  _| \___ \| |  _  / _ \| | | |/ _` | | __|
| |___ ___) | |_| |/ ___ \ |_| | (_| | | |_
|_____|____/ \____/_/   \_\__,_|\__,_|_|\__|
```

> **$50K Big4 ESG audits in 30 minutes for $500.**
> AI đọc báo cáo doanh nghiệp + tin tức + dữ liệu NGO, phát hiện hành vi tẩy xanh (greenwashing) sử dụng khung đánh giá GRI/SASB/TCFD, đúc các chứng chỉ xác thực on-chain. Sẵn sàng cho EU CSRD. Phát triển trên GenLayer.

---

## 🚀 Tổng quan dự án

**ESGAudit** là một ứng dụng phi tập trung (dApp) hoạt động trên mạng lưới **GenLayer Blockchain** — một nền tảng hợp đồng thông minh tiên tiến thế hệ mới (Intelligent Contracts) viết bằng Python. Dựa trên hai khả năng đột phá của GenLayer:
1. `gl.nondet.web.render(url, mode="text")`: Hợp đồng tự duyệt và đọc dữ liệu từ Internet (báo cáo phát triển bền vững PDF/HTML, tin tức Bloomberg/Reuters, dữ liệu vệ tinh Global Forest Watch, báo cáo từ các tổ chức phi chính phủ NGO).
2. `gl.nondet.exec_prompt(task, response_format="json")`: Hợp đồng trực tiếp gọi LLM để đóng vai trò là một chuyên gia kiểm toán ESG cao cấp (đạt chuẩn KPMG/Deloitte) nhằm phân tích hành vi tẩy xanh và ra phán quyết on-chain.

Hệ thống giúp tự động hóa quy trình kiểm toán ESG vốn rất tốn kém và chậm chạp, đồng thời mang lại sự minh bạch tuyệt đối cho thị trường vốn ESG trị giá 30 nghìn tỷ USD và thị trường Carbon Credit trị giá 30 tỷ USD.

---

## 🛠️ Công nghệ sử dụng

- **Smart Contracts**: Python (GenLayer SDK v0.2.16)
- **Frontend**: HTML5, Vanilla CSS3 (Giao diện Dark Forest Green & Earth tones sang trọng, hiện đại), JavaScript ES6.
- **AI Engine**: Llama 3 / GPT-4 (Tích hợp thông qua cơ chế đồng thuận AI của GenLayer).
- **Tiêu chuẩn kiểm toán**: GRI (Global Reporting Initiative), SASB (Sustainability Accounting Standards Board), TCFD (Task Force on Climate-related Financial Disclosures).

---

## 📂 Cấu trúc thư mục

```text
ESGAudit/
├── README.md                          # Tổng quan dự án, hướng dẫn deploy
├── ARCHITECTURE.md                    # Sơ đồ kiến trúc, luồng nghiệp vụ
├── contracts/
│   ├── storage_test.py                # Sanity contract — deploy ĐẦU TIÊN
│   ├── esg_audit.py                   # Contract chính
│   └── mock_usdc.py                   # Mock USDC ERC20 cho audit fee
├── frontend/
│   ├── index.html                     # Landing + Public Registry
│   ├── submit-audit.html              # Form công ty submit audit
│   ├── audit-detail.html              # Chi tiết audit + ESG verdict
│   ├── company-profile.html           # Profile công ty + badge history
│   ├── investor-dashboard.html        # Dashboard cho investor screen ESG
│   ├── whistleblower.html             # Submit challenge evidence
│   ├── styles.css                     # Theme: dark forest green + earth tones
│   ├── app.js                         # Logic gọi GenLayer SDK (placeholder)
│   └── assets/                        # Chứa các file vector hình ảnh logo/badge
├── tests/
│   ├── test_flow.md                   # Kịch bản test step-by-step trên Studio
│   └── sample_companies.md            # Các công ty thực tế để test (Apple, Patagonia, Shell...)
└── docs/
    ├── DEPLOY_GUIDE.md                # 7 Rules + deploy procedure
    ├── DEMO_SCRIPT.md                 # Script 3-phút demo cho hackathon
    ├── BUSINESS_MODEL.md              # Cơ cấu định giá, quy mô thị trường
    ├── AI_PROMPT_LIBRARY.md           # Thư viện prompt của AI Auditor
    └── ESG_FRAMEWORK.md               # Giải thích các tiêu chuẩn GRI/SASB/TCFD
```

---

## 🌍 Tác động thực tế (Real-World Impact)

1. **Tuân thủ CSRD Châu Âu (EU CSRD)**: Đến năm 2026, hơn 50.000 doanh nghiệp bắt buộc phải kiểm toán ESG. ESGAudit giúp họ tự kiểm toán nhanh chóng trước khi thực hiện kiểm toán chính thức hoặc cung cấp bằng chứng tin cậy cho bên thứ ba.
2. **Xác thực cho Quỹ Đầu tư ESG ($30T AUM)**: Cung cấp công cụ lọc thời gian thực chống tẩy xanh cho các nhà quản lý quỹ trước khi phân bổ nguồn vốn.
3. **Phòng chống gian lận Tín chỉ Carbon ($30B)**: Ngăn chặn các doanh nghiệp mua tín chỉ "ma", tín chỉ trùng lặp, hoặc không tạo ra tác động giảm khí thải thực tế nhờ phân tích chéo nguồn cấp dữ liệu của các tổ chức đăng ký (Verra, Gold Standard) và vệ tinh.
4. **Cơ chế thổi còi (Whistleblower Bounty)**: Khuyến khích cộng đồng cùng giám sát, gửi bằng chứng phản bác để cập nhật tình trạng on-chain và nhận phần thưởng từ quỹ chung.

---

## ⚙️ Hướng dẫn khởi chạy nhanh

### Deploy Hợp đồng thông minh lên GenLayer Studio
1. Truy cập [GenLayer Studio](https://studio.genlayer.com/run-debug).
2. Xóa bộ nhớ đệm qua **Settings -> Reset Storage -> Confirm** và nhấn F5/Cmd+Shift+R để làm mới trang.
3. Tạo file mới và copy nội dung từ `contracts/storage_test.py`. Deploy file này **đầu tiên** để kiểm tra môi trường.
4. Tiếp tục deploy `contracts/mock_usdc.py` để khởi tạo token demo.
5. Deploy hợp đồng chính `contracts/esg_audit.py`. Hãy đảm bảo kiểm tra kỹ **7 Nguyên tắc triển khai (7 Rules)** trong tài liệu `docs/DEPLOY_GUIDE.md` để tránh lỗi biên dịch.

### Mở Giao diện Frontend
Mở file `frontend/index.html` trong bất kỳ trình duyệt web nào của bạn. Giao diện sử dụng Vanilla Javascript cùng CSS để mô phỏng tương tác gọi ví Web3 và truy vấn trạng thái từ GenLayer blockchain.
