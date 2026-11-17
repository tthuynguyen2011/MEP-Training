# GIÁO TRÌNH ĐÀO TẠO KỸ SƯ HVAC & KIỂM TOÁN VIÊN NĂNG LƯỢNG MEP THỰC CHIẾN
## (Chương trình Đào tạo Chuyên sâu theo Chuẩn ASHRAE & ISO 500XX thông qua Kiến tạo Công cụ Kỹ thuật)

---

### MỤC TIÊU ĐÀO TẠO & PHƯƠNG PHÁP LUẬN
- **Đối tượng đào tạo:** Kỹ sư mới tốt nghiệp / Kỹ sư HVAC mới vào nghề (Junior 0 - 2 năm kinh nghiệm).
- **Mục tiêu đầu ra:**
  1. Trở thành **Senior HVAC/MEP Design Engineer**: Nắm vững nguyên lý nhiệt động học, khí hậu học, thủy lực mạng ống, thiết kế thành thạo hệ thống HVAC trung tâm (Chiller, VRV/VRF, AHU/FCU, VAV, Thông gió PCCC) cho mọi thể loại công trình (Văn phòng, Khách sạn, Bệnh viện, Data Center, Nhà xưởng).
  2. Trở thành **Lead Energy Auditor & Commissioning Specialist (Kiểm toán viên Năng lượng ISO 50002 / Chuyên gia TAB & Cx)**: Có khả năng lập kế hoạch đo kiểm thực địa, phân tích hóa đơn và baseline, chẩn đoán căn bệnh vận hành (Low Delta-T, cáu cặn, xung đột nhiệt), đề xuất và tính toán khả thi tài chính các giải pháp tiết kiệm năng lượng (ECMs) chuẩn ASHRAE 211 / IPMVP.
- **Phương pháp luận "Learning by Building Tools":** 
  - Kỹ sư không chỉ học lý thuyết suông hay dùng phần mềm thương mại dạng "hộp đen" (Black-box), mà phải tự lập trình/xây dựng và làm chủ công cụ tính toán của chính mình.
  - Mọi công thức đều phải truy vết nguồn gốc (Traceability) từ tiêu chuẩn quốc tế (**ASHRAE Fundamentals, Equipment, Applications, 90.1, 55, 62.1, 170**) và quy chuẩn Việt Nam (**QCVN 09:2017/BXD, QCVN 02:2022/BXD, TCVN 5687:2024, ISO 50001/50002**).

---

## LỘ TRÌNH CHI TIẾT 16 TUẦN THỰC HÀNH

```mermaid
gantt
    title Lộ trình 16 tuần Đào tạo Kỹ sư HVAC & Kiểm toán viên MEP
    dateFormat  YYYY-MM-DD
    section Giai đoạn 1: Nền tảng
    Mod 1: Nhiệt ẩm & RTS Load          :a1, 2026-11-01, 3w
    Mod 2: Khí động & Thủy lực          :a2, after a1, 3w
    section Giai đoạn 2: Thiết kế Hệ thống
    Mod 3: Chiller Plant & Heat Pump     :a3, after a2, 3w
    Mod 4: Công trình Chuyên biệt       :a4, after a3, 2w
    section Giai đoạn 3: Năng lượng & Kiểm toán
    Mod 5: Quy chuẩn ASHRAE 90.1 & QCVN 09:a5, after a4, 2w
    Mod 6: Kiểm toán Năng lượng ISO 50002:a6, after a5, 2w
    Mod 7: Cx, TAB, FDD & Capstone      :a7, after a6, 1w
```

---

### GIAI ĐOẠN 1: NỀN TẢNG KỸ THUẬT VÀ TÍNH TOÁN ĐỘNG LỰC HỌC

