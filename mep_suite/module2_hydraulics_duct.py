"""
Module 2: Khí động lực học Đường ống gió & Thủy lực Đường ống nước (ASHRAE Systems & Equipment)
Tham chiếu:
- ASHRAE Handbook of Fundamentals (Ch. 21 Duct Design, Ch. 22 Pipe Sizing)
- TCVN 5687:2024 (Thông gió - Điều hòa không khí - Thiết kế mạng đường ống)
- ASHRAE HVAC Systems & Equipment (Pumps, Fans, Hydronic Distribution)
"""

import math
from typing import Dict, List, Tuple, Optional


class DuctSizer:
    """
    Bộ tính toán khí động học đường ống gió:
    - Kích thước tương đương Huebscher (Tròn sang Chữ nhật)
    - Phương pháp ma sát không đổi (Equal Friction) & Khống chế vận tốc âm học
    - Tính toán cột áp tĩnh ngoài của quạt (Fan External Static Pressure - ESP)
    """

    AIR_DENSITY = 1.204  # kg/m3 ở 20°C, 101.325 kPa
    AIR_VISCOSITY = 1.81e-5  # Pa.s (Kinematic ~ 1.5e-5 m2/s)

    @staticmethod
    def huebscher_circular_equivalent(width_mm: float, height_mm: float) -> float:
        """
        Đường kính ống tròn tương đương De (mm) cho ống chữ nhật kích thước a x b (mm)
        Công thức Huebscher (ASHRAE Fundamentals Ch. 21 Eq. 25):
        De = 1.30 * (a * b)^0.625 / (a + b)^0.25
        """
        a = max(width_mm, 10.0)
        b = max(height_mm, 10.0)
        return 1.30 * ((a * b) ** 0.625) / ((a + b) ** 0.25)

    @staticmethod
    def rectangular_dimensions_from_de(de_mm: float, aspect_ratio: float = 1.5) -> Tuple[int, int]:
        """
        Tìm kích thước ống chữ nhật rộng x cao (làm tròn lên bội số 50 mm)
        từ đường kính ống tròn De và tỷ lệ cạnh mong muốn (aspect ratio a/b).
        """
        # Xấp xỉ: a * b = (pi * de^2 / 4), với a = ar * b => b = sqrt(pi/4 / ar) * de
        b = math.sqrt((math.pi / 4.0) / aspect_ratio) * de_mm
        a = aspect_ratio * b
        
        # Làm tròn lên bội số 50 mm theo tiêu chuẩn chế tạo ống gió tôn mạ kẽm
        round_a = int(math.ceil(a / 50.0) * 50)
        round_b = int(math.ceil(b / 50.0) * 50)
        return max(150, round_a), max(150, round_b)

    def calculate_friction_loss(self, airflow_m3_h: float, de_mm: float, roughness_mm: float = 0.09) -> Dict[str, float]:
        """
        Tính tổn thất ma sát đơn vị dP/L (Pa/m) và vận tốc gió V (m/s)
        Sử dụng phương trình Darcy-Weisbach và Colebrook-White cho không khí trong ống tôn mạ kẽm.
        """
        q_m3_s = airflow_m3_h / 3600.0
        d_m = de_mm / 1000.0
        area_m2 = math.pi * (d_m ** 2) / 4.0
        velocity = q_m3_s / area_m2
        
        reynolds = (self.AIR_DENSITY * velocity * d_m) / self.AIR_VISCOSITY
        
        # Hệ số ma sát Darcy f theo Swamee-Jain (xấp xỉ nghiệm Colebrook-White)
        epsilon = (roughness_mm / 1000.0) / d_m
        if reynolds < 2300:
            f = 64.0 / max(reynolds, 1.0)
        else:
            f = 0.25 / (math.log10(epsilon / 3.7 + 5.74 / (reynolds ** 0.9)) ** 2)
            
        # Tổn thất áp suất ma sát dP/L = f * (rho / 2) * (V^2 / D) [Pa/m]
        dp_per_meter = f * (self.AIR_DENSITY / 2.0) * (velocity ** 2) / d_m
        velocity_pressure = 0.5 * self.AIR_DENSITY * (velocity ** 2)
        
        return {
            "velocity_m_s": round(velocity, 2),
            "reynolds": round(reynolds, 0),
            "friction_factor": round(f, 4),
            "dp_per_meter_pa": round(dp_per_meter, 2),
            "velocity_pressure_pa": round(velocity_pressure, 2)
        }

    def size_duct_by_equal_friction(self, airflow_m3_h: float,
                                    target_friction_pa_m: float = 1.0,
                                    max_velocity_m_s: float = 6.5,
                                    aspect_ratio: float = 1.5) -> Dict[str, any]:
        """
        Chọn kích thước ống gió tự động theo phương pháp Ma sát không đổi (thường 0.8 - 1.2 Pa/m)
        đồng thời khống chế vận tốc tối đa theo tiêu chuẩn độ ồn (tiêu chuẩn văn phòng: 5 - 7 m/s).
        """
        # Quét tìm đường kính De thỏa mãn target_friction
        de_test = 100.0
        step = 5.0
        while de_test < 2500.0:
            res = self.calculate_friction_loss(airflow_m3_h, de_test)
            if res["dp_per_meter_pa"] <= target_friction_pa_m and res["velocity_m_s"] <= max_velocity_m_s:
                break
            de_test += step
            
        w_mm, h_mm = self.rectangular_dimensions_from_de(de_test, aspect_ratio)
        actual_de = self.huebscher_circular_equivalent(w_mm, h_mm)
        actual_res = self.calculate_friction_loss(airflow_m3_h, actual_de)
        
        return {
            "airflow_m3_h": airflow_m3_h,
            "round_diameter_mm": int(math.ceil(de_test / 25.0) * 25),
            "rect_width_mm": w_mm,
            "rect_height_mm": h_mm,
            "actual_velocity_m_s": actual_res["velocity_m_s"],
            "actual_dp_pa_m": actual_res["dp_per_meter_pa"]
        }

    def calculate_fan_esp(self, duct_run_length_m: float, avg_dp_pa_m: float,
                          num_elbows: int, num_tees: int,
                          fire_damper_dp: float = 25.0,
                          vav_box_dp: float = 40.0,
                          diffuser_dp: float = 30.0,
                          filter_dp: float = 120.0,
                          coil_air_dp: float = 95.0,
                          safety_margin: float = 1.15) -> Dict[str, float]:
        """
        Tính toán tổng trở lực cột áp ngoài của quạt (External Static Pressure - ESP)
        Cộng dồn: Trở lực ma sát ống + Trở lực phụ kiện + Trở lực thiết bị (Lọc, Dàn coil, Van dập lửa, VAV, Miệng gió)
        """
        # Tổn thất cục bộ Co x V^2/2 x rho, trung bình mỗi cút 90° co tròn/cánh hướng ~ 15-20 Pa, tê ~ 25 Pa
        local_fittings_dp = (num_elbows * 18.0) + (num_tees * 25.0)
        straight_duct_dp = duct_run_length_m * avg_dp_pa_m
        
        terminal_equipment_dp = fire_damper_dp + vav_box_dp + diffuser_dp
        ahu_internal_dp = filter_dp + coil_air_dp
        
        net_esp = (straight_duct_dp + local_fittings_dp + terminal_equipment_dp)
        total_fan_sp = (net_esp + ahu_internal_dp) * safety_margin
        
        return {
            "straight_duct_dp_pa": round(straight_duct_dp, 1),
            "fittings_dp_pa": round(local_fittings_dp, 1),
            "terminals_dp_pa": round(terminal_equipment_dp, 1),
            "net_external_static_pressure_pa": round(net_esp * safety_margin, 1),
            "ahu_internal_dp_pa": round(ahu_internal_dp, 1),
            "total_fan_static_pressure_pa": round(total_fan_sp, 1)
        }


