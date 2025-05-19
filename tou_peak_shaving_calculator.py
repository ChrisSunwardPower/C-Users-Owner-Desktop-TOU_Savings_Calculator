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

    # Bill breakdown
    peak_cost = monthly_bill * 0.3
    off_peak_cost = monthly_bill * 0.7

    # Determine kWh for peak usage
    peak_kwh = peak_cost / peak_rate
    off_peak_kwh = off_peak_cost / off_peak_rate

    # Get battery specs
    battery = BATTERY_SPECS[battery_type]
    battery_storage = battery['storage_kwh'] * battery_units

    # Check battery coverage
    if battery_storage >= peak_kwh:
        # Battery fully covers peak usage, rebill at off-peak rate
        new_peak_cost = peak_kwh * off_peak_rate
        remaining_peak_kwh = 0  # All peak usage is covered
    else:
        # Partial coverage: Battery covers only part of peak usage
        covered_kwh = battery_storage
        uncovered_kwh = peak_kwh - covered_kwh
        new_peak_cost = (covered_kwh * off_peak_rate) + (uncovered_kwh * peak_rate)
        remaining_peak_kwh = uncovered_kwh

    # New bill calculation
    new_bill = (off_peak_kwh * off_peak_rate) + new_peak_cost

    # Calculate savings
    savings = monthly_bill - new_bill
    savings = max(0, savings)

    # Annual, 10-year, and 15-year savings
    annual_savings = savings * 12
    ten_year_savings = annual_savings * 10
    fifteen_year_savings = annual_savings * 15

    return round(savings, 2), round(annual_savings, 2), round(ten_year_savings, 2), round(fifteen_year_savings, 2), remaining_peak_kwh
