import pandas as pd
import streamlit as st
import json
from datetime import datetime

# Function to load data
def load_data(filename):
    return pd.read_excel(filename, sheet_name=None)

# Function to calculate the percentage change
def calculate_percentage_change(old_value, new_value):
    if old_value == 0:
        return float('inf') if new_value != 0 else 0
    return ((new_value - old_value) / old_value) * 100

# Load data
data = load_data('all_stocks_data.xlsx')

# Extract the relevant sheets
stock_data = data.get('Stock Data')  # Replace with the actual sheet name if different

# Streamlit UI
st.title('Stock Comparative Analysis')

# Select stock
stock_symbols = stock_data['symbol'].unique()
selected_stock = st.selectbox('Select a stock', stock_symbols)

# Filter data for the selected stock
selected_data = stock_data[stock_data['symbol'] == selected_stock].iloc[0]
industry = selected_data['industry']
st.write(f'Industry: {industry}')

# Extract Income Statement data
income_statement_quarterly = json.loads(selected_data['Income Statement (Quarterly)'])
income_statement_annual = json.loads(selected_data['Income Statement (Annual)'])

# Convert timestamps to datetime
def parse_data(data):
    parsed_data = {}
    for date_str, metrics in data.items():
        date = pd.to_datetime(date_str)
        parsed_data[date] = metrics
    return parsed_data

income_statement_quarterly = parse_data(income_statement_quarterly)
income_statement_annual = parse_data(income_statement_annual)

# Get the latest and previous periods for comparison
def get_latest_and_previous(data):
    dates = sorted(data.keys())
    if len(dates) < 2:
        return None, None
    latest = dates[-1]
    previous = dates[-2]
    return data[latest], data[previous]

latest_quarterly, previous_quarterly = get_latest_and_previous(income_statement_quarterly)
latest_annual, previous_annual = get_latest_and_previous(income_statement_annual)

# Display comparative analysis
def display_comparative_analysis(latest, previous, period):
    if latest and previous:
        st.subheader(f'Comparative Analysis - {period}')
        for key in latest.keys():
            latest_value = latest.get(key, 'N/A')
            previous_value = previous.get(key, 'N/A')
            if isinstance(latest_value, (int, float)) and isinstance(previous_value, (int, float)):
                change = calculate_percentage_change(previous_value, latest_value)
                st.write(f'{key}: {latest_value} (Change: {change:.2f}%)')
            else:
                st.write(f'{key}: {latest_value} (No previous data)')

st.subheader('Quarterly Income Statement Comparison')
display_comparative_analysis(latest_quarterly, previous_quarterly, 'Quarterly Income Statement')

st.subheader('Annual Income Statement Comparison')
display_comparative_analysis(latest_annual, previous_annual, 'Annual Income Statement')

