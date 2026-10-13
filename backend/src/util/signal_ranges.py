from typing import TypedDict


class RangeDict(TypedDict):
    min: int | float
    max: int | float


MaxxECUSensibleRanges: dict[int, dict[str, RangeDict]] = {
    1312: {
        "EngineSpeed": {"min": 0, "max": 8000},
        "ThrottlePos": {"min": 0, "max": 100},
        "MAP": {"min": 0, "max": 300},
        "Lambda_Average": {"min": 0.5, "max": 1.5},
    },
    1313: {
        "Lambda_A": {"min": 0.5, "max": 1.5},
        "Lambda_B": {"min": 0.5, "max": 1.5},
        "Ignition_Timing": {"min": -10, "max": 60},
        "IgnitionCut": {"min": 0, "max": 100},
    },
    1314: {
        "FuelInjPulsewidth": {"min": 0, "max": 30},
        "FuelInjDuty": {"min": 0, "max": 100},
        "FuelCut": {"min": 0, "max": 100},
        "VehicleSpeed": {"min": 0, "max": 300},
    },
    1315: {
        "WheelSpeedAvgNonDriven": {"min": 0, "max": 300},
        "WheelSpeedAvgDriven": {"min": 0, "max": 300},
        "TracControl_SlipMeasured": {"min": 0, "max": 50},
        "TracControl_SlipTarget": {"min": 0, "max": 50},
    },
    1316: {
        "TracControl_CutRequest": {"min": 0, "max": 100},
        "Lambda_corr_A": {"min": 50, "max": 150},
        "Lambda_corr_B": {"min": 50, "max": 150},
        "ECU_FirmwareVersion": {"min": 1.0, "max": 10.0},
    },
    1317: {
        "User_Channel_9": {"min": 0, "max": 1000},
        "User_Channel_10": {"min": 0, "max": 1000},
        "User_Channel_11": {"min": 0, "max": 1000},
        "User_Channel_12": {"min": 0, "max": 1000},
    },
    1318: {
        "Shiftcut_active": {"min": 0, "max": 1},
        "Revlimit_active": {"min": 0, "max": 1},
        "Antilag_active": {"min": 0, "max": 1},
        "Launch_control_active": {"min": 0, "max": 1},
        "TracControl_power_limiter_active": {"min": 0, "max": 1},
        "Throttle_blip_active": {"min": 0, "max": 1},
        "AC_idle_up_active": {"min": 0, "max": 1},
        "Knock_detected": {"min": 0, "max": 1},
        "Brake_pedal_active": {"min": 0, "max": 1},
        "Clutch_pedal_active": {"min": 0, "max": 1},
        "Speed_limit_active": {"min": 0, "max": 1},
        "GP_limiter_active": {"min": 0, "max": 1},
        "User_cut_active": {"min": 0, "max": 1},
        "ECU_is_logging": {"min": 0, "max": 1},
        "Nitrous_active": {"min": 0, "max": 1},
        "Spare_status_bit": {"min": 0, "max": 1},
        "Spare_0x526_2": {"min": 0, "max": 1000},
        "RevLimit_RPM": {"min": 0, "max": 8000},
        "Spare_0x526_6": {"min": 0, "max": 1000},
    },
    1319: {
        "Acc_forward": {"min": -2.0, "max": 2.0},
        "Acc_Right": {"min": -2.0, "max": 2.0},
        "Acc_Up": {"min": -2.0, "max": 2.0},
        "Lambda_Target": {"min": 0.6, "max": 1.3},
    },
    1320: {
        "Knock_Level_All_peak": {"min": 0, "max": 500},
        "Knock_correction": {"min": -15, "max": 0},
        "Knock_count": {"min": 0, "max": 100},
        "Knock_last_cylinder": {"min": 0, "max": 12},
    },
    1328: {
        "CoolantTemp": {"min": -40, "max": 120},
        "IntakeAirTemp": {"min": -40, "max": 100},
        "BaroPress": {"min": 50, "max": 110},
        "ECU_BatteryVoltage": {"min": 8, "max": 16},
    },
    1329: {
        "ExhaustTemp1": {"min": 0, "max": 1000},
        "Ignition_Trim_total": {"min": -20, "max": 20},
        "FuelEthanolContent": {"min": 0, "max": 100},
        "FuelTrimTotal": {"min": -30, "max": 30},
    },
    1330: {
        "ExhaustTemp2": {"min": 0, "max": 1000},
        "ExhaustTemp3": {"min": 0, "max": 1000},
        "ExhaustTemp4": {"min": 0, "max": 1000},
        "ExhaustTemp5": {"min": 0, "max": 1000},
    },
    1331: {
        "ExhaustTemp6": {"min": 0, "max": 1000},
        "ExhaustTemp7": {"min": 0, "max": 1000},
        "ExhaustTemp8": {"min": 0, "max": 1000},
        "ExhaustTempHighest": {"min": 0, "max": 1000},
    },
    1332: {
        "ECU_LostSyncCount": {"min": 0, "max": 10},
        "ECU_ErrorCodeCount": {"min": 0, "max": 10},
        "ECU_Temp": {"min": -20, "max": 85},
        "ExhaustTempDifference": {"min": 0, "max": 200},
    },
    1333: {
        "ECU_UserAnalogInput1": {"min": 0, "max": 5},
        "ECU_UserAnalogInput2": {"min": 0, "max": 5},
        "ECU_UserAnalogInput3": {"min": 0, "max": 5},
        "ECU_UserAnalogInput4": {"min": 0, "max": 5},
    },
    1334: {
        "GearPosn": {"min": 0, "max": 6},
        "Boost_Solenoid_Duty": {"min": 0, "max": 100},
        "Engine_Oil_Pressure": {"min": 0, "max": 800},
        "Engine_Oil_Temperature": {"min": -40, "max": 150},
    },
    1335: {
        "Fuel_Pressure_1": {"min": 0, "max": 800},
        "Wastegate_Pressure": {"min": 0, "max": 300},
        "Coolant_Pressure": {"min": 0, "max": 300},
        "Boost_Target": {"min": 0, "max": 300},
    },
    1336: {
        "User_Channel_1": {"min": 0, "max": 1000},
        "User_Channel_2": {"min": 0, "max": 1000},
        "User_Channel_3": {"min": 0, "max": 1000},
        "User_Channel_4": {"min": 0, "max": 1000},
    },
    1337: {
        "User_Channel_5": {"min": 0, "max": 1000},
        "User_Channel_6": {"min": 0, "max": 1000},
        "User_Channel_7": {"min": 0, "max": 1000},
        "User_Channel_8": {"min": 0, "max": 1000},
    },
    1344: {
        "Active_boost_table": {"min": 0, "max": 4},
        "Active_Tune_Selector": {"min": 0, "max": 4},
        "Virtual_fuel_tank": {"min": 0, "max": 100},
        "Transmission_Temp": {"min": -40, "max": 150},
        "Differential_Temp": {"min": -40, "max": 150},
    },
    1345: {
        "VVT_intake_cam1_position": {"min": -30, "max": 60},
        "VVT_exhaust_cam1_position": {"min": -30, "max": 60},
        "VVT_intake_cam2_position": {"min": -30, "max": 60},
        "VVT_exhaust_cam2_position": {"min": -30, "max": 60},
    },
    1346: {
        "VVT_intake_cam_target": {"min": -30, "max": 60},
        "VVT_exhaust_cam_target": {"min": -30, "max": 60},
        "Spare_0x542_4": {"min": 0, "max": 1000},
        "Spare_0x542_6": {"min": 0, "max": 1000},
    },
}