#### TUẦN 01 - 03: MODULE 1 - NHIỆT ẨM HỌC & TÍNH TOÁN TẢI LÀM LẠNH RTS
* **Mục tiêu lý thuyết:**
  - Nắm vững 7 thông số trạng thái không khí ẩm: $T_{db}, T_{wb}, T_{dp}, RH, W, h, v$ trên đồ thị Psychrometric chart.
  - Các quá trình biến đổi nhiệt ẩm: Làm lạnh khử ẩm, sưởi ấm, hòa trộn 2 dòng khí, quá trình qua dàn lạnh với điểm đọng sương bề mặt thiết bị (ADP) và hệ số lọt gió (Bypass Factor - BF).
  - Phương pháp tính tải làm lạnh RTS (Radiant Time Series) của ASHRAE: Phân biệt Heat Gain tức thời và Cooling Load có xét đến độ trễ bức xạ và quán tính nhiệt kết cấu tường/sàn bê tông.
* **Tài liệu học tập bắt buộc:**
  - ASHRAE Handbook of Fundamentals - Chapter 1 (Psychrometrics), Chapter 14 (Climatic Design Information), Chapter 18 (Nonresidential Cooling Load).
  - QCVN 02:2022/BXD - Số liệu khí hậu tự nhiên Việt Nam (Nhiệt độ tính toán mùa hè tần suất 1%, 2.5%).
* **Bài tập & Đề án Tool:**
  - Viết module Python/Excel tính toán toàn bộ thông số nhiệt ẩm từ phương trình áp suất hơi bão hòa ASHRAE Eq. 5 & 6.
  - Lập bảng tính tải đỉnh cho 5 phòng với các hướng kính khác nhau, tính tải nhiệt truyền qua kết cấu ($U \cdot A \cdot \Delta T$), bức xạ kính ($SHGC$), nhiệt người ($Sensible/Latent$), chiếu sáng ($W/m^2$), thiết bị văn phòng và gió tươi ($ASHRAE 62.1$).

---

#### TUẦN 04 - 06: MODULE 2 - KHÍ ĐỘNG HỌC MẠNG GIÓ & THỦY LỰC MẠNG NƯỚC
* **Mục tiêu lý thuyết:**
  - Khí động học ống gió: Phương pháp ma sát đồng đều (Equal Friction) và Phục hồi áp suất tĩnh (Static Regain). Đường kính ống tròn tương đương Huebscher.
  - Giới hạn vận tốc âm học để chống ồn (NC/NR Criteria) cho các khu vực nhạy cảm (Phòng họp, phòng ngủ khách sạn, phòng giám đốc).
  - Tính toán tổn thất cột áp tĩnh ngoài của quạt (Fan ESP): Ống thẳng, co cút tee, van dập lửa chì (FD/NFD), van VAV Box, dàn coil làm lạnh, phin lọc sơ cấp/thứ cấp (G4/F7/F8).
  - Thủy lực mạng nước lạnh (Chilled Water): Phương trình Darcy-Weisbach, Colebrook-White, tổn thất qua phụ kiện ($K$-factor, $Cv/Kv$).
  - Hiện tượng xâm thực khí (Cavitation) và kiểm soát cột áp hút dương khả dụng ($NPSHa > NPSHr$).
* **Tài liệu học tập bắt buộc:**
  - ASHRAE Fundamentals - Chapter 21 (Duct Design), Chapter 22 (Pipe Sizing).
  - TCVN 5687:2024 - Thông gió và điều hòa không khí.
* **Bài tập & Đề án Tool:**
  - Lập trình thuật toán tự động chọn kích thước ống gió chữ nhật chuẩn hóa (bội số 50 mm) từ lưu lượng và ma sát mục tiêu ($0.8 - 1.0\text{ Pa/m}$).
  - Lập bảng tính thủy lực mạng đường ống nước lạnh ChW/CdW: Tự động tra cỡ ống SCH40/ống hàn, tính tổn thất áp suất theo Darcy-Weisbach, tính cột áp bơm và công suất động cơ bơm.

---

