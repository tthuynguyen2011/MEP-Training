"""
Module 4: Thiết kế & Cấu hình MEP Chuyên biệt theo Loại hình Công trình (ASHRAE Applications)
Tham chiếu:
- ASHRAE HVAC Applications Handbook (Commercial, Hospitality, Healthcare, Data Centers, Industrial)
- ASHRAE Standard 170 (Ventilation of Health Care Facilities)
- ASHRAE TC 9.9 (Thermal Guidelines for Data Processing Environments)
- ASHRAE Standard 62.1 (Ventilation for Acceptable Indoor Air Quality)
"""

import math
from typing import Dict, List, Tuple, Optional


class FacilityMEPConfigurator:
    """
    Bộ cấu hình thông số thiết kế & vận hành theo từng thể loại công trình chuyên biệt:
    1. Văn phòng thương mại (Office Buildings)
    2. Khách sạn & Nghỉ dưỡng (Hotels & Resorts)
    3. Bệnh viện & Phòng mổ (Healthcare & Operating Theatres - ASHRAE 170)
    4. Trung tâm Dữ liệu (Data Centers - ASHRAE TC 9.9 & PUE)
    5. Nhà xưởng công nghiệp (Industrial Plants)
    """

    @staticmethod
    def office_ashrae62_ventilation(floor_area_m2: float, num_people: int,
                                    space_type: str = "office_general") -> Dict[str, float]:
        """
        Tính toán lưu lượng gió tươi khu vực thở (Breathing Zone Outdoor Airflow Vbz)
        theo ASHRAE 62.1: Vbz = Rp * Pz + Ra * Az
        - Văn phòng tiêu chuẩn: Rp = 2.5 L/(s.người), Ra = 0.3 L/(s.m2)
        - Phòng họp (Conference): Rp = 2.5 L/(s.người), Ra = 0.3 L/(s.m2) với mật độ người cao
        """
        rp = 2.5  # L/s per person
        ra = 0.3  # L/s per m2
        if space_type == "conference":
            rp = 2.5
            ra = 0.3
            
        vbz_l_s = rp * num_people + ra * floor_area_m2
        vbz_m3_h = vbz_l_s * 3.6
        
        # Tỷ lệ gió tươi trên mỗi người (m3/h.người)
        fresh_air_per_person = vbz_m3_h / max(num_people, 1)
        
        return {
            "space_type": space_type,
            "floor_area_m2": floor_area_m2,
            "occupancy": num_people,
            "vbz_l_s": round(vbz_l_s, 1),
            "vbz_m3_h": round(vbz_m3_h, 1),
            "fresh_air_per_person_m3_h": round(fresh_air_per_person, 1)
        }

    @staticmethod
    def hotel_mep_parameters(num_rooms: int, star_rating: int = 5) -> Dict[str, float]:
        """
        Cấu hình thông số tải lạnh & Nước nóng sinh hoạt (DHW) cho Khách sạn:
        - Tiêu chuẩn nước nóng: 100 - 150 L/phòng/ngày ở 60°C (cho KS 4-5 sao)
        - Hệ số đồng thời tải lạnh phòng ngủ: 0.70 - 0.80
        - Mức ồn yêu cầu phòng ngủ: NC 25 - 30 (dàn lạnh FCU/VRV chạy êm)
        """
        liters_per_room_day = 120.0 if star_rating >= 4 else 80.0
        total_dhw_liters = num_rooms * liters_per_room_day
        
        # Tải lạnh trung bình mỗi phòng tiêu chuẩn ~ 2.5 - 3.5 kW (0.7 - 1.0 RT/room)
        cooling_per_room_kw = 3.2
        diversity_factor = 0.75
        coincident_cooling_load_kw = num_rooms * cooling_per_room_kw * diversity_factor
        
        return {
            "num_rooms": num_rooms,
            "star_rating": star_rating,
            "dhw_total_liters_day": round(total_dhw_liters, 0),
            "recommended_hot_water_temp_c": 60.0,
            "cooling_diversity_factor": diversity_factor,
            "total_coincident_cooling_kw": round(coincident_cooling_load_kw, 1),
            "total_coincident_cooling_rt": round(coincident_cooling_load_kw / 3.51685, 1),
            "max_guestroom_noise_nc": 28
        }

    @staticmethod
    def hospital_operating_theatre_ashrae170(room_area_m2: float, room_height_m: float = 3.0) -> Dict[str, any]:
        """
        Thiết kế Phòng mổ Bệnh viện theo ASHRAE Standard 170 (Bảng 7.1):
        - Bội số trao đổi không khí (Total Air Change): Tối thiểu 20 ACH
        - Bội số gió tươi ngoài (Outdoor Air Change): Tối thiểu 4 ACH
        - Chênh lệch áp suất: Dương (+) tối thiểu +2.5 Pa (+0.01 in.wg)
        - Nhiệt độ thiết kế: 18°C đến 23°C
        - Độ ẩm thiết kế: 20% đến 60% RH
        - Cấp lọc: Lọc sơ cấp (MERV 8) + Lọc thứ cấp (MERV 14) + Lọc HEPA H14 (99.99%) tại miệng trần Laminar
        """
        volume_m3 = room_area_m2 * room_height_m
        min_total_ach = 20.0
        min_outdoor_ach = 4.0
        
        total_supply_airflow_m3_h = volume_m3 * min_total_ach
        outdoor_airflow_m3_h = volume_m3 * min_outdoor_ach
        recirculated_airflow_m3_h = total_supply_airflow_m3_h - outdoor_airflow_m3_h
        
        # Để duy trì áp suất dương +2.5 Pa, lưu lượng hút thải/hồi = 85% - 90% lưu lượng cấp
        exhaust_airflow_m3_h = total_supply_airflow_m3_h * 0.88
        pressurization_excess_airflow_m3_h = total_supply_airflow_m3_h - exhaust_airflow_m3_h
        
        return {
            "room_volume_m3": round(volume_m3, 1),
            "min_total_airflow_m3_h": round(total_supply_airflow_m3_h, 1),
            "min_total_airflow_l_s": round(total_supply_airflow_m3_h / 3.6, 1),
            "outdoor_fresh_air_m3_h": round(outdoor_airflow_m3_h, 1),
            "recirc_airflow_m3_h": round(recirculated_airflow_m3_h, 1),
            "exhaust_return_airflow_m3_h": round(exhaust_airflow_m3_h, 1),
            "room_positive_pressure_pa": 2.5,
            "design_temp_celsius": "18.0 - 21.0 °C",
            "design_rh_percent": "45.0 - 55.0 %",
            "filter_requirement": "MERV 8 + MERV 14 + HEPA 99.99% (Laminar Flow ceiling)"
        }

    @staticmethod
    def data_center_pue_and_cooling(it_load_kw: float,
                                    cooling_system_kw: float,
                                    ups_and_power_loss_kw: float,
                                    lighting_aux_kw: float) -> Dict[str, any]:
        """
        Đánh giá Trung tâm dữ liệu theo ASHRAE TC 9.9 & Chỉ số hiệu quả PUE:
        - Tải nhiệt IT sinh ra 100% nhiệt hiện (SHR = 1.0)
        - Nhiệt độ khuyến nghị (Recommended A1): 18°C đến 27°C (Nhiệt độ khí cấp vào rack Server)
        - PUE (Power Usage Effectiveness) = Total Facility Power / IT Load Power
        """
        total_facility_power_kw = it_load_kw + cooling_system_kw + ups_and_power_loss_kw + lighting_aux_kw
        pue = total_facility_power_kw / max(it_load_kw, 1.0)
        
        # Đổi tải IT sang Tấn lạnh làm mát: 1 kW nhiệt IT = 1 kW tải lạnh ~ 0.2843 RT
        cooling_load_rt = it_load_kw / 3.51685
        
        # Đánh giá chỉ số PUE:
        # < 1.2: Tiên tiến (Hyperscale / Free Cooling)
        # 1.2 - 1.4: Tốt (Efficient Enterprise Data Center)
        # 1.4 - 1.7: Trung bình (Average Legacy Data Center)
        # > 1.7: Kém (Cần kiểm toán và tối ưu luồng khí Hot/Cold Aisle)
        if pue < 1.25:
            rating = "Xuất sắc (Eco/Hyperscale Level)"
        elif pue <= 1.45:
            rating = "Tốt (Modern Efficient Data Center)"
        elif pue <= 1.70:
            rating = "Trung bình (Có tiềm năng tiết kiệm 15-25% điện)"
        else:
            rating = "Kém hiệu quả (CẦN KIỂM TOÁN NĂNG LƯỢNG: Cô lập luồng nóng/lạnh, nâng nhiệt độ cấp)"

        return {
            "it_load_kw": round(it_load_kw, 1),
            "it_cooling_required_rt": round(cooling_load_rt, 1),
            "total_facility_power_kw": round(total_facility_power_kw, 1),
            "pue": round(pue, 2),
            "cooling_power_share_pct": round((cooling_system_kw / total_facility_power_kw) * 100.0, 1),
            "pue_rating": rating,
            "ashrae_tc99_guideline": "Class A1 Recommended: Cold Aisle Temp 18 - 27°C, Dew point <= 15°C"
        }

    @staticmethod
    def industrial_factory_ventilation(floor_area_m2: float, height_m: float,
                                       internal_equipment_heat_kw: float,
                                       allowable_temp_rise_c: float = 4.0) -> Dict[str, float]:
        """
        Tính toán thông gió giải nhiệt cưỡng bức cho Nhà xưởng sản xuất công nghiệp:
        Lưu lượng thông gió cần thiết để thải nhiệt dư nhà xưởng:
        Q_flow (m3/s) = Heat (kW) / (rho * Cp * Delta_T_allowable)
        """
        rho = 1.204  # kg/m3
        cp = 1.006  # kJ/(kg.K)
        volume_m3 = floor_area_m2 * height_m
        
        q_flow_m3_s = internal_equipment_heat_kw / (rho * cp * allowable_temp_rise_c)
        q_flow_m3_h = q_flow_m3_s * 3600.0
        ach = q_flow_m3_h / max(volume_m3, 1.0)
        
        return {
            "internal_heat_load_kw": internal_equipment_heat_kw,
            "allowable_temp_rise_k": allowable_temp_rise_c,
            "required_exhaust_airflow_m3_h": round(q_flow_m3_h, 1),
            "required_exhaust_airflow_l_s": round(q_flow_m3_s * 1000.0, 1),
            "calculated_air_changes_ach": round(ach, 1)
        }
