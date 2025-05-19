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
    print(f"Peak kWh: {peak_kwh}")  # Debug

    # Calculate new peak cost
    # Covered kWh is billed at off-peak, uncovered at peak rate
    if peak_kwh <= BATTERY_CAPACITY_KWH:
        new_peak_cost = peak_kwh * off_peak_rate
        uncovered_kwh = 0
    else:
        covered_kwh = BATTERY_CAPACITY_KWH
        uncovered_kwh = peak_kwh - BATTERY_CAPACITY_KWH
        new_peak_cost = (covered_kwh * off_peak_rate) + (uncovered_kwh * peak_rate)

    # New bill calculation
    new_bill = off_peak_cost + new_peak_cost

    # Savings calculation
    savings = monthly_bill - new_bill
    savings = max(0, savings)

    # Battery coverage warning (moved to end for clarity)
    if uncovered_kwh > 0:
        st.warning(f"⚡ Battery capacity is insufficient to cover {uncovered_kwh:.2f} kWh of peak usage. These kWh will be billed at the peak rate.")
