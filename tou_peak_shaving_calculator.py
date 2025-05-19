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

    # Adjust savings for uncovered peak usage
    uncovered_cost = remaining_peak_kwh * peak_rate
    adjusted_monthly_savings = (cost_without_battery - cost_with_battery) - uncovered_cost

    # Ensure savings do not go negative
    adjusted_monthly_savings = max(0, adjusted_monthly_savings)

    # Propagate to annual, 10-year, and 15-year savings
    yearly_savings = adjusted_monthly_savings * 12
    ten_year_savings = yearly_savings * 10
    fifteen_year_savings = yearly_savings * 15

    return (
        round(adjusted_monthly_savings, 2),
        round(yearly_savings, 2),
        round(ten_year_savings, 2),
        round(fifteen_year_savings, 2),
        battery_power,
        battery_peak,
        battery_storage,
        remaining_peak_kwh
    )
