import streamlit as st

# Constants
BATTERY_CAPACITY_KWH = 13.5
PGE_PEAK_RATE = 0.4389
PGE_OFF_PEAK_RATE = 0.0908
PACIFIC_PEAK_RATE = 0.12
PACIFIC_OFF_PEAK_RATE = 0.07

# App Title
st.title('Peak Shaving Savings Calculator')

# User Inputs
bill = st.number_input('Monthly Bill ($)', min_value=0.0, step=10.0, value=200.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])

# Determine Rates
if provider == 'PGE':
    peak_rate = PGE_PEAK_RATE
    off_peak_rate = PGE_OFF_PEAK_RATE
else:
    peak_rate = PACIFIC_PEAK_RATE
    off_peak_rate = PACIFIC_OFF_PEAK_RATE

# Calculate Peak and Off-Peak Usage
peak_cost = bill * 0.30
off_peak_cost = bill * 0.70

# Calculate On-Peak kWh
on_peak_kwh = peak_cost / peak_rate

# Battery Capacity Calculation
monthly_battery_capacity = BATTERY_CAPACITY_KWH * 30

# Check if Battery Can Offset All Peak Usage
uncovered_kwh = 0
uncovered_cost = 0

if on_peak_kwh > monthly_battery_capacity:
    uncovered_kwh = on_peak_kwh - monthly_battery_capacity
    uncovered_cost = uncovered_kwh * peak_rate
    st.warning(f"Warning: Peak usage of {on_peak_kwh:.2f} kWh exceeds battery capacity of {monthly_battery_capacity} kWh. The battery can only offset up to {monthly_battery_capacity} kWh, leaving {uncovered_kwh:.2f} kWh uncovered and billed at the peak rate.")

# Calculate Total kWh as Off-Peak
adjusted_on_peak_kwh = min(on_peak_kwh, monthly_battery_capacity)
total_kwh = adjusted_on_peak_kwh + (off_peak_cost / off_peak_rate)

# New Bill Calculation
new_bill = (total_kwh * off_peak_rate) + uncovered_cost

# Calculate Savings
monthly_savings = bill - new_bill
annual_savings = monthly_savings * 12
ten_year_savings = annual_savings * 10
fifteen_year_savings = annual_savings * 15

# Display Savings
st.subheader('Savings Overview')
st.write(f'Monthly Savings: ${monthly_savings:.2f}')
st.write(f'Annual Savings: ${annual_savings:.2f}')
st.write(f'10-Year Savings: ${ten_year_savings:.2f}')
st.write(f'15-Year Savings: ${fifteen_year_savings:.2f}')
