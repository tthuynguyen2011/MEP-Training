"""
Module 1: Nhiệt ẩm học Psychrometrics & Tính toán Tải nhiệt RTS theo ASHRAE Fundamentals
Tham chiếu:
- ASHRAE Handbook of Fundamentals (Ch. 1 Psychrometrics, Ch. 17/18 Nonresidential Cooling and Heating Load Calculations)
- QCVN 02:2022/BXD (Số liệu điều kiện tự nhiên)
- TCVN 5687:2024 (Thông gió và điều hòa không khí)
"""

import math
from typing import Dict, Tuple, Optional


class Psychrometrics:
    """
    Bộ tính toán nhiệt ẩm học chuẩn xác theo phương trình ASHRAE Fundamentals Ch. 1.
    Mặc định áp suất khí quyển tiêu chuẩn ở mực nước biển: 101325 Pa (101.325 kPa).
    """

    def __init__(self, p_atm: float = 101325.0):
        self.p_atm = p_atm  # Pa

    def sat_vapor_pressure(self, t_celsius: float) -> float:
        """
        Tính áp suất hơi nước bão hòa Pws (Pa) theo ASHRAE Fundamentals 2017 Ch. 1 Eq. 5 & 6.
        Dải nhiệt độ: 0°C đến 200°C.
        """
        T = t_celsius + 273.15  # Kelvin
        if t_celsius >= 0.0:
            c8 = -5.8002206e03
            c9 = 1.3914993e00
            c10 = -4.8640239e-02
            c11 = 4.1764768e-05
            c12 = -1.4452093e-08
            c13 = 6.5459673e00
            ln_pws = (c8 / T + c9 + c10 * T + c11 * (T ** 2) + 
                      c12 * (T ** 3) + c13 * math.log(T))
            return math.exp(ln_pws)
        else:
            # Dưới 0°C (trên băng)
            c1 = -5.6745359e03
            c2 = 6.3925247e00
            c3 = -9.6778430e-03
            c4 = 6.2215701e-07
            c5 = 2.0747825e-09
            c6 = -9.4840240e-13
            c7 = 4.1635019e00
            ln_pws = (c1 / T + c2 + c3 * T + c4 * (T ** 2) + 
                      c5 * (T ** 3) + c6 * (T ** 4) + c7 * math.log(T))
            return math.exp(ln_pws)

    def humidity_ratio_from_pw(self, pw: float) -> float:
        """Dung ẩm W (kg_w / kg_da) từ áp suất hơi riêng phần pw (Pa). ASHRAE Eq. 22"""
        return 0.621945 * pw / max(self.p_atm - pw, 1.0)

    def pw_from_humidity_ratio(self, w: float) -> float:
        """Áp suất hơi pw (Pa) từ dung ẩm W"""
        return self.p_atm * w / (0.621945 + w)

    def state_from_tdb_rh(self, t_db: float, rh_percent: float) -> Dict[str, float]:
        """
        Xác định đầy đủ trạng thái không khí từ Nhiệt độ bầu khô T_db (°C) và Độ ẩm tương đối RH (%)
        Trả về: T_db, RH, W (kg/kg_da), W_g (g/kg_da), h (kJ/kg_da), v (m3/kg_da), T_dp (°C), P_w (Pa)
        """
        phi = max(0.001, min(100.0, rh_percent)) / 100.0
        pws = self.sat_vapor_pressure(t_db)
        pw = phi * pws
        w = self.humidity_ratio_from_pw(pw)
        
        # Enthalpy (kJ/kg_da) ASHRAE Eq. 32: h = 1.006 * t + W * (2501 + 1.86 * t)
        h = 1.006 * t_db + w * (2501.0 + 1.86 * t_db)
        
        # Thể tích riêng v (m3/kg_da) ASHRAE Eq. 28: v = R_da * T * (1 + 1.607858 * W) / P
        r_da = 287.042  # J / (kg_da * K)
        T_kelvin = t_db + 273.15
        v = (r_da * T_kelvin * (1.0 + 1.607858 * w)) / self.p_atm
        
        # Nhiệt độ đọng sương T_dp (°C) ASHRAE Fundamentals Ch. 1 Eq. 39 & 40
        alpha = math.log(pw / 1000.0)  # pw in kPa
        if t_db >= 0.0:
            t_dp = 6.54 + 14.526 * alpha + 0.7389 * (alpha ** 2) + 0.09486 * (alpha ** 3) + 0.4569 * ((pw / 1000.0) ** 0.1984)
        else:
            t_dp = 6.09 + 12.608 * alpha + 0.4959 * (alpha ** 2)
            
        return {
            "t_db": round(t_db, 2),
            "rh": round(rh_percent, 1),
            "w_kg": w,
            "w_g": round(w * 1000.0, 3),
            "h_kj": round(h, 2),
            "v_m3": round(v, 4),
            "t_dp": round(t_dp, 2),
            "pw_pa": round(pw, 1)
        }

    def mix_airstreams(self, state1: Dict[str, float], m1: float,
                       state2: Dict[str, float], m2: float) -> Dict[str, float]:
        """
        Hòa trộn 2 dòng không khí (Lưu lượng khối lượng m1, m2 tính theo kg/s hoặc m3/s quy đổi).
        Định luật bảo toàn khối lượng và năng lượng:
        m3 = m1 + m2
        h3 = (m1*h1 + m2*h2) / m3
        w3 = (m1*w1 + m2*w2) / m3
        """
        m_total = m1 + m2
        if m_total <= 0:
            return state1
        
        w_mix = (m1 * state1["w_kg"] + m2 * state2["w_kg"]) / m_total
        h_mix = (m1 * state1["h_kj"] + m2 * state2["h_kj"]) / m_total
        
        # Tìm T_db từ Enthalpy và W: h = 1.006 * t + W * (2501 + 1.86 * t) => t = (h - 2501*W) / (1.006 + 1.86*W)
        t_mix = (h_mix - 2501.0 * w_mix) / (1.006 + 1.86 * w_mix)
        
        # Tính RH tương ứng
        pw_mix = self.pw_from_humidity_ratio(w_mix)
        pws_mix = self.sat_vapor_pressure(t_mix)
        rh_mix = min(100.0, max(0.0, (pw_mix / pws_mix) * 100.0))
        
        return self.state_from_tdb_rh(t_mix, rh_mix)

    def cooling_coil_process(self, enter_state: Dict[str, float],
                             adp_celsius: float,
                             bypass_factor: float) -> Tuple[Dict[str, float], float]:
        """
        Quá trình xử lý nhiệt ẩm qua dàn lạnh (Cooling & Dehumidification):
        - enter_state: Trạng thái không khí vào dàn
        - adp_celsius: Điểm sương đọng bề mặt thiết bị (Apparatus Dew Point)
        - bypass_factor (BF): Hệ số lọt gió (0.05 đến 0.20 cho AHU/FCU điển hình)
        Trả về: (leave_state, shr)
        """
        adp_state = self.state_from_tdb_rh(adp_celsius, 100.0)
        
        # Điểm rời dàn nằm trên đoạn nối giữa Enter và ADP
        t_leave = adp_celsius + bypass_factor * (enter_state["t_db"] - adp_celsius)
        w_leave = adp_state["w_kg"] + bypass_factor * (enter_state["w_kg"] - adp_state["w_kg"])
        
        # Tính lại RH rời dàn
        pw_leave = self.pw_from_humidity_ratio(w_leave)
        pws_leave = self.sat_vapor_pressure(t_leave)
        rh_leave = min(100.0, max(0.0, (pw_leave / pws_leave) * 100.0))
        
        leave_state = self.state_from_tdb_rh(t_leave, rh_leave)
        
        # Hệ số nhiệt hiện SHR
        delta_h_total = enter_state["h_kj"] - leave_state["h_kj"]
        q_sensible = 1.006 * (enter_state["t_db"] - leave_state["t_db"])
        shr = q_sensible / max(delta_h_total, 1e-4) if delta_h_total > 0 else 1.0
        
        return leave_state, round(min(1.0, max(0.0, shr)), 3)


