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

def calculate_savings(monthly_bill, provider, battery_type, battery_units):
    # Get rates
    rates = TOU_RATES[provider]
    peak_rate = rates['peak_rate']
    off_peak_rate = rates['off_peak_rate']

    # Debug output
    print(f"Monthly Bill: {monthly_bill}")

    # Bill breakdown
    peak_cost = monthly_bill * 0.3
    off_peak_cost = monthly_bill * 0.7
    print(f"Peak Cost: {peak_cost}, Off-Peak Cost: {off_peak_cost}")

    # Determine kWh for peak and off-peak
    peak_kwh = peak_cost / peak_rate
    off_peak_kwh = off_peak_cost / off_peak_rate
    print(f"Peak kWh: {peak_kwh}, Off-Peak kWh: {off_peak_kwh}")

    # Get battery specs
    battery = BATTERY_SPECS[battery_type]
    battery_storage = battery['storage_kwh'] * battery_units
    print(f"Battery Storage: {battery_storage} kWh")

    # Rebill peak usage
    if battery_storage >= peak_kwh:
        # Full coverage: Rebill peak at off-peak rate
        new_peak_cost = peak_kwh * off_peak_rate
        remaining_peak_kwh = 0
    else:
        # Partial coverage
        covered_kwh = battery_storage
        uncovered_kwh = peak_kwh - covered_kwh
        new_peak_cost = (covered_kwh * off_peak_rate) + (uncovered_kwh * peak_rate)
        remaining_peak_kwh = uncovered_kwh

    print(f"Rebilled Peak Cost: {new_peak_cost}")

    # New bill calculation
    new_bill = (off_peak_kwh * off_peak_rate) + new_peak_cost
    print(f"New Bill: {new_bill}")

    # Calculate savings
    savings = monthly_bill - new_bill
    savings = max(0, savings)
    print(f"Monthly Savings: {savings}")

    # Annual, 10-year, and 15-year savings
    annual_savings = savings * 12
    ten_year_savings = annual_savings * 10
    fifteen_year_savings = annual_savings * 15

    return round(savings, 2), round(annual_savings, 2), round(ten_year_savings, 2), round(fifteen_year_savings, 2), remaining_peak_kwh

# Streamlit UI
st.set_page_config(page_title='TOU Peak Shaving Calculator', layout='centered')
st.title('Time of Use (TOU) Peak Shaving Savings Calculator')

# Input Section
st.header('Enter Your Information')
monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=200.0, step=10.0, key='monthly_bill_input')
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'], key='provider_input')
battery_type = st.selectbox('Select Battery Type', ['FranklinWH aPower 2', 'Tesla Powerwall 2'], key='battery_type_input')
battery_units = st.selectbox('Number of Batteries', [1, 2, 3, 4, 5], key='battery_units_input')

# Calculate Savings
if st.button('Calculate Savings', key='calculate_button'):
    savings, annual_savings, ten_year_savings, fifteen_year_savings, remaining_peak_kwh = calculate_savings(
        monthly_bill, provider, battery_type, battery_units)

    # Output Section
    st.subheader('Savings Breakdown')
    st.write(f"Monthly Savings: ${savings}")
    st.write(f"Annual Savings: ${annual_savings}")
    st.write(f"10-Year Savings: ${ten_year_savings}")
    st.write(f"15-Year Savings: ${fifteen_year_savings}")

    # Warning for uncovered peak usage
    if remaining_peak_kwh > 0:
        st.warning(f"⚡ Battery capacity is insufficient to cover {remaining_peak_kwh} kWh of peak usage, which will be billed at the peak rate.")
else:
    st.info('Enter your information and click "Calculate Savings" to see the results.')
