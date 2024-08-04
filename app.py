import pandas as pd
import streamlit as st
import os

# Function to load data from an Excel file
def load_data('all_stocks_data.xlsx'):
    try:
        return pd.read_excel(file_path, sheet_name=None)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to get stock data from the Excel sheet
def get_stock_data(data, stock_symbol):
    return data.get(stock_symbol)

# Function to calculate percentage change
def calculate_percentage_change(current, previous):
    return ((current - previous) / previous) * 100 if previous != 0 else float('inf')

# Function to display comparative analysis
def display_comparative_analysis(stock_data, stock_symbol):
    st.write(f"### Comparative Analysis for {stock_symbol}")

    industry = stock_data.get('Industry')
    st.write(f"**Industry:** {industry}")

    income_statement_quarterly = stock_data.get('Income Statement (Quarterly)')
    income_statement_annual = stock_data.get('Income Statement (Annual)')

    # Get the last quarter and last year data
    last_quarter = income_statement_quarterly.iloc[-1]
    last_year_quarter = income_statement_quarterly.iloc[-5]  # Assuming quarterly data is available for 5 quarters
    last_year = income_statement_annual.iloc[-1]

    st.write("#### Income Statement (Quarterly) Comparison")
    for key in last_quarter.keys():
        current_value = last_quarter[key]
        previous_value = last_year_quarter[key]
        change = calculate_percentage_change(current_value, previous_value)
        st.write(f"{key}: {current_value} (Change: {change:.2f}%)")

    st.write("#### Income Statement (Annual) Comparison")
    for key in last_quarter.keys():
        current_value = last_quarter[key]
        previous_value = last_year[key]
        change = calculate_percentage_change(current_value, previous_value)
        st.write(f"{key}: {current_value} (Change: {change:.2f}%)")

# Main function to run the Streamlit app
def main():
    st.title("Stock Comparative Analysis")

    # Check if the file exists
    file_path = 'all_stocks_data.xlsx'
    if not os.path.exists(file_path):
        st.error(f"The file {file_path} does not exist.")
        return

    # Load the data
    data = load_data(file_path)
    if data is None:
        return

    # Select a stock
    stock_symbol = st.selectbox("Select a Stock", options=list(data.keys()))

    # Get the stock data
    stock_data = get_stock_data(data, stock_symbol)

    # Display comparative analysis
    if stock_data is not None:
        display_comparative_analysis(stock_data, stock_symbol)
    else:
        st.write("No data available for the selected stock.")

if __name__ == "__main__":
    main()
