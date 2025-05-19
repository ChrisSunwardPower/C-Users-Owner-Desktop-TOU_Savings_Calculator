import streamlit as st

# Constants
BATTERY_CAPACITY_KWH = 13.5
PEAK_RATE_PGE = 0.19
OFF_PEAK_RATE_PGE = 0.10
PEAK_RATE_PACIFIC = 0.21
OFF_PEAK_RATE_PACIFIC = 0.12

# App Title
st.title('Peak Shaving Savings Calculator')

# User Inputs
bill = st.number_input('Monthly Bill ($)', min_value=0.0, step=10.0, value=200.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
batteries = st.number_input('Number of Batteries', min_value=0, step=1, value=1)

# Determine Rates
if provider == 'PGE':
    peak_rate = PEAK_RATE_PGE
    off_peak_rate = OFF_PEAK_RATE_PGE
else:
    peak_rate = PEAK_RATE_PACIFIC
    off_peak_rate = OFF_PEAK_RATE_PACIFIC

# Calculate Savings
peak_usage = bill * 0.30
off_peak_usage = bill * 0.70
on_peak_kwh = peak_usage / peak_rate
off_peak_kwh = off_peak_usage / off_peak_rate

# Calculate Battery Capacity
battery_capacity = batteries * BATTERY_CAPACITY_KWH
on_peak_kwh -= min(on_peak_kwh, battery_capacity)

# Recalculate Savings
monthly_savings = (on_peak_kwh * peak_rate) - (on_peak_kwh * off_peak_rate)
annual_savings = monthly_savings * 12
ten_year_savings = annual_savings * 10
fifteen_year_savings = annual_savings * 15

# Display Savings
st.subheader('Savings Overview')
st.write(f'Monthly Savings: ${monthly_savings:.2f}')
st.write(f'Annual Savings: ${annual_savings:.2f}')
st.write(f'10-Year Savings: ${ten_year_savings:.2f}')
st.write(f'15-Year Savings: ${fifteen_year_savings:.2f}')