### GIAI ĐOẠN 2: THIẾT KẾ HỆ THỐNG NGUỒN NHIỆT LẠNH & ĐẶC THÙ CÔNG TRÌNH

#### TUẦN 07 - 09: MODULE 3 - MÔ PHỎNG TRẠM LẠNH CHILLER PLANT & BƠM NHIỆT HEAT PUMP
* **Mục tiêu lý thuyết:**
  - Nguyên lý máy nén Chiller (Centrifugal ly tâm, Screw trục vít, Scroll cuộn). Đánh giá COP, EER, kW/RT, IPLV/NPLV theo AHRI 550/590.
  - Sơ đồ nguyên lý thủy lực: Constant Primary, Primary-Secondary (Bơm sơ cấp/thứ cấp), Primary Variable Flow (VPF - Bơm sơ cấp biến lưu lượng toàn phần). Thiết kế van bypass lưu lượng tối thiểu (Minimum flow bypass valve).
  - Tháp giải nhiệt (Cooling Tower): Hiệu số Range, Approach. Tối ưu nhiệt độ nước giải nhiệt hồi theo nhiệt độ bầu ướt ngoài trời (Wet-bulb Reset).
  - Bơm nhiệt Heat Pump: Chu trình sinh nước nóng $60^\circ C$ sinh hoạt (DHW), tận dụng nhiệt ngưng tụ Chiller để tiết kiệm điện.
* **Tài liệu học tập bắt buộc:**
  - ASHRAE HVAC Systems & Equipment (Chillers, Cooling Towers, Pumps).
  - AHRI Standard 550/590.
* **Bài tập & Đề án Tool:**
  - Xây dựng mô hình mô phỏng Part-load Chiller Plant: Đánh giá tổng công suất điện tiêu thụ toàn trạm (Chiller + Bơm ChW + Bơm CdW + Tháp giải nhiệt) tại các mức tải 25%, 50%, 75%, 100%.
  - Lập bảng so sánh LCC chi phí điện năng 15 năm giữa hệ thống VPF (biến tần toàn phần) và hệ thống sơ cấp/thứ cấp truyền thống.

---

#### TUẦN 10 - 11: MODULE 4 - THIẾT KẾ CHUYÊN BIỆT THEO LOẠI HÌNH CÔNG TRÌNH
* **Mục tiêu lý thuyết:**
  - **Tòa nhà văn phòng thương mại:** Hệ VAV kết hợp xử lý khí tươi PAU/DOAS; thu hồi nhiệt bánh xe quay (Heat Recovery Wheel / HRV); điều khiển chiếu sáng và điều hòa theo cảm biến CO2 và hiện diện (Occupancy).
  - **Khách sạn & Resort:** Nước nóng trung tâm Heat Pump; giải pháp chống đọng sương cửa kính và hành lang ẩm ướt nhiệt đới; tiêu chuẩn độ ồn NC 25-28.
  - **Bệnh viện & Phòng mổ (ASHRAE 170):** Khống chế bội số trao đổi khí $\ge 20\text{ ACH}$, gió tươi $\ge 4\text{ ACH}$, áp suất dương phòng mổ $+2.5\text{ Pa}$, phòng cách ly áp âm $-2.5\text{ Pa}$, lọc HEPA trần Laminar.
  - **Trung tâm dữ liệu (ASHRAE TC 9.9):** Mật độ tải nhiệt cao ($kW/rack$), chỉ số hiệu quả năng lượng PUE, luồng khí lạnh/nóng cô lập (Cold/Hot Aisle Containment), làm mát CRAH/In-row.
  - **Nhà máy công nghiệp:** Cân bằng nhiệt thải nhà xưởng, thông gió hút khói khí độc (ACGIH Industrial Ventilation), làm mát áp suất dương làm mát bay hơi (Evaporative Cooling).
* **Bài tập & Đề án Tool:**
  - Xây dựng module tính toán kiểm tra áp suất và lưu lượng phòng mổ theo ASHRAE 170.
  - Xây dựng công cụ tính toán chỉ số PUE và đánh giá hiệu quả giải nhiệt Data Center theo ASHRAE TC 9.9.

