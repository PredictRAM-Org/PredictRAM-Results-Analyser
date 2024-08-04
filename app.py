import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Load the data from the Excel file
@st.cache
def load_data(file):
    return pd.read_excel(file, sheet_name=None)

data = load_data('all_stocks_data.xlsx')

# Sidebar for selecting a stock symbol
st.sidebar.title("Select Stock Symbol")
symbols = list(data.keys())
selected_symbol = st.sidebar.selectbox("Symbol", symbols)

# Display the selected stock symbol
st.title(f"Financial Data for {selected_symbol}")

# Extracting the relevant sections for the selected symbol
stock_data = data[selected_symbol]
industry = stock_data.get('industry')
income_statement_quarterly = stock_data.get('Income Statement (Quarterly)')
income_statement_annual = stock_data.get('Income Statement (Annual)')
balance_sheet_quarterly = stock_data.get('Balance Sheet (Quarterly)')
balance_sheet_annual = stock_data.get('Balance Sheet (Annual)')

# Display industry information
st.header("Industry")
st.write(industry)

# Function to display financial data
def display_financial_data(title, financial_data):
    st.header(title)
    for date, values in financial_data.items():
        st.subheader(date.strftime('%Y-%m-%d'))
        st.json(values)

# Display Income Statement (Quarterly)
if income_statement_quarterly:
    display_financial_data("Income Statement (Quarterly)", income_statement_quarterly)

# Display Income Statement (Annual)
if income_statement_annual:
    display_financial_data("Income Statement (Annual)", income_statement_annual)

# Display Balance Sheet (Quarterly)
if balance_sheet_quarterly:
    display_financial_data("Balance Sheet (Quarterly)", balance_sheet_quarterly)

# Display Balance Sheet (Annual)
if balance_sheet_annual:
    display_financial_data("Balance Sheet (Annual)", balance_sheet_annual)

# Run the Streamlit app
if __name__ == "__main__":
    st.run()
