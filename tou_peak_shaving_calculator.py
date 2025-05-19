import streamlit as st

# User Inputs
monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=260.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
batteries = st.number_input('Number of Batteries', min_value=1, value=1)

# Rates for PGE and Pacific Power
rates = {
    'PGE': {'peak_rate': 0.35, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.33, 'off_peak_rate': 0.09}
}

selected_rates = rates[provider]
peak_rate = selected_rates['peak_rate']
off_peak_rate = selected_rates['off_peak_rate']

# Battery Capacity
battery_capacity = 13.5  # kWh per battery

def calculate_savings(monthly_bill, peak_rate, off_peak_rate, batteries):
    # Calculate Peak and Off-Peak Usage
    peak_usage_kwh = (monthly_bill * 0.3) / peak_rate
    off_peak_usage_kwh = (monthly_bill * 0.7) / off_peak_rate

    # Battery Coverage
    max_off_peak_coverage = batteries * battery_capacity
    peak_covered_kwh = min(peak_usage_kwh, max_off_peak_coverage)
    remaining_peak_kwh = peak_usage_kwh - peak_covered_kwh

    # Recalculate based on battery coverage
    total_off_peak_kwh = off_peak_usage_kwh + peak_covered_kwh
    total_billable_kwh = total_off_peak_kwh + remaining_peak_kwh
    off_peak_bill = total_off_peak_kwh * off_peak_rate
    peak_bill = remaining_peak_kwh * peak_rate

    # Calculate Savings
    total_bill = peak_bill + off_peak_bill
    savings = monthly_bill - total_bill

    return savings, savings * 12, savings * 120, savings * 180

monthly_savings, annual_savings, ten_year_savings, fifteen_year_savings = calculate_savings(monthly_bill, peak_rate, off_peak_rate, batteries)

# Display Savings
st.write(f"Peak Rate: ${peak_rate}/kWh, Off-Peak Rate: ${off_peak_rate}/kWh")
st.subheader("Savings Breakdown")
st.write(f"Monthly Savings: ${monthly_savings:.2f}")
st.write(f"Annual Savings: ${annual_savings:.2f}")
st.write(f"10-Year Savings: ${ten_year_savings:.2f}")
st.write(f"15-Year Savings: ${fifteen_year_savings:.2f}")
