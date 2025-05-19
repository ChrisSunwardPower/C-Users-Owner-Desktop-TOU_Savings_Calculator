import streamlit as st

# Standardized TOU rates
TOU_RATES = {
    'PGE': {'peak_rate': 0.28, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.32, 'off_peak_rate': 0.12}
}

# Battery Specifications
BATTERY_SPECS = {
    'FranklinWH aPower 2': {'storage_kwh': 15, 'power_kw': 10, 'peak_kw': 15},
    'Tesla Powerwall 2': {'storage_kwh': 13.5, 'power_kw': 5, 'peak_kw': 7}
}

# Function to calculate max bill for battery coverage
def max_bill_for_battery(power_kw, avg_rate):
    daily_kwh = power_kw / 0.3  # Assuming 30% of usage during peak hours
    daily_bill = daily_kwh * avg_rate
    return round(daily_bill * 30, 2)

# Function to calculate savings
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

    # Max bill the battery can cover
    max_bill = max_bill_for_battery(battery_power, avg_rate)

    # Calculate usage
    daily_bill = monthly_bill / 30
    daily_kwh = daily_bill / avg_rate
    peak_kwh = daily_kwh * 0.3
    off_peak_kwh = daily_kwh * 0.7

    # Determine battery coverage
    battery_coverage_kwh = min(battery_storage, peak_kwh)
    remaining_peak_kwh = max(0, peak_kwh - battery_coverage_kwh)

    # Costs without battery
    cost_without_battery = (peak_kwh * peak_rate) + (off_peak_kwh * off_peak_rate)

    # Costs with battery
        # Adjust for partial peak coverage
    if battery_coverage_kwh < peak_kwh:
        # Portion covered by battery at off-peak rate
        covered_kwh = battery_coverage_kwh
        remaining_peak_kwh = peak_kwh - covered_kwh
        
        # Cost with battery
        cost_with_battery = (remaining_peak_kwh * peak_rate) + (off_peak_kwh * off_peak_rate) + (covered_kwh * off_peak_rate)

        # Display warning
        st.warning("Battery capacity insufficient to fully cover peak usage. Remaining peak usage billed at peak rate.")
    else:
        # Full coverage by battery
        cost_with_battery = (remaining_peak_kwh * peak_rate) + (off_peak_kwh * off_peak_rate) + (battery_coverage_kwh * off_peak_rate)

    # Calculate savings
    daily_savings = cost_without_battery - cost_with_battery
    monthly_savings = daily_savings * 30
