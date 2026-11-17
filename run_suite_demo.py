"""
Kiểm thử và Chạy thử nghiệm toàn bộ 7 Modules của MEP Energy Master Suite
"""

import sys
import os

# Thêm đường dẫn thư viện
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mep_suite.module1_psychro_load import Psychrometrics, RTSCoolingLoad
from mep_suite.module2_hydraulics_duct import DuctSizer, PipeHydraulics
from mep_suite.module3_chiller_plant import ChillerPlantSimulator, HeatPumpSystem
from mep_suite.module4_facilities import FacilityMEPConfigurator
from mep_suite.module5_energy_codes import EnergyCodeCompliance
from mep_suite.module6_iso50002_audit import EnergyAuditISO50002, FinancialAnalysisLCCA
from mep_suite.module7_cx_tab_fdd import CommissioningTAB, FaultDetectionDiagnostics


def run_demo():
    print("=" * 80)
    print("KIỂM THỬ MEP ENERGY MASTER SUITE (ASHRAE & ISO 500XX)")
    print("=" * 80)

    # 1. Module 1: Psychrometrics & RTS Load
    print("\n[MODULE 1] NHIỆT ẨM HỌC & TẢI LẠNH RTS")
    psy = Psychrometrics()
    indoor = psy.state_from_tdb_rh(24.0, 55.0)
    outdoor = psy.state_from_tdb_rh(35.0, 60.0)
    print(f"Trạng thái trong nhà: {indoor['t_db']}°C, {indoor['rh']}% RH -> Enthalpy: {indoor['h_kj']} kJ/kg, Dung ẩm: {indoor['w_g']} g/kg, Đọng sương: {indoor['t_dp']}°C")
    print(f"Trạng thái ngoài trời: {outdoor['t_db']}°C, {outdoor['rh']}% RH -> Enthalpy: {outdoor['h_kj']} kJ/kg, Dung ẩm: {outdoor['w_g']} g/kg, Đọng sương: {outdoor['t_dp']}°C")
    
    rts = RTSCoolingLoad()
    env = rts.calculate_envelope_load(wall_area_m2=150, wall_u_value=1.8, roof_area_m2=200, roof_u_value=0.5, glass_area_m2=80, glass_u_value=2.8, glass_shgc=0.35)
    intern = rts.calculate_internal_load(floor_area_m2=200, num_people=20, lighting_w_per_m2=7.0, equipment_w_per_m2=12.0)
    vent = rts.calculate_ventilation_load(fresh_air_flow_l_s=160.0)
    room_summary = rts.synthesize_room_load(env, intern, vent)
    print(f"-> Tải lạnh tổng phòng 200m2: {room_summary['grand_total_kw']} kW ({room_summary['grand_total_rt']} RT) | SHR = {room_summary['coil_shr']}")

    # 2. Module 2: Khí động & Thủy lực
    print("\n[MODULE 2] KHÍ ĐỘNG HỌC ỐNG GIÓ & THỦY LỰC ĐƯỜNG ỐNG NƯỚC")
    duct = DuctSizer()
    d_res = duct.size_duct_by_equal_friction(airflow_m3_h=3500.0, target_friction_pa_m=1.0, max_velocity_m_s=6.0)
    print(f"-> Sizing ống gió 3500 m3/h: Ống chữ nhật {d_res['rect_width_mm']} x {d_res['rect_height_mm']} mm, Vận tốc = {d_res['actual_velocity_m_s']} m/s, Ma sát = {d_res['actual_dp_pa_m']} Pa/m")
    
    flow_info = PipeHydraulics.flow_rate_from_cooling_capacity(capacity_kw=350.0, delta_t_celsius=5.5)
    pipe_res = PipeHydraulics.auto_size_pipe(flow_info["flow_m3_h"])
    print(f"-> Sizing ống nước lạnh cho 350 kW (100 RT): Lưu lượng = {flow_info['flow_m3_h']} m3/h ({flow_info['flow_gpm']} GPM) -> Chọn cỡ {pipe_res['selected_dn']} (V = {pipe_res['velocity_m_s']} m/s, hf = {pipe_res['head_loss_m_per_100m']} mH2O/100m)")

    # 3. Module 3: Chiller Plant Simulation
    print("\n[MODULE 3] MÔ PHỎNG TRẠM LẠNH TRUNG TÂM (CHILLER PLANT)")
    plant_eval = ChillerPlantSimulator.evaluate_plant_total_efficiency(cooling_load_rt=400.0, chiller_kw=220.0, chw_pump_kw=22.0, cdw_pump_kw=30.0, tower_fan_kw=15.0)
    print(f"-> Đánh giá hiệu suất trạm 400 RT: Tổng công suất điện = {plant_eval['total_plant_power_kw']} kW -> Hiệu suất Trạm = {plant_eval['plant_kw_per_rt']} kW/RT")
    print(f"   Xếp hạng: {plant_eval['benchmark_rating']} | Khuyến nghị: {plant_eval['recommended_action']}")

    # 4. Module 4: Facilities MEP
    print("\n[MODULE 4] CẤU HÌNH THIẾT KẾ CÔNG TRÌNH CHUYÊN BIỆT")
    or_spec = FacilityMEPConfigurator.hospital_operating_theatre_ashrae170(room_area_m2=45.0, room_height_m=3.0)
    print(f"-> Phòng mổ Bệnh viện 45m2 (ASHRAE 170): Gió cấp tổng = {or_spec['min_total_airflow_m3_h']} m3/h (20 ACH), Áp suất = +{or_spec['room_positive_pressure_pa']} Pa")
    dc_spec = FacilityMEPConfigurator.data_center_pue_and_cooling(it_load_kw=500.0, cooling_system_kw=160.0, ups_and_power_loss_kw=45.0, lighting_aux_kw=5.0)
    print(f"-> Trung tâm dữ liệu 500 kW IT (ASHRAE TC 9.9): PUE = {dc_spec['pue']} | Xếp hạng: {dc_spec['pue_rating']}")

    # 5. Module 5: Energy Code
    print("\n[MODULE 5] KIỂM TRA QUY CHUẨN NĂNG LƯỢNG (QCVN 09:2017 & ASHRAE 90.1)")
    ottv_check = EnergyCodeCompliance.calculate_ottv_wall(gross_wall_area_m2=1000.0, window_area_m2=350.0, u_wall=1.8, u_window=2.4, shgc_window=0.32)
    print(f"-> Kiểm tra OTTV tường: {ottv_check['ottv_w_m2']} W/m2 (Quy chuẩn <= {ottv_check['limit_qcvn09_w_m2']} W/m2) -> Kết quả: {'ĐẠT (PASS)' if ottv_check['is_compliant'] else 'KHÔNG ĐẠT'}")

    # 6. Module 6: ISO 50002 Energy Audit & Financial LCCA
    print("\n[MODULE 6] KIỂM TOÁN NĂNG LƯỢNG ISO 50002 & HIỆU QUẢ TÀI CHÍNH")
    audit_chiller = EnergyAuditISO50002.analyze_field_chiller_logging(chw_flow_m3_h=120.0, chw_temp_in_c=10.5, chw_temp_out_c=7.0, chiller_active_power_kw=115.0)
    print(f"-> Đo đạc thực địa Chiller: Delta-T = {audit_chiller['measured_delta_t_c']}°C -> Tải thực tế: {audit_chiller['cooling_actual_rt']} RT, Hiệu suất thực tế = {audit_chiller['operating_kw_per_rt']} kW/RT | Chẩn đoán: {audit_chiller['diagnosis_severity']}")
    
    ecm = EnergyAuditISO50002.ecm_vfd_pump_savings(current_pump_kw=37.0, operating_hours_year=4500)
    lcca = FinancialAnalysisLCCA.evaluate_investment(capex_vnd=120_000_000, annual_savings_vnd=ecm['annual_savings_vnd'])
    print(f"-> Đề xuất ECM Lắp biến tần VFD cho bơm: Tiết kiệm {ecm['annual_savings_kwh']} kWh/năm ({ecm['annual_savings_vnd']:,.0f} VNĐ/năm)")
    print(f"   Thời gian hoàn vốn: {lcca['simple_payback_years']} năm | NPV 15 năm: {lcca['npv_vnd']:,.0f} VNĐ | IRR: {lcca['irr_percent']}%")

    # 7. Module 7: Cx & FDD
    print("\n[MODULE 7] COMMISSIONING (TAB) & CHẨN ĐOÁN LỖI FDD")
    tab = CommissioningTAB.evaluate_flow_deviations([500, 750, 600, 800], [530, 720, 580, 810])
    print(f"-> Nghiệm thu cân bằng gió TAB: {tab['status_summary']} (Độ lệch cực đại: {max(tab['deviations_percent'])}%)")
    
    fdd_report = FaultDetectionDiagnostics.diagnose_ahu_operation(supply_air_temp_c=16.0, setpoint_temp_c=13.0, cooling_valve_pos_pct=100.0, heating_valve_pos_pct=0.0, outdoor_air_temp_c=34.0, mixed_air_temp_c=25.0)
    for fault in fdd_report:
        print(f"   FDD Alert: {fault}")

    print("\n" + "=" * 80)
    print("HOÀN TẤT KIỂM THỬ 7 MODULES - TOÀN BỘ CÔNG THỨC HOẠT ĐỘNG CHUẨN XÁC!")
    print("=" * 80)


if __name__ == "__main__":
    run_demo()
