# BÀI GIẢNG 02: KHÍ ĐỘNG LỰC HỌC MẠNG GIÓ & THỦY LỰC MẠNG ĐƯỜNG ỐNG NƯỚC
## (Từ Nguyên lý Dòng chảy đến Thiết kế, Sizing & Chọn Bơm / Quạt Thực chiến)

---

### MỤC TIÊU BÀI HỌC
1. **Làm chủ khí động học đường ống gió:** Hiểu rõ bản chất tổn thất ma sát và cục bộ, phương pháp Ma sát đồng đều (Equal Friction) và Phục hồi áp suất tĩnh (Static Regain), kiểm soát vận tốc âm học theo tiêu chí độ ồn NC.
2. **Tính toán chính xác cột áp quạt (Fan ESP):** Phân biệt Áp suất tĩnh (Static Pressure), Áp suất vận tốc (Velocity Pressure) và Tổng áp suất (Total Pressure). Tính bù trở lực toàn tuyến trở lực lớn nhất (Index Run).
3. **Làm chủ thủy lực mạng đường ống nước ChW/CdW:** Công thức Darcy-Weisbach, Colebrook-White, quy tắc sizing đường ống theo giới hạn ma sát ($1 - 3\text{ mH2O/100m}$) và vận tốc ($0.8 - 2.4\text{ m/s}$).
4. **Phân biệt hệ kín (Closed loop) và hệ hở (Open loop):** Cột áp tĩnh hình học (Static Lift) của tháp giải nhiệt và hiện tượng xâm thực khí (Cavitation) với $NPSHa$ và $NPSHr$.

---

## PHẦN 1: KHÍ ĐỘNG LỰC HỌC ĐƯỜNG ỐNG GIÓ (DUCT AERODYNAMICS)

### 1.1 Phương trình cơ bản & Áp suất trong đường ống
Theo định luật bảo toàn năng lượng Bernoulli cho chất khí chuyển động trong ống dẫn:
$$P_{total} = P_{static} + P_{velocity}$$
Trong đó:
- $P_{static}$ (Áp suất tĩnh): Áp suất tác dụng vuông góc lên thành ống, có xu hướng làm phồng hoặc xẹp ống (đơn vị: $\text{Pa}$).
- $P_{velocity}$ (Áp suất vận tốc): Động năng của dòng khí chuyển động theo phương dọc trục ống:
  $$P_{velocity} = \frac{1}{2} \rho V^2 \quad (\rho \approx 1.204\text{ kg/m}^3 \text{ ở } 20^\circ C)$$
- $P_{total}$ (Tổng áp suất): Thể hiện tổng năng lượng của dòng khí. Theo chiều chuyển động, $P_{total}$ **luôn luôn giảm** do ma sát và nhiễu loạn cục bộ biến thành nhiệt năng tỏa ra môi trường.

### 1.2 Đường kính ống tròn tương đương Huebscher
Trong thiết kế thực tế, đa số ống gió đi trong trần giả là ống chữ nhật (Rectangular duct) kích thước $a \times b$ để tiết kiệm chiều cao trần.
Công thức Huebscher (ASHRAE Fundamentals Ch. 21 Eq. 25) cho đường kính ống tròn $D_e$ có cùng lưu lượng và cùng độ giảm áp suất ma sát:
$$D_e = 1.30 \cdot \frac{(a \cdot b)^{0.625}}{(a + b)^{0.250}}$$
> **QUY TẮC THỰC CHIẾN:** Tỷ lệ cạnh $a/b$ (Aspect Ratio) lý tưởng là $1:1$ đến $2:1$. Tuyệt đối tránh thiết kế ống dẹt có tỷ lệ $a/b > 4:1$ vì tổn thất ma sát tăng vọt, thành ống mỏng dễ rung ồn khi gió đi qua và tốn tôn gia công.

### 1.3 Giới hạn vận tốc âm học (Noise Criteria - NC)
Vận tốc gió quá cao sẽ tạo ra tiếng rít và xoáy khí gây ồn. Giới hạn vận tốc tối đa theo khuyến cáo của ASHRAE:
- Ống gió chính trong trục kỹ thuật / phòng máy: $V_{max} \le 8.0 - 9.5\text{ m/s}$.
- Ống chính trên trần khu vực văn phòng: $V_{max} \le 5.5 - 6.5\text{ m/s}$ (NC 35).
- Ống nhánh cấp vào miệng gió: $V_{max} \le 3.5 - 4.2\text{ m/s}$ (NC 30).
- Phòng ngủ khách sạn 5 sao / Phòng thu âm: $V_{max} \le 2.5 - 3.0\text{ m/s}$ (NC 25).

---

## PHẦN 2: QUY TRÌNH TÍNH CỘT ÁP TĨNH NGOÀI CỦA QUẠT (FAN ESP)

