# HƯỚNG DẪN SỬ DỤNG TOOL TRÊN MÁY TÍNH CÁ NHÂN (100% OFFLINE / KHÔNG CẦN INTERNET)

Bộ công cụ **MEP Energy Master Suite** được thiết kế đặc biệt theo tiêu chuẩn **Zero Dependency (Không phụ thuộc mạng)** để mọi kỹ sư MEP, HVAC và Kiểm toán viên năng lượng có thể mang theo công trường, dự án hoặc cài đặt trực tiếp trên máy tính xách tay cá nhân (Laptop / PC) mà không cần internet.

---

## 1. CÁCH 1: SỬ DỤNG GIAO DIỆN ĐỒ HỌA TRỰC QUAN (KHUYÊN DÙNG)
* **Yêu cầu hệ thống:** Mọi máy tính Windows / MacOS / Linux có bất kỳ trình duyệt web nào (Microsoft Edge, Google Chrome, Cốc Cốc, Firefox).
* **Không yêu cầu:** KHÔNG cần cài Python, KHÔNG cần cài Node.js, KHÔNG cần kết nối mạng Internet.

### Các bước thực hiện:
1. Sao chép toàn bộ thư mục `02.MEP_Energy_Master_Suite` về ổ đĩa máy tính cá nhân của bạn (Ví dụ: `D:\MEP_Tools\` hoặc trên Desktop).
2. **Cách mở nhanh:** Click đúp chuột vào file:
   👉 **`Chay_Tool_MEP.bat`** (trên Windows)
   *Hoặc click đúp trực tiếp vào file **`MEP_Energy_Master_App.html`**.*
3. Ứng dụng sẽ tự động mở lên trong trình duyệt với giao diện tương tác thời gian thực:
   - Thay đổi các giá trị đầu vào $\rightarrow$ Kết quả tính toán nhiệt ẩm, kích thước ống gió, ống nước, hiệu suất Chiller, OTTV, PUE, hoàn vốn ECM sẽ cập nhật tức thì.
   - Có nút **"🖨️ In / Xuất PDF"** góc trên bên phải để in trực tiếp báo cáo thuyết minh tính toán nộp cho chủ đầu tư.

---

## 2. CÁCH 2: SỬ DỤNG FILE EXCEL WORKBOOK CHUYÊN SÂU (`.xlsx`)
* Nếu bạn quen làm việc trên bảng tính Excel:
  - Mở trực tiếp file: 👉 **`MEP_Energy_Auditor_Master_Toolkit.xlsx`**
  - File đã được khóa công thức và phân màu rõ ràng:
    + 🟡 **Ô màu Vàng kem (Input):** Nhập số liệu dự án.
    + ⚪ **Ô màu Xám nhạt (Formulas):** Tự động tính theo công thức chuẩn ASHRAE.
    + 🟢 **Ô màu Xanh lá (Output/KPI):** Kết quả đạt chuẩn, hiệu suất cao, thời gian hoàn vốn.
    + 🔴 **Ô màu Cam/Đỏ (Alerts):** Cảnh báo hội chứng Low Delta-T, cặn tháp hoặc vượt quy chuẩn OTTV.

---

## 3. CÁCH 3: CHẠY BẰNG PYTHON ENGINE (CHO KỸ SƯ LẬP TRÌNH & NÂNG CAO)
Nếu máy tính cá nhân của bạn đã có cài Python (bản 3.8 trở lên):
1. Mở PowerShell hoặc CMD tại thư mục của bộ tool.
2. Cài đặt các thư viện tính toán:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy kiểm thử toàn bộ 7 Modules:
   ```bash
   python run_suite_demo.py
   ```
4. Chạy Local Web Server:
   ```bash
   python app_server.py
   ```
   Server sẽ mở cổng cục bộ `http://localhost:8089` hoàn toàn độc lập và không gửi bất kỳ dữ liệu nào ra ngoài internet.
