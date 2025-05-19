import streamlit as st

# Utility Rates
TOU_RATES = {
    'PGE': {'peak_rate': 0.28, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.32, 'off_peak_rate': 0.12}
}

# Battery Specifications
BATTERY_CAPACITY_KWH = 13.5

# Calculate Savings

def calculate_savings(monthly_bill, provider, battery_units):
    # Get rates
    rates = TOU_RATES[provider]
    peak_rate = rates['peak_rate']
    off_peak_rate = rates['off_peak_rate']

    # Bill breakdown
    peak_cost = monthly_bill * 0.3
    off_peak_cost = monthly_bill * 0.7

    # Determine kWh for peak usage
    peak_kwh = peak_cost / peak_rate

    # Calculate total battery capacity
    total_battery_capacity = battery_units * BATTERY_CAPACITY_KWH

    # Calculate covered and uncovered kWh
    if peak_kwh <= total_battery_capacity:
        covered_kwh = peak_kwh
        uncovered_kwh = 0
    else:
        covered_kwh = total_battery_capacity
        uncovered_kwh = peak_kwh - total_battery_capacity

    # Recalculate peak cost
    new_peak_cost = (covered_kwh * off_peak_rate) + (uncovered_kwh * peak_rate)

    # New bill calculation
    new_bill = off_peak_cost + new_peak_cost

    # Savings calculation
    savings = monthly_bill - new_bill
    savings = max(0, savings)

    # Annual, 10-year, and 15-year savings
    annual_savings = savings * 12
    ten_year_savings = annual_savings * 10
    fifteen_year_savings = annual_savings * 15

    # Battery coverage warning
    if uncovered_kwh > 0:
        st.warning(f"⚡ Battery capacity is insufficient to cover {uncovered_kwh:.2f} kWh of peak usage. These kWh will be billed at the peak rate. Consider adding more batteries.")

    return round(savings, 2), round(annual_savings, 2), round(ten_year_savings, 2), round(fifteen_year_savings, 2)

# Streamlit UI
st.set_page_config(page_title='TOU Peak Shaving Calculator', layout='centered')
st.title('Time of Use (TOU) Peak Shaving Savings Calculator')

# Input Section
st.header('Enter Your Information')
monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=200.0, step=10.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
battery_units = st.selectbox('Number of Batteries', [1, 2, 3, 4, 5])

# Calculate Savings
if st.button('Calculate Savings'):
    savings, annual_savings, ten_year_savings, fifteen_year_savings = calculate_savings(monthly_bill, provider, battery_units)

    # Output Section
    st.subheader('Savings Breakdown')
    st.write(f"Monthly Savings: ${savings}")
    st.write(f"Annual Savings: ${annual_savings}")
    st.write(f"10-Year Savings: ${ten_year_savings}")
    st.write(f"15-Year Savings: ${fifteen_year_savings}")
else:
    st.info('Enter your information and click "Calculate Savings" to see the results.')