class RTSCoolingLoad:
    """
    Tính toán Tải lạnh thiết kế đỉnh (Peak Cooling Load) theo chuẩn ASHRAE RTS / Heat Balance.
    Hỗ trợ tích hợp bảng hệ số truyền nhiệt QCVN 09:2017/BXD & ASHRAE 90.1.
    """

    def __init__(self, location: str = "TP. Hồ Chí Minh", t_outdoor_db: float = 35.0,
                 t_outdoor_wb: float = 28.0, t_indoor_db: float = 24.0, rh_indoor: float = 55.0):
        self.location = location
        self.t_out_db = t_outdoor_db
        self.t_out_wb = t_outdoor_wb
        self.t_in_db = t_indoor_db
        self.rh_in = rh_indoor
        self.psychro = Psychrometrics()
        self.in_state = self.psychro.state_from_tdb_rh(t_indoor_db, rh_indoor)
        # Giả định ngoài trời 35°C / 28°C WB xấp xỉ RH ~60%
        self.out_state = self.psychro.state_from_tdb_rh(t_outdoor_db, 60.0)

    def calculate_envelope_load(self, wall_area_m2: float, wall_u_value: float,
                                roof_area_m2: float, roof_u_value: float,
                                glass_area_m2: float, glass_u_value: float,
                                glass_shgc: float, peak_solar_irradiance: float = 650.0) -> Dict[str, float]:
        """
        Tính tải truyền nhiệt qua kết cấu bao che (W):
        - Q_wall = U * A * CLTD_corr (ở đây xấp xỉ qua Delta_T tương đương có bức xạ nhiệt mặt trời)
        - Q_solar_glass = Area * SHGC * Irradiance * IAC
        """
        delta_t_air = self.t_out_db - self.t_in_db
        # Tường ngoài hấp thụ bức xạ, nhiệt độ tương đương Sol-air delta T ~ delta_T + 12°C
        sol_air_delta_wall = delta_t_air + 10.0
        sol_air_delta_roof = delta_t_air + 18.0  # Mái nhận bức xạ mặt trời trực tiếp trên đỉnh
        
        q_wall = wall_area_m2 * wall_u_value * sol_air_delta_wall
        q_roof = roof_area_m2 * roof_u_value * sol_air_delta_roof
        q_glass_cond = glass_area_m2 * glass_u_value * delta_t_air
        q_glass_solar = glass_area_m2 * glass_shgc * peak_solar_irradiance * 0.85  # IAC rèm che bên trong ~0.85
        
        q_envelope_total = q_wall + q_roof + q_glass_cond + q_glass_solar
        return {
            "q_wall_w": round(q_wall, 1),
            "q_roof_w": round(q_roof, 1),
            "q_glass_conduction_w": round(q_glass_cond, 1),
            "q_glass_solar_radiation_w": round(q_glass_solar, 1),
            "q_envelope_total_w": round(q_envelope_total, 1)
        }

    def calculate_internal_load(self, floor_area_m2: float, num_people: int,
                                lighting_w_per_m2: float, equipment_w_per_m2: float,
                                activity_sensible_w: float = 75.0,
                                activity_latent_w: float = 55.0) -> Dict[str, float]:
        """
        Tính toán tải nhiệt phát sinh từ nội vi công trình (Internal Loads):
        - Người (Sensible & Latent theo mức độ hoạt động văn phòng/khách sạn)
        - Chiếu sáng (100% Sensible)
        - Thiết bị máy tính, văn phòng (100% Sensible)
        """
        q_people_sensible = num_people * activity_sensible_w
        q_people_latent = num_people * activity_latent_w
        q_lighting = floor_area_m2 * lighting_w_per_m2
        q_equipment = floor_area_m2 * equipment_w_per_m2
        
        q_int_sensible = q_people_sensible + q_lighting + q_equipment
        q_int_latent = q_people_latent
        
        return {
            "q_people_sensible_w": round(q_people_sensible, 1),
            "q_people_latent_w": round(q_people_latent, 1),
            "q_lighting_w": round(q_lighting, 1),
            "q_equipment_w": round(q_equipment, 1),
            "q_internal_sensible_w": round(q_int_sensible, 1),
            "q_internal_latent_w": round(q_int_latent, 1),
            "q_internal_total_w": round(q_int_sensible + q_int_latent, 1)
        }

    def calculate_ventilation_load(self, fresh_air_flow_l_s: float) -> Dict[str, float]:
        """
        Tính tải xử lý gió tươi theo ASHRAE 62.1 & TCVN 5687:2024:
        - Lưu lượng m3/s = L/s / 1000
        - Q_s = 1.23 * Flow (L/s) * (T_out - T_in) [W]
        - Q_l = 3010 * Flow (L/s) * (W_out - W_in) [W]
        - Q_total = 1.2 * Flow (L/s) * (h_out - h_in) [W]
        """
        delta_t = self.out_state["t_db"] - self.in_state["t_db"]
        delta_w = max(0.0, self.out_state["w_kg"] - self.in_state["w_kg"])
        delta_h = max(0.0, self.out_state["h_kj"] - self.in_state["h_kj"])
        
        q_vent_sensible = 1.204 * 1.006 * fresh_air_flow_l_s * delta_t  # 1.21 * L/s * dT
        q_vent_latent = 1.204 * 2501.0 * fresh_air_flow_l_s * delta_w  # ~3010 * L/s * dW
        q_vent_total = 1.204 * fresh_air_flow_l_s * delta_h
        
        return {
            "fresh_air_l_s": round(fresh_air_flow_l_s, 1),
            "fresh_air_m3_h": round(fresh_air_flow_l_s * 3.6, 1),
            "q_vent_sensible_w": round(q_vent_sensible, 1),
            "q_vent_latent_w": round(q_vent_latent, 1),
            "q_vent_total_w": round(q_vent_total, 1)
        }

    def synthesize_room_load(self, envelope: Dict[str, float],
                             internal: Dict[str, float],
                             ventilation: Dict[str, float],
                             safety_factor: float = 1.10) -> Dict[str, float]:
        """
        Tổng hợp toàn bộ tải lạnh cho khu vực (Room/Zone Peak Load Summary):
        - Tải không gian (Room Sensible / Latent)
        - Tải tổng dàn lạnh (Grand Total bao gồm gió tươi)
        - Đổi sang đơn vị chuẩn: kW, BTU/h, RT (Tấn lạnh)
        """
        room_sensible = envelope["q_envelope_total_w"] + internal["q_internal_sensible_w"]
        room_latent = internal["q_internal_latent_w"]
        room_total = room_sensible + room_latent
        
        grand_sensible = (room_sensible + ventilation["q_vent_sensible_w"]) * safety_factor
        grand_latent = (room_latent + ventilation["q_vent_latent_w"]) * safety_factor
        grand_total = grand_sensible + grand_latent
        
        capacity_kw = grand_total / 1000.0
        capacity_rt = capacity_kw / 3.51685  # 1 RT = 3.51685 kW
        capacity_btu = capacity_kw * 3412.14
        
        shr = grand_sensible / grand_total if grand_total > 0 else 1.0
        
        return {
            "room_sensible_kw": round(room_sensible / 1000.0, 2),
            "room_latent_kw": round(room_latent / 1000.0, 2),
            "ventilation_total_kw": round(ventilation["q_vent_total_w"] / 1000.0, 2),
            "grand_total_kw": round(capacity_kw, 2),
            "grand_total_rt": round(capacity_rt, 2),
            "grand_total_btu_h": round(capacity_btu, 0),
            "coil_shr": round(shr, 3)
        }
