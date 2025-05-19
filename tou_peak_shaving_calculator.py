import streamlit as st

# Utility Rates
TOU_RATES = {
    'PGE': {'peak_rate': 0.28, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.32, 'off_peak_rate': 0.12}
}

# Battery Capacity in kWh
BATTERY_CAPACITY_KWH = 13.5

def calculate_savings(monthly_bill, provider, battery_units):
    rates = TOU_RATES[provider]
    peak_rate = rates['peak_rate']
    off_peak_rate = rates['off_peak_rate']

    # Calculate Peak and Off-Peak Costs
    peak_cost = monthly_bill * 0.3
    off_peak_cost = monthly_bill * 0.7

    # Calculate Peak kWh
    peak_kwh = peak_cost / peak_rate
    total_battery_capacity = battery_units * BATTERY_CAPACITY_KWH

    # Calculate Covered and Uncovered kWh
    covered_kwh = min(peak_kwh, total_battery_capacity)
    uncovered_kwh = max(0, peak_kwh - total_battery_capacity)

    # Calculate Costs
    covered_cost = covered_kwh * off_peak_rate
    uncovered_cost = uncovered_kwh * peak_rate

    # Calculate New Bill
    new_bill = off_peak_cost + covered_cost + uncovered_cost

    # Calculate Savings
    savings = monthly_bill - new_bill

    # Debugging Outputs
    print(f"Monthly Bill: {monthly_bill}")
    print(f"Peak kWh: {peak_kwh}, Covered kWh: {covered_kwh}, Uncovered kWh: {uncovered_kwh}")
    print(f"Covered Cost: {covered_cost}, Uncovered Cost: {uncovered_cost}")
    print(f"New Bill: {new_bill}, Savings: {savings}")

    # Warning for uncovered kWh
    if uncovered_kwh > 0:
        st.warning(f"{uncovered_kwh:.2f} kWh will be billed at the peak rate. Consider adding more batteries.")

    return round(savings, 2), round(savings * 12, 2), round(savings * 120, 2), round(savings * 180, 2)

st.set_page_config(page_title='TOU Savings Calculator', layout='centered')
st.title('TOU Peak Shaving Savings Calculator')

monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=200.0, step=10.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
battery_units = st.selectbox('Number of Batteries', [1, 2, 3, 4, 5])

if st.button('Calculate Savings'):
    savings, annual, ten_year, fifteen_year = calculate_savings(monthly_bill, provider, battery_units)
    st.subheader('Savings Breakdown')
    st.write(f"Monthly: ${savings}, Annual: ${annual}, 10-Year: ${ten_year}, 15-Year: ${fifteen_year}")