Cột áp tĩnh ngoài (External Static Pressure - ESP) là năng lượng áp suất mà quạt phải sinh ra để thắng toàn bộ trở lực của hệ thống đường ống và phụ kiện bên ngoài vỏ AHU/quạt:
$$ESP = \Delta P_{straight} + \Delta P_{fittings} + \Delta P_{terminals}$$
Tổng cột áp tĩnh quạt (Fan Total Static Pressure - TSP) bao gồm cả trở lực nội vi bên trong vỏ máy:
$$TSP = ESP + \Delta P_{internal} (\text{Phin lọc, Dàn coil lạnh, Buồng hòa trộn})$$

```mermaid
flowchart LR
    A["Không khí vào AHU"] --> B["Phin lọc G4 + F8<br>ΔP: 120 - 180 Pa"]
    B --> C["Dàn coil nước lạnh AHU<br>ΔP: 90 - 140 Pa"]
    C --> D["Quạt cấp (Supply Fan)<br>Sinh tổng áp TSP"]
    D --> E["Ống gió thẳng + Cút co<br>ΔP: 80 - 150 Pa"]
    E --> F["Van dập lửa chì FD + VAV<br>ΔP: 65 Pa"]
    F --> G["Miệng gió khuếch tán Diffuser<br>ΔP: 25 - 35 Pa"]
```

### Bảng dự phòng trở lực chuẩn cho dự án văn phòng Hạng A:
1. **Phin lọc sơ cấp G4 (Pre-filter) ở trạng thái bẩn vừa:** $70\text{ Pa}$.
2. **Phin lọc tinh F7/F8 (Secondary filter) ở trạng thái bẩn vừa:** $130\text{ Pa}$.
3. **Dàn coil làm lạnh nước (6 - 8 hàng ống ướt):** $110\text{ Pa}$.
4. **Trở lực ma sát ống gió thẳng tuyến dài nhất ($100\text{ m} \times 0.9\text{ Pa/m}$):** $90\text{ Pa}$.
5. **Trở lực co, cút, côn giảm, tee (5 co $\times 18\text{ Pa} + 2\text{ tee} \times 25\text{ Pa}$):** $140\text{ Pa}$.
6. **Van ngăn lửa FD chì:** $25\text{ Pa}$.
7. **Hộp điều chỉnh lưu lượng biến đổi VAV Box:** $45\text{ Pa}$.
8. **Miệng gió khuếch tán kèm hộp gom gió:** $30\text{ Pa}$.
- $\rightarrow$ Tổng trở lực thực tế: $640\text{ Pa}$.
- Hệ số an toàn thiết kế ($15\%$ safety margin): $TSP = 640 \times 1.15 = 736\text{ Pa}$.

---

## PHẦN 3: THỦY LỰC MẠNG ĐƯỜNG ỐNG NƯỚC LẠNH (CHILLED WATER HYDRAULICS)

### 3.1 Lưu lượng và Phương trình Darcy-Weisbach
Lưu lượng nước lạnh tuần hoàn được tính từ công suất lạnh:
$$\dot{Q} = \dot{m} \cdot C_p \cdot \Delta T \implies Q\text{ (m}^3\text{/h)} = \frac{kW \times 3600}{\rho \cdot C_p \cdot \Delta T}$$
Với nước lạnh $7^\circ C$, $\rho \approx 1000\text{ kg/m}^3$, $C_p = 4.186\text{ kJ/kg.K}$, độ chênh nhiệt độ $\Delta T = 5.5^\circ C$:
$$Q\text{ (m}^3\text{/h)} \approx \frac{kW}{6.395} \approx \frac{RT \times 3.51685}{6.395} \approx 0.55\text{ m}^3\text{/(h.RT)} \quad (\approx 2.4\text{ GPM/RT})$$

Tổn thất cột áp ma sát trong đường ống tròn đường kính trong $D$:
$$h_f\text{ (mH}_2\text{O)} = f \cdot \frac{L}{D} \cdot \frac{V^2}{2g}$$
Hệ số ma sát $f$ được tính theo phương trình Swamee-Jain (cho dòng chảy rối chuyển tiếp trong ống thép hàn, độ nhám $\epsilon = 0.045\text{ mm}$):
$$f = \frac{0.25}{\left[\log_{10}\left(\frac{\epsilon}{3.7 D} + \frac{5.74}{Re^{0.9}}\right)\right]^2}$$

### 3.2 Tiêu chí vàng chọn cỡ ống nước lạnh (ASHRAE Chapter 22)
1. **Tổn thất ma sát giới hạn:** $1.0\text{ mH}_2\text{O/100m} \le \frac{\Delta h}{L} \le 3.0\text{ mH}_2\text{O/100m}$ (tương đương $100 - 300\text{ Pa/m}$).
2. **Khống chế vận tốc dòng chảy:**
   - Ống nhỏ $\le DN50$: $V \le 1.2\text{ m/s}$ (tránh xói mòn van và tiếng ồn tại các phòng).
   - Ống trung bình $DN65 - DN150$: $V \le 1.5 - 2.0\text{ m/s}$.
   - Ống chính lớn $\ge DN200$: $V \le 2.2 - 2.5\text{ m/s}$.