class PipeHydraulics:
    """
    Bộ tính toán thủy lực mạng đường ống nước lạnh Chilled Water (CHW) và Nước giải nhiệt Condenser Water (CDW).
    Chuẩn mực: ASHRAE Fundamentals Ch. 22 & Darcy-Weisbach.
    """

    WATER_DENSITY = 1000.0  # kg/m3
    WATER_SPECIFIC_HEAT = 4.186  # kJ/(kg.K)
    WATER_KINEMATIC_VISCOSITY = 1.004e-6  # m2/s ở 20°C, ở 7°C nước lạnh ~ 1.4e-6 m2/s
    PIPE_ROUGHNESS_STEEL_MM = 0.045  # Độ nhám ống thép hàn mạ kẽm / SCH40

    # Bảng đường kính trong danh định chuẩn DN (mm) của ống thép SCH40
    PIPE_SCHEDULE_40 = {
        "DN15": 15.8, "DN20": 20.9, "DN25": 26.6, "DN32": 35.1, "DN40": 40.9,
        "DN50": 52.5, "DN65": 62.7, "DN80": 77.9, "DN100": 102.3, "DN125": 128.2,
        "DN150": 154.1, "DN200": 202.7, "DN250": 254.5, "DN300": 304.8,
        "DN350": 336.5, "DN400": 387.4, "DN450": 438.2, "DN500": 489.0
    }

    @classmethod
    def flow_rate_from_cooling_capacity(cls, capacity_kw: float, delta_t_celsius: float = 5.5) -> Dict[str, float]:
        """
        Tính lưu lượng nước lạnh yêu cầu từ công suất làm lạnh:
        Q (m3/h) = (kW * 3600) / (rho * Cp * Delta_T)
        - Hệ nước lạnh tiêu chuẩn: 7°C cấp / 12.5°C hồi -> Delta T = 5.5°C (~ 2.4 GPM/RT hoặc 0.57 m3/(h.RT))
        - Hệ nước giải nhiệt: 32°C vào / 37°C ra -> Delta T = 5.0°C (~ 3.0 GPM/RT hoặc 0.72 m3/(h.RT))
        """
        q_m3_s = (capacity_kw) / (cls.WATER_DENSITY * cls.WATER_SPECIFIC_HEAT * delta_t_celsius)
        q_m3_h = q_m3_s * 3600.0
        q_gpm = q_m3_h * 4.40287  # 1 m3/h = 4.40287 US GPM
        q_l_s = q_m3_s * 1000.0
        
        return {
            "capacity_kw": capacity_kw,
            "delta_t_k": delta_t_celsius,
            "flow_m3_h": round(q_m3_h, 2),
            "flow_l_s": round(q_l_s, 2),
            "flow_gpm": round(q_gpm, 1)
        }

    @classmethod
    def calculate_pipe_pressure_drop(cls, flow_m3_h: float, inner_dia_mm: float,
                                    water_temp_celsius: float = 7.0) -> Dict[str, float]:
        """
        Tính toán tổn thất cột áp thủy lực cho 1 mét ống thẳng (mH2O/100m và Pa/m)
        theo phương trình Darcy-Weisbach và công thức Swamee-Jain.
        """
        d_m = inner_dia_mm / 1000.0
        area_m2 = math.pi * (d_m ** 2) / 4.0
        v_m_s = (flow_m3_h / 3600.0) / area_m2
        
        # Độ nhớt động lực học nước theo nhiệt độ (°C)
        nu = 1.787e-6 / (1.0 + 0.0337 * water_temp_celsius + 0.000221 * (water_temp_celsius ** 2))
        reynolds = (v_m_s * d_m) / nu
        
        epsilon = (cls.PIPE_ROUGHNESS_STEEL_MM / 1000.0) / d_m
        if reynolds < 2000:
            f = 64.0 / max(reynolds, 1.0)
        else:
            f = 0.25 / (math.log10(epsilon / 3.7 + 5.74 / (reynolds ** 0.9)) ** 2)
            
        g = 9.81
        # h_f (mH2O/m) = f * (V^2 / (2*g*D))
        hf_per_m = f * (v_m_s ** 2) / (2.0 * g * d_m)
        hf_per_100m = hf_per_m * 100.0  # mH2O / 100m
        pa_per_m = hf_per_m * cls.WATER_DENSITY * g  # Pa / m
        
        return {
            "velocity_m_s": round(v_m_s, 2),
            "reynolds": round(reynolds, 0),
            "friction_factor": round(f, 4),
            "head_loss_m_per_100m": round(hf_per_100m, 2),
            "pa_per_meter": round(pa_per_m, 1)
        }

    @classmethod
    def auto_size_pipe(cls, flow_m3_h: float,
                       target_loss_m_per_100m: float = 3.0,
                       max_velocity_m_s: float = 2.2) -> Dict[str, any]:
        """
        Tự động chọn kích thước danh định ống DN theo tiêu chuẩn ASHRAE Ch. 22:
        - Giới hạn tổn thất ma sát tối đa: <= 3.0 mH2O / 100m (~ 300 Pa/m)
        - Giới hạn vận tốc tối đa: <= 1.2 m/s (cho ống nhỏ <= DN50) đến 2.4 m/s (cho ống chính lớn >= DN100)
        """
        selected_dn = None
        selected_data = None
        
        for dn, inner_d in cls.PIPE_SCHEDULE_40.items():
            res = cls.calculate_pipe_pressure_drop(flow_m3_h, inner_d)
            # Khống chế vận tốc âm học và xói mòn ống
            v_limit = 1.3 if inner_d <= 52.5 else max_velocity_m_s
            if res["head_loss_m_per_100m"] <= target_loss_m_per_100m and res["velocity_m_s"] <= v_limit:
                selected_dn = dn
                selected_data = res
                break
                
        if not selected_dn:
            # Nếu lưu lượng quá lớn, chọn ống lớn nhất
            selected_dn = "DN500"
            selected_data = cls.calculate_pipe_pressure_drop(flow_m3_h, cls.PIPE_SCHEDULE_40["DN500"])
            
        return {
            "selected_dn": selected_dn,
            "inner_dia_mm": cls.PIPE_SCHEDULE_40[selected_dn],
            "flow_m3_h": flow_m3_h,
            **selected_data
        }

    @classmethod
    def calculate_pump_head_and_power(cls, total_pipe_length_m: float,
                                      avg_loss_m_100m: float,
                                      equipment_losses_kpa: float,
                                      static_lift_m: float = 0.0,
                                      pump_eff: float = 0.75,
                                      motor_eff: float = 0.92,
                                      safety_margin: float = 1.15) -> Dict[str, float]:
        """
        Tính toán tổng cột áp bơm H (mH2O) và công suất điện trục động cơ bơm (kW):
        - H_friction: Đường ống + phụ kiện (hệ số tương đương tương đương 1.5 lần chiều dài thẳng)
        - H_equipment: Tổn thất qua Bình bay hơi / Bình ngưng Chiller, Coil AHU, Tháp giải nhiệt, Van điều khiển cân bằng PICV
        - H_static: Cột áp tĩnh hình học (chỉ áp dụng cho mạch hở như Tháp giải nhiệt; mạch kín = 0)
        - Công suất P_elec (kW) = (rho * g * Q * H) / (3.6 * 10^6 * eta_pump * eta_motor)
        """
        equivalent_length_m = total_pipe_length_m * 1.5  # Tính bù 50% cho co cút, van góc, tê
        hf_pipes_m = (equivalent_length_m / 100.0) * avg_loss_m_100m
        
        # 1 kPa = 0.101972 mH2O
        hf_equip_m = equipment_losses_kpa * 0.101972
        
        total_head_m = (hf_pipes_m + hf_equip_m + static_lift_m) * safety_margin
        
        return {
            "pipe_friction_head_m": round(hf_pipes_m, 2),
            "equipment_head_m": round(hf_equip_m, 2),
            "static_lift_m": round(static_lift_m, 2),
            "total_pump_head_m": round(total_head_m, 2),
            "total_pump_head_kpa": round(total_head_m * 9.81, 1),
            "total_pump_head_bar": round((total_head_m * 9.81) / 100.0, 2)
        }
