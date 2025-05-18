import streamlit as st

# Standardized TOU rates
TOU_RATES = {
    'PGE': {'peak_rate': 0.28, 'off_peak_rate': 0.10},
    'Pacific Power': {'peak_rate': 0.32, 'off_peak_rate': 0.12}
}

# Battery kWh per unit
BATTERY_KWH_PER_UNIT = 15

# Function to calculate max bill for battery coverage
def max_bill_for_battery(battery_capacity, avg_rate):
    # Peak kWh that the battery setup can cover
    peak_kwh = battery_capacity
    # Total daily kWh usage that corresponds to the peak usage
    daily_kwh = peak_kwh / 0.3
    # Daily bill in dollars
    daily_bill = daily_kwh * avg_rate
    # Monthly bill
    monthly_bill = daily_bill * 30
    return round(monthly_bill, 2)

# Function to calculate savings
def calculate_savings(monthly_bill, provider, battery_units):
    rates = TOU_RATES[provider]
    peak_rate = rates['peak_rate']
    off_peak_rate = rates['off_peak_rate']
    avg_rate = (peak_rate * 0.3) + (off_peak_rate * 0.7)

    # Battery Capacity in kWh
    battery_capacity = battery_units * BATTERY_KWH_PER_UNIT

    # Calculate max bill for battery coverage
    max_bill = max_bill_for_battery(battery_capacity, avg_rate)

    # Assuming 30% of usage during peak hours
    peak_percentage = 30 / 100

    # Daily Bill Calculation
    daily_bill = monthly_bill / 30

    # Estimate Daily kWh Usage
    daily_kwh = daily_bill / avg_rate

    # kWh Usage During Peak and Off-Peak Hours
    peak_kwh = daily_kwh * peak_percentage
    off_peak_kwh = daily_kwh * (1 - peak_percentage)

    # Battery Coverage
    battery_coverage_kwh = min(battery_capacity, peak_kwh)
    remaining_peak_kwh = max(0, peak_kwh - battery_coverage_kwh)

    # Cost Without Battery
    cost_without_battery = (peak_kwh * peak_rate) + (off_peak_kwh * off_peak_rate)

    # Cost With Battery
    cost_with_battery = (remaining_peak_kwh * peak_rate) + (off_peak_kwh * off_peak_rate) + (battery_coverage_kwh * off_peak_rate)

    # Daily Savings
    daily_savings = cost_without_battery - cost_with_battery

    # Monthly, Yearly, 10-Year, and 15-Year Savings
    monthly_savings = daily_savings * 30
    yearly_savings = monthly_savings * 12
    ten_year_savings = yearly_savings * 10
    fifteen_year_savings = yearly_savings * 15

    return (
        round(monthly_savings, 2),
        round(yearly_savings, 2),
        round(ten_year_savings, 2),
        round(fifteen_year_savings, 2),
        round(max_bill, 2)
    )

# Streamlit UI
st.set_page_config(page_title='TOU Peak Shaving Savings Calculator', layout='centered')
st.title('TOU Peak Shaving Savings Calculator')
st.write('Calculate potential savings by using a battery system to shift peak usage to off-peak hours.')

# Input fields
st.sidebar.header('Input Parameters')
monthly_bill = st.sidebar.number_input('Monthly Bill ($)', min_value=0.0, value=200.0)
provider = st.sidebar.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
battery_units = st.sidebar.selectbox('Number of Batteries (1 Battery = 15 kWh)', [1, 2, 3, 4, 5])

# Calculate button
if st.sidebar.button('Calculate Savings'):
    monthly_savings, yearly_savings, ten_year_savings, fifteen_year_savings, max_bill = calculate_savings(monthly_bill, provider, battery_units)

    total_battery_kwh = battery_units * BATTERY_KWH_PER_UNIT
    st.success(f"Monthly Savings: ${monthly_savings}")
    st.success(f"Yearly Savings: ${yearly_savings}")
    st.success(f"10-Year Savings: ${ten_year_savings}")
    st.success(f"15-Year Savings: ${fifteen_year_savings}")
    st.info(f"Total Battery Capacity: {total_battery_kwh} kWh")

    # Display Alert if Bill Exceeds Battery Coverage
    if monthly_bill > max_bill:
        st.warning(f"⚡ Warning: Your bill exceeds the coverage capacity of {battery_units} battery/batteries ({total_battery_kwh} kWh). You may need additional batteries to fully offset peak usage.")
    else:
        st.success(f"Your current bill is within the coverage capacity of {battery_units} battery/batteries ({total_battery_kwh} kWh).")

else:
    st.info('Enter the values and click "Calculate Savings" to see the result.')

# Footer
st.write('Developed to help customers assess the financial benefits of peak load shaving using battery storage.')
