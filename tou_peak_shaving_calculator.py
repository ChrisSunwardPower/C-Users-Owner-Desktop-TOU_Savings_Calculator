import streamlit as st

# Utility Rates
TOU_RATES = {
    'PGE': {'peak_rate': 0.28, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.32, 'off_peak_rate': 0.12}
}

# Battery Specifications
BATTERY_SPECS = {
    'FranklinWH aPower 2': {'storage_kwh': 15, 'power_kw': 10, 'peak_kw': 15},
    'Tesla Powerwall 2': {'storage_kwh': 13.5, 'power_kw': 5, 'peak_kw': 7}
}

# Savings Calculation

def calculate_savings(monthly_bill, provider, battery_type, battery_units):
    rates = TOU_RATES[provider]
    peak_rate = rates['peak_rate']
    off_peak_rate = rates['off_peak_rate']
    avg_rate = (peak_rate * 0.3) + (off_peak_rate * 0.7)

    # Battery Specifications
    specs = BATTERY_SPECS[battery_type]
    battery_storage = specs['storage_kwh'] * battery_units
    battery_power = specs['power_kw'] * battery_units
    battery_peak = specs['peak_kw'] * battery_units

    # Debug Input Values
    print(f"Monthly Bill: {monthly_bill}")
    print(f"Provider: {provider}")
    print(f"Battery Type: {battery_type}")
    print(f"Battery Units: {battery_units}")
    print(f"Rates: {rates}")

    # Determine daily usage
    try:
        daily_bill = monthly_bill / 30
        daily_kwh = daily_bill / avg_rate if avg_rate != 0 else 0
        peak_kwh = daily_kwh * 0.3
        off_peak_kwh = daily_kwh * 0.7
    except ZeroDivisionError:
        st.error("Error: Division by zero in usage calculation. Check input values.")
        return (0, 0, 0, 0, battery_power, battery_peak, battery_storage, 0)

    print(f"Daily Bill: {daily_bill}")
    print(f"Daily kWh: {daily_kwh}")
    print(f"Peak kWh: {peak_kwh}")
    print(f"Off-Peak kWh: {off_peak_kwh}")
