import streamlit as st

# User Inputs
monthly_bill = st.number_input('Monthly Bill ($)', min_value=0.0, value=260.0)
provider = st.selectbox('Select Utility Provider', ['PGE', 'Pacific Power'])
batteries = st.number_input('Number of Batteries', min_value=1, value=1)

# Assumptions (Standardized for Oregon)
peak_rate = 0.35  # $/kWh
off_peak_rate = 0.10  # $/kWh

# Calculate Peak Shaving
peak_usage_kwh = 265.07  # Example peak usage in kWh
peak_savings = peak_usage_kwh * (peak_rate - off_peak_rate)
monthly_savings = peak_savings / batteries
annual_savings = monthly_savings * 12

ten_year_savings = annual_savings * 10
fifteen_year_savings = annual_savings * 15

# Display Savings
st.write(f"{peak_usage_kwh} kWh will be billed at the peak rate. Consider adding more batteries.")
st.subheader("Savings Breakdown")
st.write(f"Monthly: ${monthly_savings:.2f}")
st.write(f"Annual: ${annual_savings:.2f}")
st.write(f"10-Year: ${ten_year_savings:.2f}")
st.write(f"15-Year: ${fifteen_year_savings:.2f}")
