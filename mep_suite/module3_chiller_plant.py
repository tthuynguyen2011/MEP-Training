"""
Module 3: Mô phỏng Trạm Lạnh Trung tâm (Central Chiller Plant), Bơm, Tháp & Bơm nhiệt (Heat Pump)
Tham chiếu:
- AHRI Standard 550/590 (Performance Rating of Water-Chilling and Heat Pump Water-Heating Packages)
- ASHRAE 90.1 (Minimum Chiller and Heat Pump Efficiency Requirements)
- CTI STD-201 (Cooling Technology Institute Standard for Cooling Towers)
"""

import math
from typing import Dict, List, Tuple, Optional


class ChillerPlantSimulator:
    """
    Bộ tính toán & mô phỏng Trạm làm lạnh trung tâm (Central Chiller Plant):
    - Tính toán cân bằng nhiệt: Q_condenser = Q_evaporator + W_compressor
    - Đánh giá hiệu suất: COP, kW/RT, EER, IPLV/NPLV theo chuẩn AHRI 550/590
    - Đánh giá tổng hiệu suất toàn trạm (System Plant kW/RT: Chiller + Bơm ChW + Bơm CdW + Tháp)
    - So sánh cấu hình thủy lực: VPF (Biến lưu lượng sơ cấp) vs Primary-Secondary (Sơ cấp/Thứ cấp)
    """

    @staticmethod
    def cop_to_kw_per_rt(cop: float) -> float:
        """Đổi từ hệ số COP sang kW/RT: kW/RT = 3.51685 / COP"""
        return 3.51685 / max(cop, 0.01)

    @staticmethod
    def kw_per_rt_to_cop(kw_per_rt: float) -> float:
        """Đổi từ kW/RT sang COP: COP = 3.51685 / (kW/RT)"""
        return 3.51685 / max(kw_per_rt, 0.01)

    @classmethod
    def calculate_ahri_iplv(cls, cop_100: float, cop_75: float, cop_50: float, cop_25: float) -> Dict[str, float]:
        """
        Tính chỉ số hiệu suất non tải tích hợp IPLV (Integrated Part Load Value) theo AHRI 550/590:
        IPLV = 0.01*A + 0.42*B + 0.45*C + 0.12*D (với A, B, C, D là COP tại 100%, 75%, 50%, 25% tải)
        """
        iplv_cop = 0.01 * cop_100 + 0.42 * cop_75 + 0.45 * cop_50 + 0.12 * cop_25
        iplv_kw_per_rt = cls.cop_to_kw_per_rt(iplv_cop)
        
        return {
            "iplv_cop": round(iplv_cop, 2),
            "iplv_kw_per_rt": round(iplv_kw_per_rt, 3),
            "cop_full_load": round(cop_100, 2),
            "kw_per_rt_full_load": round(cls.cop_to_kw_per_rt(cop_100), 3)
        }

    @classmethod
    def simulate_chiller_at_part_load(cls, full_capacity_rt: float,
                                      full_load_kw_per_rt: float,
                                      load_fraction: float,
                                      cw_entering_temp_c: float = 30.0,
                                      chw_leaving_temp_c: float = 7.0,
                                      has_vfd: bool = True) -> Dict[str, float]:
        """
        Mô phỏng Chiller tại điểm tải cụ thể (Part-load simulation):
        - load_fraction (PLR): Tỷ lệ tải (0.1 đến 1.0)
        - cw_entering_temp_c: Nhiệt độ nước giải nhiệt vào bình ngưng
        - has_vfd: Máy nén có biến tần (VFD) hay khởi động trực tiếp (Constant Speed)
        """
        plr = max(0.15, min(1.0, load_fraction))
        operating_rt = full_capacity_rt * plr
        cooling_kw = operating_rt * 3.51685
        
        # Ảnh hưởng nhiệt độ nước giải nhiệt: chuẩn 30°C. Cứ giảm 1°C ECWT tiết kiệm ~1.5 - 2% điện năng Chiller
        temp_correction = 1.0 + 0.018 * (cw_entering_temp_c - 30.0) - 0.012 * (chw_leaving_temp_c - 7.0)
        
        # Đường cong Part-Load điển hình của Chiller ly tâm nước (Centrifugal water-cooled chiller)
        if has_vfd:
            # Chiller có VFD hiệu suất part load cực cao ở dải 50-75%
            # f(PLR) = a + b*PLR + c*PLR^2
            plr_multiplier = 0.55 + 0.25 * plr + 0.20 * (plr ** 2)
        else:
            # Constant speed Chiller suy giảm hiệu suất mạnh khi xuống dưới 40% tải
            plr_multiplier = 0.72 + 0.15 * plr + 0.13 * (plr ** 2)
            
        current_kw_per_rt = full_load_kw_per_rt * plr_multiplier * temp_correction
        chiller_power_kw = operating_rt * current_kw_per_rt
        cop = cls.kw_per_rt_to_cop(current_kw_per_rt)
        
        # Nhiệt lượng thải qua bình ngưng: Q_cond = Q_evap + Power_compressor
        heat_rejection_kw = cooling_kw + chiller_power_kw
        heat_rejection_rt = heat_rejection_kw / 3.51685
        
        return {
            "operating_load_rt": round(operating_rt, 1),
            "operating_load_kw": round(cooling_kw, 1),
            "chiller_power_kw": round(chiller_power_kw, 1),
            "operating_kw_per_rt": round(current_kw_per_rt, 3),
            "operating_cop": round(cop, 2),
            "heat_rejection_kw": round(heat_rejection_kw, 1),
            "heat_rejection_rt": round(heat_rejection_rt, 1)
        }

    @classmethod
    def evaluate_plant_total_efficiency(cls, cooling_load_rt: float,
                                        chiller_kw: float,
                                        chw_pump_kw: float,
                                        cdw_pump_kw: float,
                                        tower_fan_kw: float) -> Dict[str, any]:
        """
        Đánh giá hiệu suất tổng thể toàn trạm làm lạnh (Total Plant Efficiency - kW/RT)
        và phân hạng hiệu năng theo chuẩn công trình xanh Quốc tế (ASHRAE / BCA Green Mark / LEED).
        """
        total_plant_power_kw = chiller_kw + chw_pump_kw + cdw_pump_kw + tower_fan_kw
        plant_kw_per_rt = total_plant_power_kw / max(cooling_load_rt, 1.0)
        
        # Phân loại hiệu năng (Benchmarking):
        # < 0.65: Xuất sắc (World-class Green Building)
        # 0.65 - 0.75: Tốt (Standard Efficient System)
        # 0.75 - 0.88: Trung bình (Fair)
        # > 0.88: Kém / Cần cải tạo kiểm toán năng lượng (Poor / Energy Audit Priority)
        if plant_kw_per_rt < 0.65:
            rating = "Xuất sắc (World-Class / LEED Platinum Tier)"
            action = "Duy trì bảo dưỡng định kỳ và giám sát FDD liên tục."
        elif plant_kw_per_rt <= 0.75:
            rating = "Tốt (High Performance / ASHRAE 90.1 Compliance)"
            action = "Vận hành ổn định, có thể tối ưu thêm điểm đặt ChW reset."
        elif plant_kw_per_rt <= 0.88:
            rating = "Trung bình (Moderate Efficiency)"
            action = "Cần kiểm tra van điều khiển, cáu cặn bình ngưng và lắp VFD cho bơm."
        else:
            rating = "Kém (Low Efficiency - Tiêu hao điện cao)"
            action = "CẦN KIỂM TOÁN NĂNG LƯỢNG NGAY (ISO 50002): Chẩn đoán Low Delta-T, cặn tháp và tối ưu lại tuần tự chạy máy (Staging)."

        return {
            "cooling_load_rt": round(cooling_load_rt, 1),
            "total_plant_power_kw": round(total_plant_power_kw, 1),
            "plant_kw_per_rt": round(plant_kw_per_rt, 3),
            "chiller_share_pct": round((chiller_kw / total_plant_power_kw) * 100.0, 1),
            "chw_pump_share_pct": round((chw_pump_kw / total_plant_power_kw) * 100.0, 1),
            "cdw_pump_share_pct": round((cdw_pump_kw / total_plant_power_kw) * 100.0, 1),
            "tower_fan_share_pct": round((tower_fan_kw / total_plant_power_kw) * 100.0, 1),
            "benchmark_rating": rating,
            "recommended_action": action
        }


