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
    cost_with_battery = (remaining_peak_kwh * peak_rate) + (off_peak_kwh * off_peak_rate) + (battery_coverage_kwh * off_peak_rate)

    # Savings calculations
    daily_savings = cost_without_battery - cost_with_battery
    monthly_savings = daily_savings * 30
    yearly_savings = monthly_savings * 12
    ten_year_savings = yearly_savings * 10
    fifteen_year_savings = yearly_savings * 15

    return (
        round(monthly_savings, 2),
        round(yearly_savings, 2),
        round(ten_year_savings, 2),
        round(fifteen_year_savings, 2),
        round(max_bill, 2),
        battery_power,
        battery_peak,
        battery_storage
    )

# Streamlit UI
st.set_page_config(page_title='TOU Peak Shaving Savings Calculator', layout='centered')
st.title('Time of Use (TOU) Peak Shaving Savings Calculator')

st.header('Input Parameters')
monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=200.0, step=1.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
battery_type = st.selectbox('Select Battery Type', ['FranklinWH aPower 2', 'Tesla Powerwall 2'])
battery_units = st.selectbox('Number of Batteries', [1, 2, 3, 4, 5])

if st.button('Calculate Savings'):
    monthly_savings, yearly_savings, ten_year_savings, fifteen_year_savings, max_bill, battery_power, battery_peak, battery_storage = calculate_savings(
        monthly_bill, provider, battery_type, battery_units)

    st.success(f"Monthly Savings: ${monthly_savings}")
    st.success(f"Yearly Savings: ${yearly_savings}")
    st.success(f"10-Year Savings: ${ten_year_savings}")
    st.success(f"15-Year Savings: ${fifteen_year_savings}")

    st.info(f"Total Battery Power Output: {battery_power} kW continuous, {battery_peak} kW peak")
    st.info(f"Total Battery Storage Capacity: {battery_storage} kWh")

    if monthly_bill > max_bill:
        st.warning(f"⚡ Warning: Your bill exceeds the battery capacity of {battery_units} {battery_type}(s). Consider adding more batteries to fully offset peak usage.")
else:
    st.info('Enter the values and click "Calculate Savings" to see the result.')

st.write('Developed to help customers assess the financial benefits of peak load shaving using battery storage.')
