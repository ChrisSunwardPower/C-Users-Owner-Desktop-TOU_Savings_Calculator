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

# Calculate Savings

def calculate_savings(monthly_bill, provider, battery_type):
    # Get rates
    rates = TOU_RATES[provider]
    peak_rate = rates['peak_rate']
    off_peak_rate = rates['off_peak_rate']

    # Bill breakdown
    peak_cost = monthly_bill * 0.3
    off_peak_cost = monthly_bill * 0.7

    # Determine kWh for peak usage
    peak_kwh = peak_cost / peak_rate

    # Get battery specs
    battery = BATTERY_SPECS[battery_type]
    battery_storage = battery['storage_kwh']  # Single battery capacity in kWh

    # Determine coverage
    if battery_storage >= peak_kwh:
        # Full coverage - Rebill entire peak kWh at off-peak rate
        new_peak_cost = peak_kwh * off_peak_rate
        remaining_peak_kwh = 0
    else:
        # Partial coverage
        covered_kwh = battery_storage
        uncovered_kwh = peak_kwh - covered_kwh
        new_peak_cost = (covered_kwh * off_peak_rate) + (uncovered_kwh * peak_rate)
        remaining_peak_kwh = uncovered_kwh

    # New bill calculation
    new_bill = off_peak_cost + new_peak_cost

    # Calculate Savings and Battery Coverage
    # Determine maximum peak coverage in kWh
    battery_capacity_kwh = 13.5  # Unified capacity for simplicity

    # Check if the battery can fully cover peak usage
    if peak_kwh > battery_capacity_kwh:
        uncovered_kwh = peak_kwh - battery_capacity_kwh
        st.warning(f"⚡ Battery capacity is insufficient to cover {uncovered_kwh:.2f} kWh of peak usage. These kWh will be billed at the peak rate.")
    else:
        uncovered_kwh = 0

    # Recalculate peak cost with battery coverage
    if uncovered_kwh == 0:
        # Fully covered, rebill entire peak at off-peak rate
        new_peak_cost = peak_kwh * off_peak_rate
    else:
        # Partially covered, split billing
        covered_kwh = battery_capacity_kwh
        new_peak_cost = (covered_kwh * off_peak_rate) + (uncovered_kwh * peak_rate)

    # New bill calculation
    new_bill = off_peak_cost + new_peak_cost

    # Savings calculation
    savings = monthly_bill - new_bill
    savings = max(0, savings)