class HeatPumpSystem:
    """
    Tính toán Hệ thống Bơm nhiệt (Heat Pump) & Thu hồi nhiệt (Heat Recovery):
    - Bơm nhiệt nước nóng trung tâm (Air-to-Water / Water-to-Water)
    - Tận dụng nhiệt thải bình ngưng Chiller phục vụ cấp nước nóng sinh hoạt (DHW).
    """

    @staticmethod
    def calculate_dhw_heating_load(daily_hot_water_liters: float,
                                   cold_water_temp_c: float = 20.0,
                                   hot_water_temp_c: float = 60.0,
                                   heating_hours: float = 8.0) -> Dict[str, float]:
        """
        Tính công suất nhiệt yêu cầu để đun nước nóng sinh hoạt:
        Q (kJ) = m * Cp * Delta_T
        Q_heating (kW) = Q (kJ) / (Heating_Hours * 3600)
        """
        mass_kg = daily_hot_water_liters  # 1 lít nước ~ 1 kg
        delta_t = hot_water_temp_c - cold_water_temp_c
        total_energy_kj = mass_kg * 4.186 * delta_t
        total_energy_kwh = total_energy_kj / 3600.0
        
        required_heat_capacity_kw = total_energy_kwh / max(heating_hours, 0.5)
        
        return {
            "daily_liters": daily_hot_water_liters,
            "delta_t_k": delta_t,
            "total_energy_kwh_per_day": round(total_energy_kwh, 1),
            "required_heat_capacity_kw": round(required_heat_capacity_kw, 1)
        }

    @classmethod
    def compare_heat_pump_vs_electric_boiler(cls, heating_kwh_per_day: float,
                                             heat_pump_cop: float = 4.0,
                                             electricity_tariff_vnd_kwh: float = 2500.0) -> Dict[str, float]:
        """
        So sánh chi phí vận hành (OPEX) giữa Bơm nhiệt Heat Pump và Bình đun điện trở (Electric Boiler COP ~ 0.95):
        Tính số tiền tiết kiệm hàng năm và lượng giảm phát thải CO2 (Hệ số lưới điện VN ~ 0.72 kgCO2/kWh).
        """
        # Bình đun điện trở
        boiler_eff = 0.95
        kwh_boiler = heating_kwh_per_day / boiler_eff
        cost_boiler_annual = kwh_boiler * 365.0 * electricity_tariff_vnd_kwh
        
        # Bơm nhiệt Heat Pump
        kwh_heat_pump = heating_kwh_per_day / heat_pump_cop
        cost_heat_pump_annual = kwh_heat_pump * 365.0 * electricity_tariff_vnd_kwh
        
        annual_savings_vnd = cost_boiler_annual - cost_heat_pump_annual
        energy_saved_kwh = (kwh_boiler - kwh_heat_pump) * 365.0
        co2_reduction_tons = (energy_saved_kwh * 0.72) / 1000.0
        
        return {
            "boiler_annual_kwh": round(kwh_boiler * 365.0, 0),
            "heat_pump_annual_kwh": round(kwh_heat_pump * 365.0, 0),
            "boiler_cost_annual_vnd": round(cost_boiler_annual, 0),
            "heat_pump_cost_annual_vnd": round(cost_heat_pump_annual, 0),
            "annual_savings_vnd": round(annual_savings_vnd, 0),
            "energy_saved_kwh_annual": round(energy_saved_kwh, 0),
            "co2_reduction_tons_annual": round(co2_reduction_tons, 2),
            "energy_saving_percent": round((1.0 - kwh_heat_pump / kwh_boiler) * 100.0, 1)
        }