### 3.3 Tính toán Cột áp Bơm (Total Dynamic Head - TDH)
1. **Đối với hệ thống kín (Closed Loop - Mạch nước lạnh Chilled Water):**
   - Áp suất tĩnh của tòa nhà (Static Head do độ cao 20 tầng) **triệt tiêu hoàn toàn** vì cột nước lên và cột nước xuống cân bằng nhau.
   - Bơm chỉ cần thắng trở lực ma sát đường ống và thiết bị:
     $$H_{pump} = \Delta H_{pipe} + \Delta H_{fittings} + \Delta H_{evaporator} + \Delta H_{coil} + \Delta H_{valves}$$
     - Bình bay hơi Chiller (Evaporator): $40 - 60\text{ kPa}$ ($\sim 4 - 6\text{ mH}_2\text{O}$).
     - Dàn coil AHU xa nhất: $30 - 50\text{ kPa}$ ($\sim 3 - 5\text{ mH}_2\text{O}$).
     - Van điều khiển cân bằng áp lực độc lập (PICV): $20 - 35\text{ kPa}$ ($\sim 2 - 3.5\text{ mH}_2\text{O}$).
     - Ma sát đường ống và co cút tuyến xa nhất: $12 - 18\text{ mH}_2\text{O}$.
     $\rightarrow$ Cột áp bơm nước lạnh tòa nhà cao tầng thường dao động từ **$25 - 32\text{ mH}_2\text{O}$**.
2. **Đối với hệ thống hở (Open Loop - Mạch nước giải nhiệt Condenser Water):**
   - Nước từ đáy tháp chảy về bình ngưng Chiller, bơm đẩy nước lên đỉnh tháp qua vòi phun xịt (Nozzle).
   - **Bơm phải thắng thêm chiều cao nâng tĩnh (Static Lift):** Khoảng cách từ mặt nước bể chứa đáy tháp đến vòi phun đỉnh tháp (thường $2.5 - 4.5\text{ m}$) cộng áp suất vòi phun ($3 - 5\text{ m}$).

### 3.4 Hiện tượng Xâm thực Khí (Cavitation) và $NPSH$
Hiện tượng xâm thực xảy ra khi áp suất tại miệng hút của bơm giảm xuống dưới áp suất bốc hơi của nước, tạo ra các bong bóng hơi. Khi đi vào cánh bơm có áp suất cao, bóng hơi nổ sụp với áp lực cực lớn làm rỗ mòn cánh bơm, gây rung lắc và phá hủy phớt chặn cơ khí.
- Điều kiện để bơm không bị xâm thực:
  $$NPSHa \ge NPSHr + 0.5\text{ m}$$
  - $NPSHr$ (Net Positive Suction Head Required): Cột áp hút dương tối thiểu do nhà sản xuất bơm quy định.
  - $NPSHa$ (Net Positive Suction Head Available): Cột áp hút dương thực tế do thiết kế mặt bằng ống quyết định:
    $$NPSHa = \frac{P_{surface}}{\rho g} \pm Z_{level} - h_{suction\_friction} - \frac{P_{vapor}}{\rho g}$$

---

## PHẦN 4: CASE STUDY THỰC HÀNH - THIẾT KẾ CỤM BƠM CHILLER 500 RT

* **Thông số:** Chiller 500 RT giải nhiệt nước.
* **Tính lưu lượng:**
  $$Q = 500\text{ RT} \times 0.55\text{ m}^3\text{/(h.RT)} = 275.0\text{ m}^3\text{/h} = 76.4\text{ L/s} = 1,210\text{ GPM}$$
* **Chọn đường kính ống:**
  - Tra bảng ống thép SCH40: Chọn ống **DN250** (đường kính trong $254.5\text{ mm}$).
  - Vận tốc dòng chảy:
    $$V = \frac{0.0764}{\pi \times (0.2545)^2 / 4} = 1.50\text{ m/s} \quad (\text{Thỏa mãn } V \le 2.2\text{ m/s})$$
  - Tổn thất ma sát theo Colebrook: $h_f = 1.45\text{ mH}_2\text{O/100m}$ (Nằm trong dải chuẩn $1 - 2\text{ m/100m}$).
* **Tính công suất điện động cơ bơm:**
  - Cột áp thiết kế: $H = 28\text{ mH}_2\text{O}$.
  - Hiệu suất bơm $\eta_{pump} = 78\%$, hiệu suất động cơ IE3 $\eta_{motor} = 93\%$.
  - Công suất điện trục:
    $$P_{elec} = \frac{\rho \cdot g \cdot Q \cdot H}{3.6 \times 10^6 \times \eta_{pump} \times \eta_{motor}} = \frac{1000 \times 9.81 \times 275 \times 28}{3.6 \times 10^6 \times 0.78 \times 0.93} = 28.9\text{ kW}$$
  - Chọn công suất động cơ định mức tiêu chuẩn: **$37.0\text{ kW}$** (Dự phòng $25\%$ chống quá tải khi khởi động).
