"""
Module 6: Kiểm toán Năng lượng theo ISO 50002 & Đo kiểm M&V theo ASHRAE 211 / IPMVP
Tham chiếu:
- TCVN ISO 50002:2015 / ISO 50002 (Kiểm toán năng lượng - Yêu cầu và hướng dẫn sử dụng)
- TCVN ISO 50001:2019 (Hệ thống quản lý năng lượng - EnMS)
- ASHRAE Standard 211 (Standard for Commercial Building Energy Audits)
- ASHRAE Guideline 14 (Measurement of Energy, Demand, and Water Savings)
- IPMVP (International Performance Measurement and Verification Protocol)
"""

import math
from typing import Dict, List, Tuple, Optional


class EnergyAuditISO50002:
    """
    Bộ công cụ thực hành Kiểm toán Năng lượng theo chuẩn ISO 50002:
    1. Thiết lập Đường cơ sở năng lượng (Energy Baseline - EnB) & Chỉ số EnPIs (EUI, SEC)
    2. Xử lý số liệu đo đạc thực địa (Field Logging: Chiller, Bơm, Quạt, Biến áp)
    3. Chẩn đoán các căn bệnh kinh điển: Hội chứng chênh nhiệt độ thấp (Low Delta-T), cáu cặn bình ngưng
    4. Thư viện tính toán giải pháp Tiết kiệm Năng lượng (Energy Conservation Measures - ECMs)
    """

    @staticmethod
    def calculate_eui(annual_kwh: float, gross_floor_area_m2: float) -> Dict[str, float]:
        """
        Tính toán Chỉ số cường độ sử dụng năng lượng EUI (Energy Use Intensity - kWh/m2.năm)
        Chuẩn đánh giá:
        - Văn phòng VN: 110 - 150 kWh/m2.năm (Tốt), > 200 kWh/m2.năm (Tiêu hao cao)
        - Khách sạn 4-5 sao: 180 - 250 kWh/m2.năm (Tốt), > 320 kWh/m2.năm (Tiêu hao cao)
        - TTTM: 220 - 300 kWh/m2.năm
        """
        eui = annual_kwh / max(gross_floor_area_m2, 1.0)
        return {
            "annual_kwh": annual_kwh,
            "gross_floor_area_m2": gross_floor_area_m2,
            "eui_kwh_per_m2_year": round(eui, 1)
        }

    @staticmethod
    def linear_baseline_regression(months_x_cdd: List[float], months_y_kwh: List[float]) -> Dict[str, float]:
        """
        Xây dựng hàm hồi quy tuyến tính đường cơ sở năng lượng (Energy Baseline EnB):
        Y (kWh) = a + b * X (CDD - Cooling Degree Days)
        Kiểm tra độ chính xác mô hình theo ASHRAE Guideline 14: Hệ số tương quan R2 >= 0.75
        """
        n = len(months_x_cdd)
        if n < 6 or n != len(months_y_kwh):
            raise ValueError("Cần ít nhất 6 tháng số liệu để xây dựng Baseline")
            
        sum_x = sum(months_x_cdd)
        sum_y = sum(months_y_kwh)
        sum_xx = sum(x * x for x in months_x_cdd)
        sum_yy = sum(y * y for y in months_y_kwh)
        sum_xy = sum(x * y for x, y in zip(months_x_cdd, months_y_kwh))
        
        denom = (n * sum_xx - sum_x * sum_x)
        if abs(denom) < 1e-9:
            return {"slope_b": 0.0, "intercept_a": sum_y / n, "r_squared": 0.0}
            
        slope_b = (n * sum_xy - sum_x * sum_y) / denom
        intercept_a = (sum_y - slope_b * sum_x) / n
        
        # Hệ số xác định R^2
        ss_tot = sum((y - (sum_y / n)) ** 2 for y in months_y_kwh)
        ss_res = sum((y - (intercept_a + slope_b * x)) ** 2 for x, y in zip(months_x_cdd, months_y_kwh))
        r2 = 1.0 - (ss_res / max(ss_tot, 1e-6))
        
        return {
            "intercept_base_load_kwh": round(intercept_a, 1),
            "slope_weather_sensitivity": round(slope_b, 2),
            "r_squared": round(r2, 3),
            "ashrae14_compliant": r2 >= 0.75
        }

    @staticmethod
    def analyze_field_chiller_logging(chw_flow_m3_h: float,
                                      chw_temp_in_c: float,
                                      chw_temp_out_c: float,
                                      chiller_active_power_kw: float,
                                      design_delta_t: float = 5.5) -> Dict[str, any]:
        """
        Phân tích số liệu đo đạc thực tế tại hiện trường (Field Measurement):
        - Đo lưu lượng nước lạnh bằng đồng hồ siêu âm (m3/h)
        - Đo nhiệt độ nước vào/ra bằng cảm biến chính xác Pt100
        - Đo công suất điện Chiller bằng Power Quality Analyzer (kW)
        Tính:
        - Tải lạnh thực tế (Operating Cooling Capacity - RT & kW)
        - Hiệu suất vận hành tức thời (Operating kW/RT & COP)
        - Chẩn đoán hội chứng Low Delta-T (chênh lệch nhiệt độ thấp)
        """
        delta_t_measured = chw_temp_in_c - chw_temp_out_c
        
        # Tải lạnh thực tế: Q = m_dot * Cp * delta_T
        # Q_kw = (m3/h / 3600) * 1000 kg/m3 * 4.186 kJ/kg.K * delta_T = (m3/h * delta_T * 4.186) / 3.6
        cooling_actual_kw = (chw_flow_m3_h * delta_t_measured * 4.186) / 3.6
        cooling_actual_rt = cooling_actual_kw / 3.51685
        
        operating_kw_per_rt = chiller_active_power_kw / max(cooling_actual_rt, 0.1)
        operating_cop = 3.51685 / max(operating_kw_per_rt, 0.01)
        
        # Chẩn đoán lỗi hội chứng Low Delta-T
        is_low_delta_t = delta_t_measured < (design_delta_t * 0.75)
        severity = "Bình thường"
        if delta_t_measured < 3.0:
            severity = "Nghiêm trọng (Lãng phí điện bơm rất lớn, Chiller bị non tải giả tạo)"
        elif is_low_delta_t:
            severity = "Cảnh báo (Delta-T suy giảm)"

        return {
            "measured_delta_t_c": round(delta_t_measured, 2),
            "cooling_actual_kw": round(cooling_actual_kw, 1),
            "cooling_actual_rt": round(cooling_actual_rt, 1),
            "chiller_power_kw": round(chiller_active_power_kw, 1),
            "operating_kw_per_rt": round(operating_kw_per_rt, 3),
            "operating_cop": round(operating_cop, 2),
            "is_low_delta_t_syndrome": is_low_delta_t,
            "diagnosis_severity": severity,
            "root_causes": [
                "Van bypass 3 ngả hoặc 2 ngả bị kẹt mở rò rỉ",
                "Dàn coil AHU bị bám bẩn hoặc lưu lượng qua dàn vượt mức thiết kế",
                "Van cân bằng tại các nhánh FCU chưa được cân bằng động (chưa lắp PICV)"
            ] if is_low_delta_t else ["Hệ thống tuần hoàn nước lạnh hoạt động trao đổi nhiệt tốt."]
        }

    @staticmethod
    def ecm_vfd_pump_savings(current_pump_kw: float,
                             operating_hours_year: float,
                             avg_flow_fraction: float = 0.70,
                             electricity_cost_vnd_kwh: float = 2300.0) -> Dict[str, float]:
        """
        Tính toán giải pháp ECM: Lắp biến tần VFD cho Bơm nước lạnh thứ cấp hoặc Bơm giải nhiệt:
        Theo định luật đồng dạng bơm (Affinity Laws): P2 / P1 = (Q2 / Q1)^3
        Ở lưu lượng trung bình 70%, công suất lý thuyết chỉ còn (0.7)^3 = 34.3% công suất định mức!
        """
        # Do có tổn thất biến tần và cột áp tĩnh tối thiểu, hệ số thực nghiệm công suất P2/P1 ~ (Q2/Q1)^2.4
        power_fraction = avg_flow_fraction ** 2.4
        new_avg_pump_kw = current_pump_kw * power_fraction
        
        baseline_kwh = current_pump_kw * operating_hours_year
        post_ecm_kwh = new_avg_pump_kw * operating_hours_year
        savings_kwh = baseline_kwh - post_ecm_kwh
        savings_vnd = savings_kwh * electricity_cost_vnd_kwh
        
        return {
            "baseline_pump_kw": current_pump_kw,
            "vfd_avg_pump_kw": round(new_avg_pump_kw, 1),
            "annual_baseline_kwh": round(baseline_kwh, 0),
            "annual_post_ecm_kwh": round(post_ecm_kwh, 0),
            "annual_savings_kwh": round(savings_kwh, 0),
            "annual_savings_vnd": round(savings_vnd, 0),
            "energy_saving_percent": round((1.0 - power_fraction) * 100.0, 1)
        }


