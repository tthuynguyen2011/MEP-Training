# MEP ENERGY MASTER SUITE (ASHRAE & ISO 500XX)
### Bộ Công Cụ Kỹ Thuật HVAC, Thiết Kế MEP & Kiểm Toán Năng Lượng Thực Chiến

Bộ công cụ này được thiết kế và xây dựng để phục vụ công tác **đào tạo chuyên sâu kỹ sư HVAC/MEP** và ứng dụng trực tiếp vào các **dự án thiết kế, thẩm tra kỹ thuật và kiểm toán năng lượng công trình** theo chuẩn mực quốc tế **ASHRAE** và **ISO 500XX**.

---

## 1. CẤU TRÚC BỘ CÔNG CỤ

```
02.MEP_Energy_Master_Suite/
│
├── README.md                              # Hướng dẫn tổng quan & cách sử dụng Suite
├── GIAO_TRINH_DAO_TAO_KY_SU.md            # Giáo trình đào tạo 16 tuần từ Junior lên Senior & Auditor
├── requirements.txt                       # Thư viện phụ thuộc Python (numpy, scipy, openpyxl, etc.)
│
├── mep_suite/                             # Thư viện mã nguồn Python lõi kỹ thuật
│   ├── __init__.py                        # Export API của 7 Modules
│   ├── module1_psychro_load.py            # Module 1: Nhiệt ẩm học Psychrometrics & Tải lạnh RTS
│   ├── module2_hydraulics_duct.py         # Module 2: Khí động ống gió & Thủy lực ống nước ChW/CdW
│   ├── module3_chiller_plant.py           # Module 3: Mô phỏng Chiller Plant, Bơm, Tháp & Heat Pump
│   ├── module4_facilities.py              # Module 4: Cấu hình chuyên biệt: Hospital, Data Center, Hotel, Office
│   ├── module5_energy_codes.py            # Module 5: Tuân thủ Quy chuẩn QCVN 09:2017 & ASHRAE 90.1
│   ├── module6_iso50002_audit.py          # Module 6: Kiểm toán Năng lượng ISO 50002 & Phân tích LCCA (NPV/IRR)
│   └── module7_cx_tab_fdd.py              # Module 7: Nghiệm thu vận hành (Cx), Cân bằng TAB & Chẩn đoán lỗi FDD
│
├── build_excel_tool.py                    # Script tự động tạo Workbook Excel chuẩn chuyên nghiệp
├── run_suite_demo.py                      # Script chạy kiểm thử toàn bộ 7 modules với dữ liệu mẫu
└── MEP_Energy_Auditor_Master_Toolkit.xlsx # File Excel Workbook hoàn chỉnh với công thức sống trực quan
```

---

## 2. NỘI DUNG 7 MODULES CỐT LÕI

| Module | Tên chuyên đề | Tiêu chuẩn tham chiếu | Chức năng kỹ thuật chính |
| :--- | :--- | :--- | :--- |
| **01** | **Psychrometrics & Peak Load** | ASHRAE Fundamentals (Ch. 1, 18), QCVN 02:2022 | Tra cứu 7 thông số nhiệt ẩm, mô phỏng quá trình dàn lạnh (ADP, BF, SHR), tính tải đỉnh RTS. |
| **02** | **Duct & Pipe Hydraulics** | ASHRAE Fundamentals (Ch. 21, 22), TCVN 5687:2024 | Sizing ống gió (Equal Friction, Huebscher, Fan ESP), sizing ống nước ChW (Darcy-Weisbach, Cột áp bơm). |
| **03** | **Central Chiller Plant Sim** | AHRI 550/590, ASHRAE Systems & Equipment | Cân bằng nhiệt Chiller, COP, kW/RT, IPLV non tải, đánh giá hiệu suất toàn trạm (Chiller + Bơm + Tháp). |
| **04** | **Specialized Facilities MEP** | ASHRAE 170, ASHRAE TC 9.9, ASHRAE 62.1 | Phòng mổ bệnh viện (20 ACH, +2.5 Pa), Data Center (PUE, làm mát IT), Khách sạn (Nước nóng Heat Pump). |
| **05** | **Energy Code Compliance** | QCVN 09:2017/BXD, ASHRAE Standard 90.1-2022 | Tính toán và kiểm tra tuân thủ OTTV tường/mái, tỷ lệ kính WWR, mật độ chiếu sáng LPD, hiệu suất tối thiểu COP. |
| **06** | **ISO 50002 Energy Audit** | TCVN ISO 50002:2015, ASHRAE 211, IPMVP | Xây dựng Baseline hồi quy CDD, xử lý số liệu đo đạc thực tế, chẩn đoán Low Delta-T, tính toán ECM & LCCA. |
| **07** | **Commissioning & TAB & FDD** | ASHRAE Guideline 0/1.1, NEBB TAB, NIST FDD | Bảng nghiệm thu cân bằng tỷ lệ mạng gió/nước ($\pm 10\%$), chẩn đoán lỗi tự động (FDD) cho AHU và Chiller. |

---

## 3. HƯỚNG DẪN SỬ DỤNG

### Cách 1: Sử dụng File Excel Workbook trực quan (`MEP_Energy_Auditor_Master_Toolkit.xlsx`)
- Mở trực tiếp file bằng Microsoft Excel.
- Các ô màu **Vàng kem (Soft Yellow)** là các ô nhập liệu của người dùng (User Inputs).
- Các ô màu **Xám nhạt / Xanh lá** là các ô công thức tính toán tự động sống (Live formulas) không cần chỉnh sửa.
- File đã tích hợp đầy đủ 8 sheets tương ứng từ Tổng quan dự án (`00_DASHBOARD`) đến từng chuyên đề chi tiết.

### Cách 2: Chạy kiểm thử mẫu với Python
Mở PowerShell hoặc Command Prompt tại thư mục bộ tool:
```powershell
python run_suite_demo.py
```

### Cách 3: Nhúng thư viện vào các script tính toán tùy chỉnh
```python
from mep_suite import Psychrometrics, PipeHydraulics, ChillerPlantSimulator, EnergyAuditISO50002

# Tra cứu nhiệt ẩm
psy = Psychrometrics()
state = psy.state_from_tdb_rh(t_db=24.0, rh_percent=55.0)
print(f"Enthalpy: {state['h_kj']} kJ/kg, Dew point: {state['t_dp']} °C")

# Sizing ống nước lạnh
flow = PipeHydraulics.flow_rate_from_cooling_capacity(capacity_kw=350.0)
pipe = PipeHydraulics.auto_size_pipe(flow_m3_h=flow["flow_m3_h"])
print(f"Chọn ống: {pipe['selected_dn']} (V = {pipe['velocity_m_s']} m/s)")
```

---

## 4. TÀI LIỆU ĐÀO TẠO KÈM THEO
Vui lòng đọc file [`GIAO_TRINH_DAO_TAO_KY_SU.md`](GIAO_TRINH_DAO_TAO_KY_SU.md) để xem chi tiết lộ trình 16 tuần, các đầu việc bài tập và tiêu chí đánh giá nghiệm thu học viên.
