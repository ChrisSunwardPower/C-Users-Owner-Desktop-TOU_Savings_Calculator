import streamlit as st

# Utility Rates
TOU_RATES = {
    'PGE': {'peak_rate': 0.28, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.32, 'off_peak_rate': 0.12}
}

# Fixed Battery Capacity
BATTERY_CAPACITY_KWH = 13.5

# Calculate Savings

def calculate_savings(monthly_bill, provider):
    # Get rates
    rates = TOU_RATES[provider]
    peak_rate = rates['peak_rate']
    off_peak_rate = rates['off_peak_rate']

    # Bill breakdown
    peak_cost = monthly_bill * 0.3
    off_peak_cost = monthly_bill * 0.7

    # Determine kWh for peak usage
    peak_kwh = peak_cost / peak_rate

    # Check for battery coverage
    if peak_kwh > BATTERY_CAPACITY_KWH:
        uncovered_kwh = peak_kwh - BATTERY_CAPACITY_KWH
        st.warning(f"⚡ Battery capacity is insufficient to cover {uncovered_kwh:.2f} kWh of peak usage. These kWh will be billed at the peak rate.")
        covered_kwh = BATTERY_CAPACITY_KWH
    else:
        uncovered_kwh = 0
        covered_kwh = peak_kwh

    # Recalculate peak cost with battery coverage
    # Covered kWh is billed at off-peak, uncovered at peak rate
    new_peak_cost = (covered_kwh * off_peak_rate) + (uncovered_kwh * peak_rate)

    # New bill calculation
    new_bill = off_peak_cost + new_peak_cost

    # Debugging output to verify calculation steps
    print(f"Covered kWh: {covered_kwh}, Uncovered kWh: {uncovered_kwh}")
    print(f"New Peak Cost: {new_peak_cost}")
    print(f"New Bill: {new_bill}")

    # Savings calculation
    savings = monthly_bill - new_bill
    savings = max(0, savings)