---

### GIAI ĐOẠN 3: HIỆU QUẢ NĂNG LƯỢNG, KIỂM TOÁN ISO 50002 & COMMISSIONING

#### TUẦN 12 - 13: MODULE 5 - QUY CHUẨN NĂNG LƯỢNG (ASHRAE 90.1 & QCVN 09:2017)
* **Mục tiêu lý thuyết:**
  - Quy chuẩn QCVN 09:2017/BXD: Tính toán chỉ số truyền nhiệt tổng của tường và mái $OTTV \le 60\text{ W/m}^2$, tỷ lệ diện tích kính trên tường (WWR).
  - Mật độ công suất chiếu sáng (LPD - $W/m^2$) theo Building Area Method và Space-by-Space Method.
  - Giới hạn hiệu suất thiết bị tối thiểu: COP Chiller, Fan Power Limitation ($kW/(m^3/s)$), động cơ IE3/IE4.
* **Bài tập & Đề án Tool:**
  - Lập công cụ thẩm định tự động hồ sơ thiết kế cơ sở: Nhập diện tích tường, kính, loại kính (U-value, SHGC) -> Tự động xuất kết luận Đạt/Không đạt theo QCVN 09 và ASHRAE 90.1-2022.

---

#### TUẦN 14 - 15: MODULE 6 - KIỂM TOÁN NĂNG LƯỢNG ISO 50002 & M&V
* **Mục tiêu lý thuyết:**
  - Quy trình kiểm toán năng lượng 3 cấp độ (Level 1 Walk-through, Level 2 Detailed, Level 3 Investment-Grade) theo ISO 50002 & ASHRAE 211.
  - Thiết lập Đường cơ sở năng lượng (Energy Baseline - EnB) bằng hồi quy đa biến theo độ ngày làm lạnh (CDD).
  - Kỹ thuật đo đạc thực địa: Đo lưu lượng siêu âm, đo nhiệt độ RTD Pt100, đo công suất điện 3 pha PQA.
  - Chẩn đoán các bệnh lý vận hành: Hội chứng chênh nhiệt độ thấp (Low Delta-T Syndrome), cáu cặn bình ngưng (Condenser Fouling), van bypass rò rỉ.
  - Thư viện giải pháp tiết kiệm năng lượng (ECMs) và phân tích tài chính đầu tư (LCCA: Simple Payback, NPV, IRR).
* **Bài tập & Đề án Tool:**
  - Xử lý bộ dữ liệu log thực địa của Chiller Plant 1000 RT: Tính công suất lạnh thực tế, tính $kW/RT$ thực tế, phát hiện Low Delta-T.
  - Lập đề xuất ECM lắp VFD cho bơm, tính dòng tiền chiết khấu NPV, IRR cho báo cáo kiểm toán.

---

#### TUẦN 16: MODULE 7 - COMMISSIONING (Cx), TAB & CAPSTONE DEFENSE
* **Mục tiêu lý thuyết:**
  - Quy trình Chạy thử nghiệm thu (Commissioning - Cx) theo ASHRAE Guideline 0 & 1.1.
  - Quy trình thử nghiệm và cân bằng hệ thống (TAB - Testing, Adjusting, Balancing): Phương pháp cân bằng tỷ lệ (Proportional Balancing) mạng gió và mạng nước.
  - Hệ thống phát hiện lỗi và chẩn đoán tự động (Automated Fault Detection and Diagnostics - FDD).
* **Đề án Tốt nghiệp (Capstone Defense):**
  - Học viên bảo vệ 1 Báo cáo Kiểm toán Năng lượng hoặc 1 Hồ sơ Thiết kế Kỹ thuật hoàn chỉnh cho công trình thực tế, toàn bộ bảng tính và mô phỏng được thực hiện bằng bộ Tool tự xây dựng.
