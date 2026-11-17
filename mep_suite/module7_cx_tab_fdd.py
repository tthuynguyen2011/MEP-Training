"""
Module 7: Nghiệm thu Vận hành (Commissioning - Cx), Thử nghiệm Cân bằng (TAB) & Chẩn đoán Lỗi (FDD)
Tham chiếu:
- ASHRAE Guideline 0 & Guideline 1.1 (The HVAC&R Commissioning Process)
- NEBB Procedural Standards for Testing Adjusting and Balancing of Environmental Systems
- ASHRAE Guideline 14 & NIST Automated Fault Detection and Diagnostics (FDD)
"""

import math
from typing import Dict, List, Tuple, Optional


class CommissioningTAB:
    """
    Bộ công cụ Cân bằng Thủy lực & Khí động (Testing, Adjusting, Balancing - TAB):
    - Phương pháp Cân bằng Tỷ lệ (Proportional Balancing Method):
      Tính toán tỷ lệ lưu lượng thực tế so với thiết kế (Flow Ratio = Actual / Design)
      Xác định nhánh chỉ số (Index Terminal - nhánh có tỷ số lưu lượng nhỏ nhất)
      Cân bằng từng bước đưa toàn bộ hệ thống về sai số cho phép +-10% theo NEBB / ASHRAE.
    """

    @staticmethod
    def evaluate_flow_deviations(design_flows: List[float], measured_flows: List[float]) -> Dict[str, any]:
        """
        Đánh giá độ sai lệch lưu lượng mạng gió hoặc nước trước và sau cân bằng:
        Tiêu chuẩn nghiệm thu NEBB: 90% <= Flow_actual / Flow_design <= 110%
        """
        if len(design_flows) != len(measured_flows):
            raise ValueError("Số lượng nhánh thiết kế và đo đạc phải bằng nhau")
            
        ratios = []
        deviations_pct = []
        in_tolerance_flags = []
        
        for d, m in zip(design_flows, measured_flows):
            ratio = m / max(d, 0.001)
            dev_pct = (ratio - 1.0) * 100.0
            ratios.append(round(ratio, 3))
            deviations_pct.append(round(dev_pct, 1))
            in_tolerance_flags.append(abs(dev_pct) <= 10.0)
            
        index_branch = ratios.index(min(ratios))
        all_passed = all(in_tolerance_flags)
        
        return {
            "num_terminals": len(design_flows),
            "flow_ratios": ratios,
            "deviations_percent": deviations_pct,
            "index_terminal_index": index_branch + 1,  # 1-based
            "min_ratio": min(ratios),
            "max_ratio": max(ratios),
            "all_within_tolerance": all_passed,
            "status_summary": "ĐẠT TIÊU CHUẨN TAB (NEBB +-10%)" if all_passed else "CHƯA ĐẠT (Cần tiếp tục cân chỉnh van nhánh)"
        }

    @staticmethod
    def calculate_balancing_valve_setting(design_flow_m3_h: float, target_dp_kpa: float) -> float:
        """
        Tính toán hệ số lưu lượng yêu cầu của van cân bằng Kv (m3/h / bar^0.5):
        Q (m3/h) = Kv * sqrt(Delta_P_bar)
        Delta_P_bar = target_dp_kpa / 100.0
        """
        dp_bar = max(target_dp_kpa, 1.0) / 100.0
        kv = design_flow_m3_h / math.sqrt(dp_bar)
        return round(kv, 2)


