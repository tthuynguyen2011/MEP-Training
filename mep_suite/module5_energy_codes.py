"""
Module 5: Tiêu chuẩn Hiệu quả Năng lượng Công trình (ASHRAE 90.1 & QCVN 09:2017/BXD)
Tham chiếu:
- QCVN 09:2017/BXD (Quy chuẩn Kỹ thuật Quốc gia về Các công trình xây dựng sử dụng năng lượng hiệu quả)
- ASHRAE Standard 90.1 (Energy Standard for Buildings Except Low-Rise Residential Buildings)
- Tiêu chí đánh giá Công trình Xanh LOTUS & LEED v4/v4.1
"""

import math
from typing import Dict, List, Tuple, Optional


class EnergyCodeCompliance:
    """
    Bộ kiểm tra và xác nhận tuân thủ Quy chuẩn Năng lượng (Code Compliance Validator):
    1. Vỏ bao che: Chỉ số truyền nhiệt tổng OTTV (Overall Thermal Transfer Value) & Tỷ lệ kính WWR
    2. Chiếu sáng: Mật độ công suất chiếu sáng LPD (Lighting Power Density - W/m2)
    3. Điều hòa không khí: Giới hạn hiệu suất tối thiểu COP / kW/RT theo QCVN 09 & ASHRAE 90.1
    """

    # Bảng LPD tối đa theo QCVN 09:2017/BXD và ASHRAE 90.1-2022 (Building Area Method)
    LPD_LIMITS_W_M2 = {
        "office": {"qcvn09": 9.0, "ashrae901_2022": 6.5, "name": "Văn phòng làm việc"},
        "hotel": {"qcvn09": 8.0, "ashrae901_2022": 6.0, "name": "Khách sạn"},
        "hospital": {"qcvn09": 11.0, "ashrae901_2022": 9.5, "name": "Bệnh viện"},
        "retail": {"qcvn09": 14.0, "ashrae901_2022": 9.8, "name": "Trung tâm thương mại"},
        "school": {"qcvn09": 8.0, "ashrae901_2022": 6.8, "name": "Trường học"},
        "warehouse": {"qcvn09": 5.0, "ashrae901_2022": 3.8, "name": "Nhà kho"}
    }

    @staticmethod
    def calculate_ottv_wall(gross_wall_area_m2: float, window_area_m2: float,
                            u_wall: float, u_window: float,
                            shgc_window: float,
                            orientation_factor: float = 1.0) -> Dict[str, any]:
        """
        Tính toán chỉ số OTTV (Overall Thermal Transfer Value) tường ngoài theo QCVN 09:2017/BXD:
        - Tỷ lệ cửa sổ trên tường WWR = Window_Area / Gross_Wall_Area
        - Công thức: OTTV = (Aw*Uw*TDeq + Af*Uf*dT + Af*SHGC*SF) / Atot
        - Giới hạn quy chuẩn QCVN 09: OTTV_wall <= 60.0 W/m2
        """
        opaque_wall_area = gross_wall_area_m2 - window_area_m2
        wwr = window_area_m2 / max(gross_wall_area_m2, 1.0)
        
        # Hệ số nhiệt độ tương đương chuẩn tại Việt Nam
        td_eq = 12.0  # Chênh lệch nhiệt độ tương đương tường đục (°C)
        delta_t_glass = 5.0  # Chênh lệch nhiệt độ truyền nhiệt qua kính (°C)
        solar_factor_sf = 130.0 * orientation_factor  # W/m2 (trung bình các hướng tại vĩ độ VN)
        
        q_wall_cond = (opaque_wall_area * u_wall * td_eq)
        q_glass_cond = (window_area_m2 * u_window * delta_t_glass)
        q_glass_solar = (window_area_m2 * shgc_window * solar_factor_sf)
        
        ottv = (q_wall_cond + q_glass_cond + q_glass_solar) / max(gross_wall_area_m2, 1.0)
        limit_qcvn09 = 60.0  # W/m2
        passed = ottv <= limit_qcvn09
        
        return {
            "gross_wall_area_m2": gross_wall_area_m2,
            "window_area_m2": window_area_m2,
            "wwr": round(wwr, 3),
            "ottv_w_m2": round(ottv, 2),
            "limit_qcvn09_w_m2": limit_qcvn09,
            "is_compliant": passed,
            "wall_conduction_part": round(q_wall_cond / gross_wall_area_m2, 2),
            "glass_conduction_part": round(q_glass_cond / gross_wall_area_m2, 2),
            "glass_solar_part": round(q_glass_solar / gross_wall_area_m2, 2)
        }

    @classmethod
    def check_lighting_compliance(cls, building_type: str, actual_lpd_w_m2: float) -> Dict[str, any]:
        """
        Kiểm tra tuân thủ Mật độ công suất chiếu sáng LPD:
        So sánh với QCVN 09:2017/BXD và ASHRAE Standard 90.1-2022.
        """
        limits = cls.LPD_LIMITS_W_M2.get(building_type.lower(), cls.LPD_LIMITS_W_M2["office"])
        qcvn_ok = actual_lpd_w_m2 <= limits["qcvn09"]
        ashrae_ok = actual_lpd_w_m2 <= limits["ashrae901_2022"]
        
        return {
            "building_type": limits["name"],
            "actual_lpd_w_m2": actual_lpd_w_m2,
            "limit_qcvn09": limits["qcvn09"],
            "compliant_qcvn09": qcvn_ok,
            "limit_ashrae901_2022": limits["ashrae901_2022"],
            "compliant_ashrae901": ashrae_ok
        }

    @staticmethod
    def check_chiller_efficiency_compliance(chiller_type: str, capacity_rt: float,
                                           cop_full_load: float, iplv_cop: float) -> Dict[str, any]:
        """
        Kiểm tra hiệu suất tối thiểu của Chiller theo QCVN 09:2017 và ASHRAE 90.1-2022 (Path A/B):
        - Chiller giải nhiệt nước trục vít / ly tâm
        - Chiller giải nhiệt gió
        """
        kw_per_rt = 3.51685 / max(cop_full_load, 0.01)
        iplv_kw_per_rt = 3.51685 / max(iplv_cop, 0.01)
        
        if "water" in chiller_type.lower():
            if capacity_rt >= 300:
                # Chiller ly tâm nước >= 300 RT
                min_cop_qcvn = 5.70  # kW/RT <= 0.617
                min_cop_ashrae = 6.40  # kW/RT <= 0.550
                min_iplv_ashrae = 8.50  # kW/RT <= 0.414
            else:
                # Chiller trục vít nước < 300 RT
                min_cop_qcvn = 5.00  # kW/RT <= 0.703
                min_cop_ashrae = 5.50  # kW/RT <= 0.639
                min_iplv_ashrae = 7.00  # kW/RT <= 0.502
        else:
            # Chiller giải nhiệt gió (Air-cooled)
            min_cop_qcvn = 2.80  # kW/RT <= 1.256
            min_cop_ashrae = 3.10  # kW/RT <= 1.134
            min_iplv_ashrae = 4.20  # kW/RT <= 0.837
            
        return {
            "chiller_type": chiller_type,
            "capacity_rt": capacity_rt,
            "actual_cop": round(cop_full_load, 2),
            "actual_kw_per_rt": round(kw_per_rt, 3),
            "actual_iplv_cop": round(iplv_cop, 2),
            "actual_iplv_kw_per_rt": round(iplv_kw_per_rt, 3),
            "qcvn09_min_cop": min_cop_qcvn,
            "qcvn09_compliant": cop_full_load >= min_cop_qcvn,
            "ashrae901_min_cop": min_cop_ashrae,
            "ashrae901_cop_compliant": cop_full_load >= min_cop_ashrae,
            "ashrae901_min_iplv": min_iplv_ashrae,
            "ashrae901_iplv_compliant": iplv_cop >= min_iplv_ashrae
        }