class FinancialAnalysisLCCA:
    """
    Phân tích Tài chính Hiệu quả Đầu tư Năng lượng (Life Cycle Cost Analysis - LCCA):
    - Thời gian hoàn vốn giản đơn (Simple Payback Period - SPB)
    - Hiện giá thuần (Net Present Value - NPV)
    - Tỷ suất sinh lời nội hàm (Internal Rate of Return - IRR)
    - Tỷ số Lợi ích / Chi phí đầu tư (Savings-to-Investment Ratio - SIR)
    """

    @staticmethod
    def evaluate_investment(capex_vnd: float,
                            annual_savings_vnd: float,
                            annual_maintenance_delta_vnd: float = 0.0,
                            lifetime_years: int = 15,
                            discount_rate: float = 0.08) -> Dict[str, float]:
        """
        Đánh giá tính khả thi tài chính của Giải pháp Tiết kiệm Năng lượng (ECM):
        - capex_vnd: Chi phí đầu tư ban đầu
        - annual_savings_vnd: Tiết kiệm tiền điện hàng năm
        - discount_rate: Tỷ suất chiết khấu (WACC, thông thường 8% - 10%/năm)
        - lifetime_years: Tuổi thọ giải pháp thiết bị (thường 10-15 năm)
        """
        net_annual_cash_flow = annual_savings_vnd - annual_maintenance_delta_vnd
        simple_payback_years = capex_vnd / max(net_annual_cash_flow, 1.0)
        
        # Tính NPV = -CAPEX + sum(CF / (1+r)^t)
        npv = -capex_vnd
        for t in range(1, lifetime_years + 1):
            npv += net_annual_cash_flow / ((1.0 + discount_rate) ** t)
            
        # Tính IRR bằng phương pháp lặp xấp xỉ Newton hoặc bisection
        irr = 0.0
        low = -0.5
        high = 2.0
        for _ in range(50):
            mid = (low + high) / 2.0
            npv_mid = -capex_vnd + sum(net_annual_cash_flow / ((1.0 + mid) ** t) for t in range(1, lifetime_years + 1))
            if abs(npv_mid) < 1.0:
                irr = mid
                break
            if npv_mid > 0:
                low = mid
            else:
                high = mid
        irr = (low + high) / 2.0
        
        sir = (npv + capex_vnd) / max(capex_vnd, 1.0)
        
        return {
            "capex_vnd": capex_vnd,
            "net_annual_savings_vnd": round(net_annual_cash_flow, 0),
            "simple_payback_years": round(simple_payback_years, 2),
            "npv_vnd": round(npv, 0),
            "irr_percent": round(irr * 100.0, 2),
            "sir_ratio": round(sir, 2),
            "is_financially_viable": (npv > 0 and simple_payback_years <= 5.0)
        }
