"""
Script tự động sinh Workbook Excel: MEP_Energy_Auditor_Master_Toolkit.xlsx
Tuân thủ tiêu chuẩn trình bày chuyên nghiệp của RFR Energy & MEP.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_workbook():
    wb = openpyxl.Workbook()
    # Xóa sheet mặc định
    wb.remove(wb.active)

    # Bảng màu chuẩn RFR Corporate Engineering
    NAVY_HEADER = "1A365D"      # Xanh navy đậm cho tiêu đề chính
    STEEL_BLUE = "2B6CB0"       # Xanh thép cho tiêu đề mục
    LIGHT_BLUE = "EBF8FF"       # Xanh nhạt cho nhóm cột
    INPUT_FILL = "FEFCBF"       # Vàng kem nhạt cho ô nhập liệu (User Input)
    CALC_FILL = "EDF2F7"        # Xám nhạt cho ô công thức tính toán
    PASS_FILL = "C6F6D5"        # Xanh lá cho Đạt / Xuất sắc
    WARN_FILL = "FEEBC8"        # Cam nhạt cho Cảnh báo
    FAIL_FILL = "FED7D7"        # Đỏ nhạt cho Không đạt

    font_title = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
    font_section = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Segoe UI", size=10, bold=True)
    font_regular = Font(name="Segoe UI", size=10)
    font_small = Font(name="Segoe UI", size=9, italic=True, color="4A5568")

    fill_navy = PatternFill(start_color=NAVY_HEADER, end_color=NAVY_HEADER, fill_type="solid")
    fill_steel = PatternFill(start_color=STEEL_BLUE, end_color=STEEL_BLUE, fill_type="solid")
    fill_input = PatternFill(start_color=INPUT_FILL, end_color=INPUT_FILL, fill_type="solid")
    fill_calc = PatternFill(start_color=CALC_FILL, end_color=CALC_FILL, fill_type="solid")
    fill_pass = PatternFill(start_color=PASS_FILL, end_color=PASS_FILL, fill_type="solid")
    fill_warn = PatternFill(start_color=WARN_FILL, end_color=WARN_FILL, fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='CBD5E0'),
        right=Side(style='thin', color='CBD5E0'),
        top=Side(style='thin', color='CBD5E0'),
        bottom=Side(style='thin', color='CBD5E0')
    )
    header_border = Border(
        left=Side(style='thin', color='A0AEC0'),
        right=Side(style='thin', color='A0AEC0'),
        top=Side(style='medium', color='1A365D'),
        bottom=Side(style='medium', color='1A365D')
    )

    # =========================================================================
    # SHEET 0: DASHBOARD TỔNG QUAN
    # =========================================================================
    ws0 = wb.create_sheet(title="00_DASHBOARD")
    ws0.views.sheetView[0].showGridLines = True
    
    ws0.merge_cells("B2:J2")
    ws0["B2"] = "MEP & ENERGY AUDITOR MASTER DASHBOARD - TỔNG QUAN DỰ ÁN"
    ws0["B2"].font = font_title
    ws0["B2"].fill = fill_navy
    ws0["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws0.row_dimensions[2].height = 36

    info_data = [
        ("Tên dự án:", "TÒA NHÀ TRUNG TÂM THƯƠNG MẠI & VĂN PHÒNG SAO KHUÊ"),
        ("Địa điểm xây dựng:", "Quận 1, TP. Hồ Chí Minh (Khí hậu QCVN 02: Vùng nhiệt đới gió mùa)"),
        ("Loại hình công trình:", "Văn phòng Hạng A kết hợp Thương mại Dịch vụ"),
        ("Tổng diện tích sàn (GFA):", 25000),  # m2
        ("Số tầng nổi / Hầm:", "22 tầng nổi / 3 tầng hầm"),
        ("Hệ thống ĐHKK áp dụng:", "Hệ Chiller giải nhiệt nước trung tâm VPF + AHU/VAV"),
        ("Tiêu chuẩn đối chiếu:", "ASHRAE 90.1-2022, QCVN 09:2017/BXD, ISO 50002:2015, ASHRAE 62.1"),
        ("Chủ trì thiết kế / Kiểm toán viên:", "RFR MEP & Energy Audit Group")
    ]
    for idx, (label, val) in enumerate(info_data, start=4):
        ws0.cell(row=idx, column=2, value=label).font = font_bold
        c_val = ws0.cell(row=idx, column=3, value=val)
        c_val.font = font_regular
        if isinstance(val, (int, float)):
            c_val.number_format = "#,##0"
            c_val.fill = fill_input
        ws0.merge_cells(start_row=idx, start_column=3, end_row=idx, end_column=6)

    # Bảng Tóm tắt KPI Năng lượng & Thiết kế
    ws0.merge_cells("B13:J13")
    ws0["B13"] = "CHỈ SỐ HIỆU NĂNG NĂNG LƯỢNG & ĐÁNH GIÁ TRỌNG YẾU (KEY PERFORMANCE INDICATORS)"
    ws0["B13"].font = font_section
    ws0["B13"].fill = fill_steel
    ws0.row_dimensions[13].height = 24

    kpis = [
        ("Chỉ số cường độ sử dụng năng lượng EUI", "kWh/m2.năm", "='06_ISO50002_ENERGY_AUDIT'!C8", "110 - 140", "Đạt chuẩn Văn phòng Xanh"),
        ("Tổng tải lạnh đỉnh toàn công trình", "RT", "='01_PSYCHROMETRICS_LOAD'!H20", "Theo thiết kế", "Đã bao gồm hệ số đồng thời"),
        ("Chỉ số truyền nhiệt vỏ bao che OTTV tường", "W/m2", "='05_ENERGY_CODE_COMPLIANCE'!C15", "< 60.0 W/m2", "Tuân thủ QCVN 09:2017"),
        ("Hiệu suất Trạm Chiller Plant thực tế", "kW/RT", "='03_CHILLER_PLANT_SIM'!E15", "< 0.75 kW/RT", "Hệ thống hiệu suất cao"),
        ("Mật độ công suất chiếu sáng LPD văn phòng", "W/m2", "='05_ENERGY_CODE_COMPLIANCE'!C23", "< 6.5 W/m2", "Tuân thủ ASHRAE 90.1-2022"),
        ("Tiềm năng tiết kiệm điện từ kiểm toán (ECMs)", "VNĐ/năm", "='06_ISO50002_ENERGY_AUDIT'!E27", "Theo phân tích", "Thời gian hoàn vốn < 2.5 năm")
    ]
    headers_kpi = ["Chỉ số / Thông số thiết kế", "Đơn vị", "Giá trị tính toán", "Mức chuẩn Benchmark", "Đánh giá sơ bộ"]
    for c_idx, h in enumerate(headers_kpi, start=2):
        c = ws0.cell(row=14, column=c_idx, value=h)
        c.font = font_bold
        c.fill = PatternFill(start_color="CBD5E0", end_color="CBD5E0", fill_type="solid")
        c.alignment = Alignment(horizontal="center")

    for r_idx, (name, unit, fmla, bench, eval_str) in enumerate(kpis, start=15):
        ws0.cell(row=r_idx, column=2, value=name).font = font_regular
        ws0.cell(row=r_idx, column=3, value=unit).alignment = Alignment(horizontal="center")
        val_cell = ws0.cell(row=r_idx, column=4, value=fmla)
        val_cell.font = font_bold
        val_cell.fill = fill_calc
        val_cell.alignment = Alignment(horizontal="right")
        if "VNĐ" in unit:
            val_cell.number_format = "#,##0"
        else:
            val_cell.number_format = "#,##0.0"
        ws0.cell(row=r_idx, column=5, value=bench).alignment = Alignment(horizontal="center")
        ws0.cell(row=r_idx, column=6, value=eval_str).alignment = Alignment(horizontal="left")

    # =========================================================================
    # SHEET 1: NHIỆT ẨM HỌC & TÍNH TẢI RTS (01_PSYCHROMETRICS_LOAD)
    # =========================================================================
    ws1 = wb.create_sheet(title="01_PSYCHROMETRICS_LOAD")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells("B2:H2")
    ws1["B2"] = "MODULE 1: NHIỆT ẨM HỌC & TÍNH TẢI ĐỈNH (ASHRAE FUNDAMENTALS & RTS METHOD)"
    ws1["B2"].font = font_title
    ws1["B2"].fill = fill_navy
    ws1["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[2].height = 30

    ws1.cell(row=4, column=2, value="1.1 THÔNG SỐ ĐIỀU KIỆN THIẾT KẾ BIÊN").font = font_bold
    ws1.cell(row=5, column=2, value="Thông số")
    ws1.cell(row=5, column=3, value="Ngoại thất (QCVN 02 / ASHRAE 1%)")
    ws1.cell(row=5, column=4, value="Nội thất tiện nghi (ASHRAE 55)")
    ws1.cell(row=5, column=5, value="Đơn vị")
    for col in range(2, 6):
        c = ws1.cell(row=5, column=col)
        c.font = font_bold
        c.fill = PatternFill(start_color="CBD5E0", end_color="CBD5E0", fill_type="solid")

    design_conditions = [
        ("Nhiệt độ bầu khô (Dry-Bulb Temp)", 35.0, 24.0, "°C"),
        ("Độ ẩm tương đối (Relative Humidity)", 60.0, 55.0, "%"),
        ("Dung ẩm tuyệt đối (Humidity Ratio W)", 21.4, 10.2, "g/kg_da"),
        ("Enthalpy không khí (h)", 90.2, 50.2, "kJ/kg_da"),
        ("Nhiệt độ đọng sương (Dew-Point Temp)", 26.1, 14.4, "°C")
    ]
    for r_idx, (param, out_val, in_val, unit) in enumerate(design_conditions, start=6):
        ws1.cell(row=r_idx, column=2, value=param).font = font_regular
        c_out = ws1.cell(row=r_idx, column=3, value=out_val)
        c_in = ws1.cell(row=r_idx, column=4, value=in_val)
        ws1.cell(row=r_idx, column=5, value=unit).alignment = Alignment(horizontal="center")
        if r_idx in (6, 7):
            c_out.fill = fill_input
            c_in.fill = fill_input
            c_out.font = font_bold
            c_in.font = font_bold
        else:
            c_out.fill = fill_calc
            c_in.fill = fill_calc

    # Bảng tính tải làm lạnh phân vùng mẫu (Zone Load Matrix)
    ws1.cell(row=13, column=2, value="1.2 BẢNG PHÂN TÍCH TẢI LÀM LẠNH ĐỈNH (PEAK COOLING LOAD BREAKDOWN)").font = font_bold
    load_headers = [
        "Khu vực / Tên phòng", "Diện tích (m2)", "Tải vỏ bao che (W)", "Tải người (W)", 
        "Tải chiếu sáng (W)", "Tải thiết bị (W)", "Tải gió tươi (W)", "Tải tổng cộng (kW)", "Tải tổng cộng (RT)"
    ]
    for c_idx, h in enumerate(load_headers, start=2):
        c = ws1.cell(row=14, column=c_idx, value=h)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    ws1.row_dimensions[14].height = 28

    sample_zones = [
        ("Khu văn phòng mở Tầng 5", 850, 18500, 15000, 5950, 10200, 22400),
        ("Phòng họp lớn Boardroom", 120, 3200, 6500, 840, 1800, 12800),
        ("Khu vực Sảnh chính đón khách", 400, 15200, 8000, 3200, 2000, 28000),
        ("Khu vực Gian hàng Thương mại", 1200, 14000, 24000, 12000, 8400, 36000),
        ("Trung tâm vận hành IT / Server", 80, 1500, 800, 480, 45000, 2200),
    ]
    for r_idx, (z_name, area, env_w, occ_w, light_w, plug_w, vent_w) in enumerate(sample_zones, start=15):
        ws1.cell(row=r_idx, column=2, value=z_name).font = font_regular
        ws1.cell(row=r_idx, column=3, value=area).number_format = "#,##0"
        ws1.cell(row=r_idx, column=4, value=env_w).number_format = "#,##0"
        ws1.cell(row=r_idx, column=5, value=occ_w).number_format = "#,##0"
        ws1.cell(row=r_idx, column=6, value=light_w).number_format = "#,##0"
        ws1.cell(row=r_idx, column=7, value=plug_w).number_format = "#,##0"
        ws1.cell(row=r_idx, column=8, value=vent_w).number_format = "#,##0"
        
        # Công thức tính tổng kW = SUM(D:H)/1000
        c_kw = ws1.cell(row=r_idx, column=9, value=f"=SUM(D{r_idx}:H{r_idx})/1000")
        c_kw.font = font_bold
        c_kw.fill = fill_calc
        c_kw.number_format = "#,##0.1"
        
        # Công thức tính RT = kW / 3.51685
        c_rt = ws1.cell(row=r_idx, column=10, value=f"=I{r_idx}/3.51685")
        c_rt.font = font_bold
        c_rt.fill = fill_calc
        c_rt.number_format = "#,##0.1"

    # Hàng tổng cộng
    tot_row = 20
    ws1.cell(row=tot_row, column=2, value="TỔNG CỘNG CÔNG SUẤT (PEAK TOTAL):").font = font_bold
    ws1.cell(row=tot_row, column=3, value=f"=SUM(C15:C19)").number_format = "#,##0"
    for c_idx in range(4, 9):
        col_let = get_column_letter(c_idx)
        c = ws1.cell(row=tot_row, column=c_idx, value=f"=SUM({col_let}15:{col_let}19)")
        c.font = font_bold
        c.number_format = "#,##0"
    c_tot_kw = ws1.cell(row=tot_row, column=9, value=f"=SUM(I15:I19)")
    c_tot_kw.font = font_bold
    c_tot_kw.fill = fill_pass
    c_tot_kw.number_format = "#,##0.1"

    c_tot_rt = ws1.cell(row=tot_row, column=10, value=f"=SUM(J15:J19)")
    c_tot_rt.font = font_bold
    c_tot_rt.fill = fill_pass
    c_tot_rt.number_format = "#,##0.1"

    # =========================================================================
    # SHEET 2: KHÍ ĐỘNG HỌC & THỦY LỰC (02_DUCT_PIPE_SIZING)
    # =========================================================================
    ws2 = wb.create_sheet(title="02_DUCT_PIPE_SIZING")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("B2:I2")
    ws2["B2"] = "MODULE 2: KHÍ ĐỘNG HỌC ĐƯỜNG ỐNG GIÓ & THỦY LỰC ĐƯỜNG ỐNG NƯỚC (ASHRAE CH. 21 & 22)"
    ws2["B2"].font = font_title
    ws2["B2"].fill = fill_navy
    ws2["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws2.row_dimensions[2].height = 30

    # 2.1 Sizing Ống gió
    ws2.cell(row=4, column=2, value="2.1 TÍNH TOÁN KÍCH THƯỚC ĐƯỜNG ỐNG GIÓ (EQUAL FRICTION & HUEBSCHER)").font = font_bold
    duct_headers = ["Đoạn ống", "Lưu lượng (m3/h)", "Tổn thất mục tiêu (Pa/m)", "Đường kính tương đương De (mm)", "Rộng (mm)", "Cao (mm)", "Vận tốc thực tế (m/s)", "Tổn thất thực tế (Pa/m)"]
    for c_idx, h in enumerate(duct_headers, start=2):
        c = ws2.cell(row=5, column=c_idx, value=h)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    sample_ducts = [
        ("Trục chính AHU-01", 12000, 1.0, 750, 900, 500, 7.4, 0.95),
        ("Nhánh cấp tầng 5 - A", 6000, 1.0, 560, 650, 400, 6.4, 0.92),
        ("Nhánh cấp tầng 5 - B", 3500, 1.0, 450, 500, 350, 5.5, 0.88),
        ("Ống cấp vào VAV Box", 1200, 0.8, 300, 350, 250, 3.8, 0.75),
        ("Cổ miệng gió khuếch tán", 400, 0.6, 200, 200, 200, 2.8, 0.65)
    ]
    for r_idx, (d_name, flow, tg_dp, de, w, h, v, act_dp) in enumerate(sample_ducts, start=6):
        ws2.cell(row=r_idx, column=2, value=d_name).font = font_regular
        ws2.cell(row=r_idx, column=3, value=flow).number_format = "#,##0"
        ws2.cell(row=r_idx, column=4, value=tg_dp).number_format = "0.0"
        ws2.cell(row=r_idx, column=5, value=de).number_format = "#,##0"
        ws2.cell(row=r_idx, column=6, value=w).number_format = "#,##0"
        ws2.cell(row=r_idx, column=7, value=h).number_format = "#,##0"
        ws2.cell(row=r_idx, column=8, value=v).number_format = "0.0"
        ws2.cell(row=r_idx, column=9, value=act_dp).number_format = "0.00"

    # 2.2 Sizing Ống nước lạnh
    ws2.cell(row=13, column=2, value="2.2 TÍNH TOÁN THỦY LỰC ĐƯỜNG ỐNG NƯỚC LẠNH (CHILLED WATER SIZING)").font = font_bold
    pipe_headers = ["Đoạn tuyến ống nước", "Tải làm lạnh (kW)", "Delta T (°C)", "Lưu lượng (m3/h)", "Lưu lượng (GPM)", "Cỡ ống danh định", "Vận tốc (m/s)", "Tổn thất ma sát (mH2O/100m)"]
    for c_idx, h in enumerate(pipe_headers, start=2):
        c = ws2.cell(row=14, column=c_idx, value=h)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    sample_pipes = [
        ("Header tổng Chiller 500 RT", 1758.0, 5.5, "=C15*3600/(1000*4.186*D15)", "=E15*4.40287", "DN250", 1.54, 1.45),
        ("Đường nhánh 1 Chiller 250 RT", 879.0, 5.5, "=C16*3600/(1000*4.186*D16)", "=E16*4.40287", "DN200", 1.22, 1.05),
        ("Trục đứng Riser cấp tầng 1-10", 700.0, 5.5, "=C17*3600/(1000*4.186*D17)", "=E17*4.40287", "DN150", 1.62, 2.10),
        ("Ống cấp AHU Tầng điển hình", 120.0, 5.5, "=C18*3600/(1000*4.186*D18)", "=E18*4.40287", "DN65", 1.45, 2.85),
        ("Ống nhánh cấp cụm FCU", 35.0, 5.5, "=C19*3600/(1000*4.186*D19)", "=E19*4.40287", "DN32", 1.15, 2.90),
    ]
    for r_idx, (p_name, kw, dt, flow_fmla, gpm_fmla, dn, v, hf) in enumerate(sample_pipes, start=15):
        ws2.cell(row=r_idx, column=2, value=p_name).font = font_regular
        ws2.cell(row=r_idx, column=3, value=kw).number_format = "#,##0.0"
        ws2.cell(row=r_idx, column=4, value=dt).number_format = "0.0"
        
        c_flow = ws2.cell(row=r_idx, column=5, value=flow_fmla)
        c_flow.font = font_bold
        c_flow.fill = fill_calc
        c_flow.number_format = "#,##0.1"
        
        c_gpm = ws2.cell(row=r_idx, column=6, value=gpm_fmla)
        c_gpm.font = font_bold
        c_gpm.fill = fill_calc
        c_gpm.number_format = "#,##0.1"
        
        ws2.cell(row=r_idx, column=7, value=dn).alignment = Alignment(horizontal="center")
        ws2.cell(row=r_idx, column=8, value=v).number_format = "0.00"
        ws2.cell(row=r_idx, column=9, value=hf).number_format = "0.00"

    # =========================================================================
    # SHEET 3: MÔ PHỎNG TRẠM LẠNH CHILLER PLANT (03_CHILLER_PLANT_SIM)
    # =========================================================================
    ws3 = wb.create_sheet(title="03_CHILLER_PLANT_SIM")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.merge_cells("B2:I2")
    ws3["B2"] = "MODULE 3: MÔ PHỎNG TRẠM CHILLER GIẢI NHIỆT NƯỚC & ĐÁNH GIÁ HIỆU SUẤT TOÀN TRẠM"
    ws3["B2"].font = font_title
    ws3["B2"].fill = fill_navy
    ws3["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws3.row_dimensions[2].height = 30

    ws3.cell(row=4, column=2, value="3.1 THÔNG SỐ CẤU HÌNH THIẾT BỊ TRẠM LẠNH").font = font_bold
    plant_params = [
        ("Công suất Chiller đơn vị:", 500, "RT (Tấn lạnh)"),
        ("Số lượng Chiller vận hành:", 2, "Tổ máy"),
        ("Tổng công suất làm lạnh trạm:", "=C5*C6", "RT"),
        ("Hiệu suất Chiller đầy tải định mức:", 0.58, "kW/RT (COP ~ 6.06)"),
        ("Hiệu suất Chiller non tải IPLV:", 0.38, "kW/RT (COP ~ 9.25)"),
        ("Nhiệt độ nước lạnh cấp / hồi:", "7.0 / 12.5", "°C (Delta T = 5.5°C)"),
        ("Nhiệt độ nước giải nhiệt vào / ra:", "30.0 / 35.0", "°C (Range = 5.0°C)"),
    ]
    for idx, (label, val, unit) in enumerate(plant_params, start=5):
        ws3.cell(row=idx, column=2, value=label).font = font_regular
        c = ws3.cell(row=idx, column=3, value=val)
        c.font = font_bold
        if isinstance(val, (int, float)):
            c.fill = fill_input
            c.number_format = "#,##0.00"
        elif str(val).startswith("="):
            c.fill = fill_calc
            c.number_format = "#,##0"
        ws3.cell(row=idx, column=4, value=unit).alignment = Alignment(horizontal="left")

    # Bảng phân tích hiệu suất thực tế toàn trạm
    ws3.cell(row=13, column=2, value="3.2 PHÂN BỔ CÔNG SUẤT TIÊU THỤ ĐIỆN TOÀN TRẠM (TOTAL PLANT kW/RT BREAKDOWN)").font = font_bold
    ws3.cell(row=14, column=2, value="Thành phần thiết bị")
    ws3.cell(row=14, column=3, value="Số lượng chạy")
    ws3.cell(row=14, column=4, value="Công suất điện đo đạc (kW)")
    ws3.cell(row=14, column=5, value="Tỷ trọng điện (%)")
    ws3.cell(row=14, column=6, value="Chỉ số riêng phần (kW/RT)")
    for col in range(2, 7):
        c = ws3.cell(row=14, column=col)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    equip_breakdown = [
        ("Máy làm lạnh nước (Water-Cooled Chillers)", 2, 440.0, "=D15/$D$19", "=D15/$C$7"),
        ("Bơm nước lạnh sơ cấp biến tần (ChW Pumps)", 2, 38.0, "=D16/$D$19", "=D16/$C$7"),
        ("Bơm nước giải nhiệt (CdW Pumps)", 2, 52.0, "=D17/$D$19", "=D17/$C$7"),
        ("Quạt tháp giải nhiệt (Cooling Tower Fans)", 2, 22.0, "=D18/$D$19", "=D18/$C$7"),
    ]
    for r_idx, (name, qty, kw, pct_fmla, part_fmla) in enumerate(equip_breakdown, start=15):
        ws3.cell(row=r_idx, column=2, value=name).font = font_regular
        ws3.cell(row=r_idx, column=3, value=qty).alignment = Alignment(horizontal="center")
        ws3.cell(row=r_idx, column=4, value=kw).number_format = "#,##0.0"
        c_pct = ws3.cell(row=r_idx, column=5, value=pct_fmla)
        c_pct.number_format = "0.0%"
        c_pct.fill = fill_calc
        c_part = ws3.cell(row=r_idx, column=6, value=part_fmla)
        c_part.number_format = "0.000"
        c_part.fill = fill_calc

    # Tổng cộng
    ws3.cell(row=19, column=2, value="TỔNG CÔNG SUẤT TOÀN TRẠM (TOTAL PLANT):").font = font_bold
    ws3.cell(row=19, column=4, value="=SUM(D15:D18)").font = font_bold
    ws3.cell(row=19, column=4).fill = fill_calc
    ws3.cell(row=19, column=4).number_format = "#,##0.0"
    
    ws3.cell(row=19, column=5, value="=SUM(E15:E18)").font = font_bold
    ws3.cell(row=19, column=5).number_format = "0.0%"

    c_tot_eff = ws3.cell(row=19, column=6, value="=D19/$C$7")
    c_tot_eff.font = font_bold
    c_tot_eff.fill = fill_pass
    c_tot_eff.number_format = "0.000"

    ws3.cell(row=21, column=2, value="ĐÁNH GIÁ CHỈ SỐ HIỆU SUẤT TOÀN TRẠM:").font = font_bold
    ws3.cell(row=21, column=3, value="HỆ THỐNG ĐẠT HIỆU NĂNG CAO (HIGH PERFORMANCE)").font = font_bold
    ws3.cell(row=21, column=3).fill = fill_pass
    ws3.cell(row=22, column=2, value="Khuyến nghị vận hành:").font = font_small
    ws3.cell(row=22, column=3, value="Tiếp tục tối ưu điểm đặt ChW Temp Reset theo tải thực tế & kiểm soát nhiệt độ nước ngưng tiếp cận nhiệt độ bầu ướt (Wet-bulb Approach <= 3°C).").font = font_small

    # =========================================================================
    # SHEET 4: CÔNG TRÌNH CHUYÊN BIỆT (04_SPECIALIZED_FACILITY)
    # =========================================================================
    ws4 = wb.create_sheet(title="04_SPECIALIZED_FACILITY")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4.merge_cells("B2:H2")
    ws4["B2"] = "MODULE 4: CẤU HÌNH THIẾT KẾ CHUYÊN BIỆT THEO LOẠI HÌNH CÔNG TRÌNH (ASHRAE APPLICATIONS)"
    ws4["B2"].font = font_title
    ws4["B2"].fill = fill_navy
    ws4["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws4.row_dimensions[2].height = 30

    # 4.1 Bệnh viện (ASHRAE 170)
    ws4.cell(row=4, column=2, value="4.1 PHÒNG MỔ BỆNH VIỆN (OPERATING THEATRE - ASHRAE STANDARD 170)").font = font_bold
    hosp_data = [
        ("Diện tích phòng mổ (m2):", 50.0, "m2"),
        ("Chiều cao thông thủy (m):", 3.2, "m"),
        ("Thể tích phòng (m3):", "=C5*C6", "m3"),
        ("Bội số trao đổi khí tổng yêu cầu (Total ACH):", 20.0, "ACH (Tối thiểu theo ASHRAE 170)"),
        ("Bội số gió tươi ngoài (Outdoor ACH):", 4.0, "ACH"),
        ("Lưu lượng gió cấp tổng yêu cầu:", "=C7*C8", "m3/h"),
        ("Lưu lượng gió tươi ngoài yêu cầu:", "=C7*C9", "m3/h"),
        ("Duy trì chênh áp phòng mổ:", "+2.5", "Pa (Áp suất dương chống lây nhiễm)")
    ]
    for idx, (label, val, note) in enumerate(hosp_data, start=5):
        ws4.cell(row=idx, column=2, value=label).font = font_regular
        c = ws4.cell(row=idx, column=3, value=val)
        c.font = font_bold
        if isinstance(val, (int, float)):
            c.fill = fill_input
            c.number_format = "#,##0.0"
        elif str(val).startswith("="):
            c.fill = fill_calc
            c.number_format = "#,##0"
        ws4.cell(row=idx, column=4, value=note).font = font_small

    # 4.2 Data Center PUE (ASHRAE TC 9.9)
    ws4.cell(row=15, column=2, value="4.2 TRUNG TÂM DỮ LIỆU & ĐÁNH GIÁ PUE (DATA CENTER - ASHRAE TC 9.9)").font = font_bold
    dc_data = [
        ("Tổng công suất tiêu thụ Server / IT (kW):", 600.0, "kW (Nhiệt hiện 100%)"),
        ("Công suất điện hệ thống làm mát CRAH/Chiller (kW):", 185.0, "kW"),
        ("Tổn hao hệ thống điện UPS & Phân phối (kW):", 45.0, "kW"),
        ("Điện chiếu sáng & phụ trợ khác (kW):", 10.0, "kW"),
        ("TỔNG CÔNG SUẤT TOÀN BỘ DATA CENTER (kW):", "=SUM(C16:C19)", "kW"),
        ("CHỈ SỐ HIỆU QUẢ NĂNG LƯỢNG (PUE):", "=C20/C16", "PUE = Total Power / IT Power"),
        ("Xếp hạng hiệu quả PUE:", "TỐT (Modern Enterprise Data Center)", "Target PUE < 1.4")
    ]
    for idx, (label, val, note) in enumerate(dc_data, start=16):
        ws4.cell(row=idx, column=2, value=label).font = font_regular
        c = ws4.cell(row=idx, column=3, value=val)
        c.font = font_bold
        if isinstance(val, (int, float)):
            c.fill = fill_input
            c.number_format = "#,##0.0"
        elif str(val).startswith("="):
            c.fill = fill_calc
            c.number_format = "0.00" if idx == 21 else "#,##0.0"
        ws4.cell(row=idx, column=4, value=note).font = font_small

    # =========================================================================
    # SHEET 5: QUY CHUẨN NĂNG LƯỢNG (05_ENERGY_CODE_COMPLIANCE)
    # =========================================================================
    ws5 = wb.create_sheet(title="05_ENERGY_CODE_COMPLIANCE")
    ws5.views.sheetView[0].showGridLines = True
    
    ws5.merge_cells("B2:H2")
    ws5["B2"] = "MODULE 5: KIỂM TRA TUÂN THỦ QUY CHUẨN NĂNG LƯỢNG (QCVN 09:2017 & ASHRAE 90.1)"
    ws5["B2"].font = font_title
    ws5["B2"].fill = fill_navy
    ws5["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws5.row_dimensions[2].height = 30

    # 5.1 OTTV
    ws5.cell(row=4, column=2, value="5.1 CHỈ SỐ TRUYỀN NHIỆT TỔNG VỎ BAO CHE (OTTV TƯỜNG NGOÀI - QCVN 09)").font = font_bold
    ottv_inputs = [
        ("Diện tích toàn bộ bề mặt tường ngoài (Aw_tot):", 1200.0, "m2"),
        ("Diện tích cửa sổ kính (Af):", 420.0, "m2"),
        ("Tỷ lệ cửa kính trên tường (WWR):", "=C6/C5", "- (Quy chuẩn WWR <= 0.50)"),
        ("Hệ số truyền nhiệt tường xây U_wall:", 1.75, "W/(m2.K)"),
        ("Hệ số truyền nhiệt kính U_glass:", 2.20, "W/(m2.K)"),
        ("Hệ số hấp thụ bức xạ nhiệt mặt trời SHGC kính:", 0.32, "- (Kính phủ Low-E)"),
        ("Chênh lệch nhiệt độ tương đương TDeq:", 12.0, "°C"),
        ("Bức xạ mặt trời tương đương SF:", 130.0, "W/m2"),
        ("CHỈ SỐ OTTV TƯỜNG TÍNH TOÁN:", "=((C5-C6)*C8*C11 + C6*C9*5.0 + C6*C10*C12)/C5", "W/m2"),
        ("Giới hạn tối đa theo QCVN 09:2017/BXD:", 60.0, "W/m2"),
        ("KẾT LUẬN TUÂN THỦ VỎ BAO CHE:", "=IF(C13<=C14, \"ĐẠT (PASS)\", \"KHÔNG ĐẠT (FAIL)\")", "Tuân thủ QCVN 09")
    ]
    for idx, (label, val, note) in enumerate(ottv_inputs, start=5):
        ws5.cell(row=idx, column=2, value=label).font = font_regular
        c = ws5.cell(row=idx, column=3, value=val)
        c.font = font_bold
        if isinstance(val, (int, float)):
            c.fill = fill_input
            c.number_format = "#,##0.00"
        elif str(val).startswith("="):
            c.fill = fill_calc
            c.number_format = "0.0%" if idx == 7 else "0.0"
        ws5.cell(row=idx, column=4, value=note).font = font_small
    ws5["C15"].fill = fill_pass

    # 5.2 LPD
    ws5.cell(row=17, column=2, value="5.2 MẬT ĐỘ CÔNG SUẤT CHIẾU SÁNG (LPD - LIGHTING POWER DENSITY)").font = font_bold
    ws5.cell(row=18, column=2, value="Loại hình không gian")
    ws5.cell(row=18, column=3, value="LPD Thiết kế (W/m2)")
    ws5.cell(row=18, column=4, value="QCVN 09:2017 (W/m2)")
    ws5.cell(row=18, column=5, value="ASHRAE 90.1-2022 (W/m2)")
    ws5.cell(row=18, column=6, value="Đánh giá tuân thủ")
    for col in range(2, 7):
        c = ws5.cell(row=18, column=col)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    lpd_rows = [
        ("Văn phòng làm việc", 5.8, 9.0, 6.5, "=IF(C19<=E19, \"ĐẠT ASHRAE & QCVN\", \"CHƯA ĐẠT\")"),
        ("Phòng họp", 7.2, 10.0, 7.5, "=IF(C20<=E20, \"ĐẠT ASHRAE & QCVN\", \"CHƯA ĐẠT\")"),
        ("Hành lang & Sảnh", 4.2, 6.0, 4.5, "=IF(C21<=E21, \"ĐẠT ASHRAE & QCVN\", \"CHƯA ĐẠT\")"),
        ("Tầng hầm đỗ xe", 2.2, 3.5, 2.5, "=IF(C22<=E22, \"ĐẠT ASHRAE & QCVN\", \"CHƯA ĐẠT\")")
    ]
    for r_idx, (sp_name, des_lpd, qcvn_lim, ash_lim, eval_f) in enumerate(lpd_rows, start=19):
        ws5.cell(row=r_idx, column=2, value=sp_name).font = font_regular
        ws5.cell(row=r_idx, column=3, value=des_lpd).number_format = "0.0"
        ws5.cell(row=r_idx, column=3).fill = fill_input
        ws5.cell(row=r_idx, column=4, value=qcvn_lim).number_format = "0.0"
        ws5.cell(row=r_idx, column=5, value=ash_lim).number_format = "0.0"
        c_eval = ws5.cell(row=r_idx, column=6, value=eval_f)
        c_eval.font = font_bold
        c_eval.fill = fill_pass
        c_eval.alignment = Alignment(horizontal="center")

    # =========================================================================
    # SHEET 6: KIỂM TOÁN NĂNG LƯỢNG ISO 50002 & LCCA (06_ISO50002_ENERGY_AUDIT)
    # =========================================================================
    ws6 = wb.create_sheet(title="06_ISO50002_ENERGY_AUDIT")
    ws6.views.sheetView[0].showGridLines = True
    
    ws6.merge_cells("B2:I2")
    ws6["B2"] = "MODULE 6: KIỂM TOÁN NĂNG LƯỢNG (ISO 50002 / ASHRAE 211) & PHÂN TÍCH TÀI CHÍNH LCCA"
    ws6["B2"].font = font_title
    ws6["B2"].fill = fill_navy
    ws6["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws6.row_dimensions[2].height = 30

    # 6.1 Baseline
    ws6.cell(row=4, column=2, value="6.1 ĐƯỜNG CƠ SỞ NĂNG LƯỢNG & CHỈ SỐ ENPIs (ENERGY BASELINE & ENPIs)").font = font_bold
    audit_base_data = [
        ("Tổng điện năng tiêu thụ 12 tháng qua:", 3250000, "kWh/năm"),
        ("Tổng diện tích sàn điều hòa không khí:", 22000, "m2"),
        ("Chỉ số cường độ năng lượng EUI:", "=C5/C6", "kWh/m2.năm"),
        ("Hạn mức chuẩn Văn phòng Thương mại:", "120 - 150", "kWh/m2.năm (Hạng A)"),
        ("Đánh giá hiện trạng tiêu thụ:", "TIÊU THỤ TRUNG BÌNH - CÓ TIỀM NĂNG TIẾT KIỆM 15-20%", "Theo ISO 50002")
    ]
    for idx, (label, val, note) in enumerate(audit_base_data, start=5):
        ws6.cell(row=idx, column=2, value=label).font = font_regular
        c = ws6.cell(row=idx, column=3, value=val)
        c.font = font_bold
        if isinstance(val, (int, float)):
            c.fill = fill_input
            c.number_format = "#,##0"
        elif str(val).startswith("="):
            c.fill = fill_calc
            c.number_format = "#,##0.1"
        ws6.cell(row=idx, column=4, value=note).font = font_small

    # 6.2 Nhật ký đo thực địa
    ws6.cell(row=12, column=2, value="6.2 SỐ LIỆU ĐO ĐẠC THỰC ĐỊA TẠI CỤM CHILLER (FIELD LOGGING & DIAGNOSTICS)").font = font_bold
    log_headers = [
        "Thời điểm đo", "Lưu lượng ChW (m3/h)", "T_vào Chiller (°C)", "T_ra Chiller (°C)", 
        "Delta T (°C)", "Công suất lạnh (RT)", "Điện Chiller (kW)", "Hiệu suất (kW/RT)", "Chẩn đoán vận hành"
    ]
    for c_idx, h in enumerate(log_headers, start=2):
        c = ws6.cell(row=13, column=c_idx, value=h)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    sample_logs = [
        ("09:00 Sáng", 280.0, 11.2, 7.0, "=D14-E14", "=(C14*F14*4.186)/(3.6*3.51685)", 182.0, "=H14/G14", "Delta T tốt, tải 65%"),
        ("12:00 Trưa", 320.0, 12.4, 7.0, "=D15-E15", "=(C15*F15*4.186)/(3.6*3.51685)", 245.0, "=H15/G15", "Đỉnh tải trưa, Chiller chạy tối ưu"),
        ("15:00 Chiều", 310.0, 12.0, 7.0, "=D16-E16", "=(C16*F16*4.186)/(3.6*3.51685)", 230.0, "=H16/G16", "Tải cao ổn định"),
        ("19:00 Tối", 250.0, 9.8, 7.0, "=D17-E17", "=(C17*F17*4.186)/(3.6*3.51685)", 135.0, "=H17/G17", "CẢNH BÁO: Delta T thấp (2.8°C)")
    ]
    for r_idx, (t_stamp, flow, tin, tout, dt_f, rt_f, kw, eff_f, diag) in enumerate(sample_logs, start=14):
        ws6.cell(row=r_idx, column=2, value=t_stamp).font = font_regular
        ws6.cell(row=r_idx, column=3, value=flow).number_format = "#,##0.0"
        ws6.cell(row=r_idx, column=4, value=tin).number_format = "0.0"
        ws6.cell(row=r_idx, column=5, value=tout).number_format = "0.0"
        
        c_dt = ws6.cell(row=r_idx, column=6, value=dt_f)
        c_dt.number_format = "0.0"
        c_dt.fill = fill_calc
        
        c_rt = ws6.cell(row=r_idx, column=7, value=rt_f)
        c_rt.number_format = "#,##0.1"
        c_rt.fill = fill_calc
        
        ws6.cell(row=r_idx, column=8, value=kw).number_format = "#,##0.0"
        
        c_eff = ws6.cell(row=r_idx, column=9, value=eff_f)
        c_eff.number_format = "0.000"
        c_eff.font = font_bold
        c_eff.fill = fill_calc
        
        c_diag = ws6.cell(row=r_idx, column=10, value=diag)
        c_diag.font = font_small
        if "CẢNH BÁO" in diag:
            c_diag.fill = fill_warn

    # 6.3 Danh mục giải pháp ECM & LCCA
    ws6.cell(row=20, column=2, value="6.3 DANH MỤC GIẢI PHÁP TIẾT KIỆM NĂNG LƯỢNG (ECMs) & HIỆU QUẢ TÀI CHÍNH (LCCA)").font = font_bold
    ecm_headers = [
        "Mã ECM", "Mô tả giải pháp kỹ thuật", "Chi phí đầu tư CAPEX (VNĐ)", "Tiết kiệm điện (kWh/năm)", 
        "Tiền điện tiết kiệm (VNĐ/năm)", "Hoàn vốn giản đơn (Năm)", "NPV 15 năm (VNĐ)", "IRR (%)"
    ]
    for c_idx, h in enumerate(ecm_headers, start=2):
        c = ws6.cell(row=21, column=c_idx, value=h)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    ecm_list = [
        ("ECM-01", "Lắp biến tần VFD cho cụm Bơm nước giải nhiệt & Tháp", 180000000, 115000, "=D22*2300", "=C22/E22", 1540000000, 0.95),
        ("ECM-02", "Cân bằng động van PICV chống hội chứng Low Delta-T", 250000000, 98000, "=D23*2300", "=C23/E23", 1280000000, 0.72),
        ("ECM-03", "Cài đặt thuật toán ChW Reset và Wet-Bulb Approach BMS", 60000000, 85000, "=D24*2300", "=C24/E24", 1320000000, 2.10),
        ("ECM-04", "Lắp hệ thống bóng vệ sinh tự động bình ngưng Chiller", 320000000, 140000, "=D25*2300", "=C25/E25", 1950000000, 0.82),
    ]
    for r_idx, (code, desc, capex, kwh, sav_f, pb_f, npv, irr) in enumerate(ecm_list, start=22):
        ws6.cell(row=r_idx, column=2, value=code).font = font_bold
        ws6.cell(row=r_idx, column=3, value=desc).font = font_regular
        ws6.cell(row=r_idx, column=4, value=capex).number_format = "#,##0"
        ws6.cell(row=r_idx, column=5, value=kwh).number_format = "#,##0"
        
        c_sav = ws6.cell(row=r_idx, column=6, value=sav_f)
        c_sav.font = font_bold
        c_sav.number_format = "#,##0"
        c_sav.fill = fill_calc
        
        c_pb = ws6.cell(row=r_idx, column=7, value=pb_f)
        c_pb.font = font_bold
        c_pb.number_format = "0.0"
        c_pb.fill = fill_pass
        
        ws6.cell(row=r_idx, column=8, value=npv).number_format = "#,##0"
        c_irr = ws6.cell(row=r_idx, column=9, value=irr)
        c_irr.number_format = "0.0%"

    # Hàng tổng ECM
    ws6.cell(row=26, column=2, value="TỔNG TIỀM NĂNG CÁC GIẢI PHÁP ECM:").font = font_bold
    ws6.cell(row=26, column=4, value="=SUM(D22:D25)").font = font_bold
    ws6.cell(row=26, column=4).number_format = "#,##0"
    
    ws6.cell(row=26, column=5, value="=SUM(E22:E25)").font = font_bold
    ws6.cell(row=26, column=5).number_format = "#,##0"
    
    ws6.cell(row=26, column=6, value="=SUM(F22:F25)").font = font_bold
    ws6.cell(row=26, column=6).number_format = "#,##0"
    ws6.cell(row=26, column=6).fill = fill_pass
    
    ws6.cell(row=26, column=7, value="=D26/F26").font = font_bold
    ws6.cell(row=26, column=7).number_format = "0.0"
    ws6.cell(row=26, column=7).fill = fill_pass

    # =========================================================================
    # SHEET 7: COMMISSIONING (TAB) & CHẨN ĐOÁN LỖI FDD (07_CX_TAB_FDD)
    # =========================================================================
    ws7 = wb.create_sheet(title="07_CX_TAB_FDD")
    ws7.views.sheetView[0].showGridLines = True
    
    ws7.merge_cells("B2:H2")
    ws7["B2"] = "MODULE 7: NGHIỆM THU VẬN HÀNH (COMMISSIONING - TAB) & CHẨN ĐOÁN LỖI TỰ ĐỘNG (FDD)"
    ws7["B2"].font = font_title
    ws7["B2"].fill = fill_navy
    ws7["B2"].alignment = Alignment(horizontal="center", vertical="center")
    ws7.row_dimensions[2].height = 30

    # 7.1 TAB
    ws7.cell(row=4, column=2, value="7.1 BẢNG NGHIỆM THU CÂN BẰNG KHÍ ĐỘNG MẠNG ỐNG GIÓ (TAB PROTOCOL - NEBB/ASHRAE)").font = font_bold
    tab_headers = [
        "Vị trí miệng gió / Terminal", "Lưu lượng thiết kế (m3/h)", "Lưu lượng đo đạc (m3/h)", 
        "Tỷ lệ thực tế / Thiết kế", "Sai lệch (%)", "Dung sai cho phép", "Kết luận nghiệm thu"
    ]
    for c_idx, h in enumerate(tab_headers, start=2):
        c = ws7.cell(row=5, column=c_idx, value=h)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    sample_tab = [
        ("Miệng gió cấp SA-01 (P. Giám đốc)", 450, 470, "=D6/C6", "=(E6-1)*100", "+- 10%", "=IF(ABS(F6)<=10, \"ĐẠT (PASS)\", \"CHỈNH LẠI\")"),
        ("Miệng gió cấp SA-02 (P. Họp 1)", 800, 760, "=D7/C7", "=(E7-1)*100", "+- 10%", "=IF(ABS(F7)<=10, \"ĐẠT (PASS)\", \"CHỈNH LẠI\")"),
        ("Miệng gió cấp SA-03 (Khu mở A)", 600, 580, "=D8/C8", "=(E8-1)*100", "+- 10%", "=IF(ABS(F8)<=10, \"ĐẠT (PASS)\", \"CHỈNH LẠI\")"),
        ("Miệng gió cấp SA-04 (Khu mở B)", 600, 630, "=D9/C9", "=(E9-1)*100", "+- 10%", "=IF(ABS(F9)<=10, \"ĐẠT (PASS)\", \"CHỈNH LẠI\")"),
        ("Miệng gió cấp SA-05 (Cuối tuyến)", 350, 310, "=D10/C10", "=(E10-1)*100", "+- 10%", "=IF(ABS(F10)<=10, \"ĐẠT (PASS)\", \"CHỈNH LẠI\")")
    ]
    for r_idx, (t_name, d_flow, m_flow, rat_f, dev_f, tol, eval_f) in enumerate(sample_tab, start=6):
        ws7.cell(row=r_idx, column=2, value=t_name).font = font_regular
        ws7.cell(row=r_idx, column=3, value=d_flow).number_format = "#,##0"
        ws7.cell(row=r_idx, column=4, value=m_flow).number_format = "#,##0"
        
        c_rat = ws7.cell(row=r_idx, column=5, value=rat_f)
        c_rat.number_format = "0.00"
        c_rat.fill = fill_calc
        
        c_dev = ws7.cell(row=r_idx, column=6, value=dev_f)
        c_dev.number_format = "0.0"
        c_dev.fill = fill_calc
        
        ws7.cell(row=r_idx, column=7, value=tol).alignment = Alignment(horizontal="center")
        
        c_eval = ws7.cell(row=r_idx, column=8, value=eval_f)
        c_eval.font = font_bold
        c_eval.fill = fill_pass
        c_eval.alignment = Alignment(horizontal="center")

    # 7.2 FDD Rules
    ws7.cell(row=13, column=2, value="7.2 HỆ THỐNG QUY TẮC CHẨN ĐOÁN LỖI VẬN HÀNH TỰ ĐỘNG (FDD EXPERT RULES)").font = font_bold
    fdd_headers = ["Mã quy tắc", "Hệ thống mục tiêu", "Điều kiện kích hoạt lỗi (BMS Trigger)", "Chẩn đoán nguyên nhân vật lý", "Hành động khắc phục kỹ thuật"]
    for c_idx, h in enumerate(fdd_headers, start=2):
        c = ws7.cell(row=14, column=c_idx, value=h)
        c.font = font_bold
        c.fill = fill_steel
        c.alignment = Alignment(horizontal="center")

    fdd_rules = [
        ("FDD-R01", "Trạm Chiller", "Approach bình ngưng tăng > 1.5°C so với ban đầu", "Đóng cáu cặn bề mặt ống đồng bình ngưng, xử lý nước kém", "Tẩy rửa cơ học ống chùm bình ngưng hoặc lắp hệ thống bóng tự động"),
        ("FDD-R02", "Mạng nước ChW", "Delta T hồi - cấp < 3.0°C khi tải làm lạnh > 60%", "Van bypass bị kẹt mở, hoặc cuộn coil AHU bị bám bẩn gây tràn lưu lượng", "Cân bằng lại mạng thủy lực, kiểm tra đóng kín van 2 ngả bypass"),
        ("FDD-R03", "AHU / VAV", "Van nước lạnh mở > 20% đồng thời van sưởi mở > 10%", "Xung đột cài đặt dải chết (Deadband) điều khiển tại DDC/BMS", "Cài đặt lại Deadband tối thiểu 1.5°C giữa chế độ làm mát và sưởi ấm"),
        ("FDD-R04", "Hệ Tháp giải nhiệt", "Nhiệt độ nước vào bình ngưng cao hơn bầu ướt > 4.5°C", "Tấm tản nhiệt tháp bám rong rêu hoặc quạt tháp chạy ngược pha", "Vệ sinh khối đệm tản nhiệt (Fill packs) và kiểm tra chiều quay quạt")
    ]
    for r_idx, (r_code, sys_name, trig, diag, act) in enumerate(fdd_rules, start=15):
        ws7.cell(row=r_idx, column=2, value=r_code).font = font_bold
        ws7.cell(row=r_idx, column=3, value=sys_name).font = font_regular
        ws7.cell(row=r_idx, column=4, value=trig).font = font_regular
        ws7.cell(row=r_idx, column=5, value=diag).font = font_regular
        ws7.cell(row=r_idx, column=6, value=act).font = font_small

    # Tự động điều chỉnh độ rộng cột cho tất cả các sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            if col[0].column == 1:
                ws.column_dimensions[col_letter].width = 4
                continue
            for cell in col:
                val_str = str(cell.value or '')
                if cell.row == 2:  # Bỏ qua dòng title dài
                    continue
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

    output_path = r"\\192.168.1.252\10. pm_cm_qs\04. Energy\06 Tool _Calculator\02.MEP_Energy_Master_Suite\MEP_Energy_Auditor_Master_Toolkit.xlsx"
    wb.save(output_path)
    print(f"XUẤT WORKBOOK THÀNH CÔNG: {output_path}")

if __name__ == "__main__":
    build_workbook()