class FaultDetectionDiagnostics:
    """
    Bộ Chẩn đoán & Phát hiện Bất thường Vận hành Tự động (Automated FDD):
    Dựa trên quy tắc chuyên gia (Rule-based FDD) cho Chiller Plant, AHU, VAV.
    """

    @staticmethod
    def diagnose_ahu_operation(supply_air_temp_c: float,
                               setpoint_temp_c: float,
                               cooling_valve_pos_pct: float,
                               heating_valve_pos_pct: float,
                               outdoor_air_temp_c: float,
                               mixed_air_temp_c: float) -> List[str]:
        """
        Chẩn đoán lỗi vận hành AHU dựa trên số liệu cảm biến BMS theo chu kỳ:
        - Lỗi 1: Xung đột làm lạnh và sưởi đồng thời (Simultaneous cooling & heating)
        - Lỗi 2: Không đạt nhiệt độ gió cấp dù van mở 100% (Under-cooling / Hunting)
        - Lỗi 3: Rò rỉ van gió tươi trong chế độ đóng (Damper leakage)
        """
        faults = []
        
        # Kiểm tra xung đột nhiệt: vừa mở lạnh vừa mở sưởi > 10%
        if cooling_valve_pos_pct > 10.0 and heating_valve_pos_pct > 10.0:
            faults.append(
                "LỖI NGHIÊM TRỌNG: Xung đột nhiệt! AHU đang đồng thời mở cả van nước lạnh ({}%) "
                "và van sưởi ({}%), gây lãng phí năng lượng khổng lồ.".format(
                    cooling_valve_pos_pct, heating_valve_pos_pct
                )
            )
            
        # Kiểm tra không đạt nhiệt độ gió cấp: Van lạnh mở 100% nhưng nhiệt độ cấp vẫn cao hơn setpoint > 2°C
        if cooling_valve_pos_pct >= 95.0 and (supply_air_temp_c - setpoint_temp_c) > 2.0:
            faults.append(
                "CẢNH BÁO HIỆU NĂNG: Không đạt nhiệt độ gió cấp (Thực tế: {}°C, Điểm đặt: {}°C) "
                "dù van lạnh đã mở tối đa 100%. Nguyên nhân: Nước lạnh không đủ lạnh, lưu lượng thiếu hoặc dàn bám bụi.".format(
                    supply_air_temp_c, setpoint_temp_c
                )
            )
            
        # Kiểm tra nhiệt độ hòa trộn bất thường
        if abs(mixed_air_temp_c - outdoor_air_temp_c) < 1.0 and cooling_valve_pos_pct > 50.0:
            faults.append(
                "CẢNH BÁO: Nhiệt độ hòa trộn xấp xỉ nhiệt độ ngoài trời ({}°C), "
                "nghi ngờ van gió hồi bị kẹt đóng hoặc van gió tươi mở quá mức thiết kế.".format(outdoor_air_temp_c)
            )
            
        if not faults:
            faults.append("Hệ thống AHU hoạt động bình thường, không ghi nhận xung đột vận hành.")
            
        return faults

    @staticmethod
    def diagnose_chiller_fouling(measured_approach_temp_c: float,
                                 baseline_approach_temp_c: float = 1.0) -> Dict[str, any]:
        """
        Chẩn đoán cáu cặn bình ngưng Chiller (Condenser Tube Fouling):
        Approach = Nhiệt độ gas lỏng ngưng tụ (Refrigerant Saturated Condensing Temp) - Nhiệt độ nước ra khỏi bình ngưng (Leaving Condenser Water Temp).
        Chuẩn sạch xuất xưởng: Approach <= 1.0°C.
        Nếu Approach tăng thêm 1.0°C -> Hiệu suất Chiller giảm ~ 2.5 - 3.5%!
        """
        delta_approach = measured_approach_temp_c - baseline_approach_temp_c
        is_fouled = delta_approach >= 1.5
        
        # Ước tính phần trăm điện năng tổn hao do cặn
        efficiency_penalty_pct = max(0.0, delta_approach * 3.0)
        
        return {
            "measured_approach_c": round(measured_approach_temp_c, 2),
            "baseline_approach_c": baseline_approach_temp_c,
            "approach_increase_c": round(delta_approach, 2),
            "estimated_efficiency_penalty_pct": round(efficiency_penalty_pct, 1),
            "status": "CẦN TẨY CẶN BÌNH NGƯNG (Tube Cleaning Required)" if is_fouled else "Bình ngưng sạch, trao đổi nhiệt tốt",
            "recommendation": "Vệ sinh cơ học hoặc sử dụng hệ thống bóng vệ sinh tự động (Online Tube Cleaning System) để khôi phục hiệu suất COP." if is_fouled else "Tiếp tục duy trì xử lý hóa chất chống ăn mòn và diệt rong rêu tháp giải nhiệt."
        }
