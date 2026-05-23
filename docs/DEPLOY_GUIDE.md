# 🚀 Hướng dẫn triển khai Hợp đồng thông minh GenLayer (DEPLOY_GUIDE)

Tài liệu này chứa các quy tắc cốt lõi, quy trình triển khai và hướng dẫn xử lý lỗi khi deploy hợp đồng thông minh GenLayer viết bằng Python lên giao diện [GenLayer Studio](https://studio.genlayer.com/run-debug).

---

## ⚠️ 7 NGUYÊN TẮC CỐT LÕI (BẮT BUỘC TUÂN THỦ)

Việc bỏ sót bất kỳ nguyên tắc nào dưới đây sẽ dẫn đến lỗi deploy hoàn toàn (100% fail). Hãy kiểm tra kỹ từng nguyên tắc trước khi thực hiện deploy.

### Rule #1 — Dòng đầu tiên phải chính xác là `# v0.2.16`
```python
# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
```
* **Triệu chứng nếu thiếu**: Hệ thống sẽ fallback về v0.1.0 và báo lỗi `Contract Queues not found` hoặc `Contract IdlenessPhase not found`.

### Rule #2 — KHÔNG khởi tạo lại `TreeMap()` hoặc `DynArray()` trong hàm `__init__`
```python
# ❌ SAI
def __init__(self):
    self.audits = TreeMap()
    self.company_badge = TreeMap()

# ✅ ĐÚNG
def __init__(self):
    self.audit_counter = u256(0)
    # TreeMap/DynArray tự động được GenVM khởi tạo rỗng — KHÔNG ĐỤNG VÀO.
```
* **Triệu chứng nếu sai**: Transaction được thông báo `FINALIZED` nhưng có trạng thái `Result: ERROR` kèm lỗi `AssertionError: TreeMap <- TreeMap`.

### Rule #3 — KHÔNG sử dụng kiểu dữ liệu `float` trong các hàm Public
```python
# ❌ SAI
@gl.public.write
def submit_audit(self, fee: float): ...

# ✅ ĐÚNG
@gl.public.write
def submit_audit(self, fee: int): ...
```
* **Triệu chứng nếu sai**: Trình phân tích cú pháp schema (schema parser) sẽ từ chối biên dịch hợp đồng.

### Rule #4 — Các kiểu dữ liệu được phép sử dụng trong Public Methods
* **Được phép**: `str`, `bool`, `bytes`, `int`, các số nguyên định cỡ (`u8` đến `u256`, `i8` đến `i256`), `Address`, `DynArray[T]`, `TreeMap[K, V]`.
* **Cấm**: `float`, `list[T]`, `dict[K, V]`, generic chưa instantiate, custom classes, `Optional[T]`, `Union[...]`.

### Rule #5 — Storage dùng `TreeMap` và `DynArray`, KHÔNG dùng `dict` hay `list` của Python
```python
class Contract(gl.Contract):
    # ✅ ĐÚNG
    audits: TreeMap[u256, str]
    audit_ids: DynArray[u256]

    # ❌ SAI
    audits: dict[int, str]
    audit_ids: list[int]
```

### Rule #6 — Tên của lớp Hợp đồng chính bắt buộc phải là `Contract` và kế thừa từ `gl.Contract`
```python
# ✅ ĐÚNG
class Contract(gl.Contract):
    ...

# ❌ SAI
class ESGAudit(gl.Contract):
    ...
```

### Rule #7 — Mọi hàm gọi `gl.nondet.*` phải được thực thi bên trong `gl.vm.run_nondet_unsafe`
```python
# ❌ SAI
@gl.public.write
def audit(self):
    result = gl.nondet.exec_prompt("...")

# ✅ ĐÚNG
@gl.public.write
def run_audit(self, audit_id: u256):
    def leader_fn():
        return gl.nondet.exec_prompt("...", response_format="json")
    def validator_fn(leader_result) -> bool:
        return isinstance(leader_result, gl.vm.Return)
    return gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
```

---

## 🩺 BẢNG TRA CỨU NHANH VÀ XỬ LÝ LỖI (TROUBLESHOOTING MAP)

| Lỗi / Triệu chứng | Nguyên nhân phổ biến | Giải pháp xử lý |
| :--- | :--- | :--- |
| `Contract Queues not found` | Thiếu khai báo phiên bản dòng số 1 | Thêm dòng `# v0.2.16` vào đầu file |
| `AssertionError: TreeMap <- TreeMap` | Reassign TreeMap trong `__init__` | Xóa dòng gán `self.x = TreeMap()` |
| Schema error / Won't compile | Sử dụng kiểu dữ liệu cấm (ví dụ: float) | Đổi kiểu dữ liệu sang `int` hoặc `str` |
| Hợp đồng không hiển thị dù Tx FINALIZED | Giao dịch thất bại tại Node | Click vào mã Hash giao dịch ở thanh bên để đọc traceback cụ thể |
| Lỗi lạ khi deploy dù code đúng | Bộ nhớ đệm (Cache) của Studio bị lỗi | Vào Settings -> Reset Storage -> Cmd+Shift+R |

---

## ✅ DANH SÁCH KIỂM TRA TRƯỚC KHI DEPLOY (PRE-DEPLOY CHECKLIST)

- [ ] Hợp đồng bắt đầu bằng dòng `# v0.2.16`
- [ ] Dòng thứ 2 chứa thông tin phụ thuộc `# { "Depends": "py-genlayer:..." }`
- [ ] Hàm `__init__` không có lệnh gán `TreeMap()` hay `DynArray()`
- [ ] Không xuất hiện kiểu dữ liệu `float` trong bất kỳ tham số đầu vào của hàm `@gl.public`
- [ ] Khai báo lưu trữ (Storage) chỉ sử dụng các kiểu `TreeMap[K, V]` hoặc `DynArray[T]`
- [ ] Lớp hợp đồng chính được đặt tên chính xác là `Contract` kế thừa `gl.Contract`
- [ ] Tất cả lời gọi `gl.nondet.web.render` và `gl.nondet.exec_prompt` đã được bao bọc trong cấu trúc `gl.vm.run_nondet_unsafe`

---

## 🚀 QUY TRÌNH DEPLOY HỢP ĐỒNG TRÊN STUDIO

1. Truy cập [GenLayer Studio](https://studio.genlayer.com/run-debug).
2. Vào **Settings -> Reset Storage -> Confirm** để làm sạch trạng thái môi trường.
3. Thực hiện **Hard Refresh** trình duyệt bằng tổ hợp phím `Cmd+Shift+R` (macOS) hoặc `Ctrl+Shift+F5` (Windows).
4. Deploy file `storage_test.py` **ĐẦU TIÊN** để xác minh môi trường hoạt động tốt. Click giao dịch để xem trạng thái đạt `Result: SUCCESS`.
5. Tiếp tục deploy `mock_usdc.py` để làm token phí.
6. Deploy hợp đồng chính `esg_audit.py`.
7. Kiểm tra trạng thái giao dịch bên sidebar đảm bảo toàn bộ đều trả về `Result: SUCCESS`.

---

## 🧠 BÀI HỌC KINH NGHIỆM TỪ ĐỘI NGŨ ANTIGRAVITY

> [!WARNING]
> 1. **Lỗi gán TreeMap**: Rất dễ viết nhầm `self.audits = TreeMap()` theo thói quen lập trình hướng đối tượng thông thường của Python. GenVM tự động quản lý vòng đời và lưu trữ của TreeMap, do đó gán đè sẽ gây phá vỡ liên kết cấu trúc dữ liệu on-chain.
> 2. **Lỗi Closure biến**: Trong các hàm leader_fn sử dụng biến từ scope ngoài (lexical closure), hãy đảm bảo các biến đó có kiểu dữ liệu cơ bản và không cố tình ghi đè lại chúng bên trong closure để tránh các lỗi không tương thích môi trường chạy bất định.
> 3. **Báo cáo PDF quá dài**: `web.render` đối với các file PDF cực kỳ nặng có thể gây hết bộ nhớ hoặc bị cắt xén nội dung giữa chừng. Hãy luôn bổ sung tùy chọn URL trang HTML (Sustainability Web Page) làm nguồn thay thế để tăng tỷ lệ thành công của cuộc kiểm toán.
