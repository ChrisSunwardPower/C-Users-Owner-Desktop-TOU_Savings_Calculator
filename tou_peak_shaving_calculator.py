import streamlit as st

# Rates for PGE and Pacific Power
rates = {
    'PGE': {'peak_rate': 0.35, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.33, 'off_peak_rate': 0.09}
}

# Battery Capacity
battery_capacity = 13.5  # kWh per battery

# User Inputs
monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=260.0)
if st.button('Increase Bill by 10%'):
    monthly_bill *= 1.1
if st.button('Decrease Bill by 10%'):
    monthly_bill *= 0.9

provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
batteries = st.number_input('Number of Batteries', min_value=1, value=1)

selected_rates = rates[provider]
peak_rate = selected_rates['peak_rate']
off_peak_rate = selected_rates['off_peak_rate']

# Calculation Function

def calculate_savings(monthly_bill, peak_rate, off_peak_rate, batteries):
    # Determine kWhs during Peak and Off-Peak Hours
    peak_bill_amount = monthly_bill * 0.3
    off_peak_bill_amount = monthly_bill * 0.7

    # Calculate kWh for Peak and Off-Peak
    peak_kwh = peak_bill_amount / peak_rate
    off_peak_kwh = off_peak_bill_amount / off_peak_rate

    # Determine Battery Coverage
    max_battery_coverage = batteries * battery_capacity
    peak_kwh_covered = min(peak_kwh, max_battery_coverage)
    peak_kwh_remaining = max(0, peak_kwh - peak_kwh_covered)

    # Calculate Adjusted Bill
    adjusted_off_peak_kwh = off_peak_kwh + peak_kwh_covered
    adjusted_peak_kwh = peak_kwh_remaining
    adjusted_off_peak_bill = adjusted_off_peak_kwh * off_peak_rate
    adjusted_peak_bill = adjusted_peak_kwh * peak_rate
    adjusted_total_bill = adjusted_off_peak_bill + adjusted_peak_bill

    # Calculate Savings
    savings = monthly_bill - adjusted_total_bill

    return savings, savings * 12, savings * 120, savings * 180

# Calculate Savings
monthly_savings, annual_savings, ten_year_savings, fifteen_year_savings = calculate_savings(monthly_bill, peak_rate, off_peak_rate, batteries)

# Display Results
st.subheader("TOU Peak Shaving Savings Calculator")
st.write(f"Monthly Bill: ${monthly_bill:.2f}")
st.write(f"Provider: {provider}")
st.write(f"Batteries: {batteries}")

st.subheader("Savings")
st.write(f"Monthly Savings: ${monthly_savings:.2f}")
st.write(f"Annual Savings: ${annual_savings:.2f}")
st.write(f"10-Year Savings: ${ten_year_savings:.2f}")
st.write(f"15-Year Savings: ${fifteen_year_savings:.2f}")
