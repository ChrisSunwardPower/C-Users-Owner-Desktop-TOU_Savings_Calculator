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

# Savings Calculation
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

    # Determine daily usage
    daily_bill = monthly_bill / 30
    daily_kwh = daily_bill / avg_rate
    peak_kwh = daily_kwh * 0.3
    off_peak_kwh = daily_kwh * 0.7

    # Calculate battery coverage
    battery_coverage_kwh = min(battery_storage, peak_kwh)
    remaining_peak_kwh = max(0, peak_kwh - battery_coverage_kwh)

    # Costs without battery
    cost_without_battery = (peak_kwh * peak_rate) + (off_peak_kwh * off_peak_rate)

    # Costs with battery
    battery_covered_cost = battery_coverage_kwh * off_peak_rate
    uncovered_peak_cost = remaining_peak_kwh * peak_rate
    off_peak_cost = off_peak_kwh * off_peak_rate

    cost_with_battery = battery_covered_cost + uncovered_peak_cost + off_peak_cost

    # Calculate savings
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
        battery_power,
        battery_peak,
        battery_storage,
        remaining_peak_kwh,
        cost_with_battery
    )

# Streamlit UI
st.set_page_config(page_title='Time of Use Peak Shaving Savings Calculator', layout='centered')
st.title('Time of Use (TOU) Peak Shaving Savings Calculator')

st.header('Input Parameters')
monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=200.0, step=10.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
battery_type = st.selectbox('Select Battery Type', ['FranklinWH aPower 2', 'Tesla Powerwall 2'])
battery_units = st.selectbox('Number of Batteries', [1, 2, 3, 4, 5])

if st.button('Calculate Savings'):
    monthly_savings, yearly_savings, ten_year_savings, fifteen_year_savings, battery_power, battery_peak, battery_storage, remaining_peak_kwh, cost_with_battery = calculate_savings(
        monthly_bill, provider, battery_type, battery_units)

    st.success(f"Monthly Savings: ${monthly_savings}")
    st.success(f"Yearly Savings: ${yearly_savings}")
    st.success(f"10-Year Savings: ${ten_year_savings}")
    st.success(f"15-Year Savings: ${fifteen_year_savings}")

    st.info(f"Battery Specs - {battery_type}: {battery_power} kW continuous, {battery_peak} kW peak, {battery_storage} kWh storage")

    if remaining_peak_kwh > 0:
        st.warning(f"⚡ Battery capacity is insufficient to cover {round(remaining_peak_kwh, 2)} kWh of peak usage, which will be billed at the peak rate.")
        st.info(f"Cost with battery (including uncovered peak usage): ${round(cost_with_battery, 2)}")
else:
    st.info('Enter values and click "Calculate Savings" to see the result.')

st.write('Developed to help customers assess the financial benefits of peak load shaving using battery storage.')
