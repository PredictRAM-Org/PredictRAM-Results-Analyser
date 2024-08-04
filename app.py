import streamlit as st
import pandas as pd

# Function to load data from the Excel file
@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path, sheet_name=None)

# Function to perform comparative analysis between two periods
def comparative_analysis(df, column_name):
    last_period = df[column_name].iloc[-1]
    previous_period = df[column_name].iloc[-2]
    
    analysis = (last_period - previous_period) / previous_period * 100
    return last_period, previous_period, analysis

# Load the data
file_path = 'all_stocks_data.xlsx'
data = load_data(file_path)

# Extract the list of stock symbols
stock_symbols = data['Sheet1']['symbol'].unique()

# Streamlit UI
st.title("Stock Comparative Analysis")

# Stock symbol selection
selected_stock = st.selectbox("Select a stock symbol:", stock_symbols)

# Filter data for the selected stock
stock_data = data['Sheet1'][data['Sheet1']['Symbol'] == selected_stock]

if not stock_data.empty:
    industry = stock_data['Industry'].values[0]
    st.write(f"**Industry:** {industry}")

    # Display comparative analysis for Income Statement (Quarterly)
    if 'Income Statement (Quarterly)' in stock_data.columns:
        st.subheader("Income Statement (Quarterly) Comparative Analysis")
        income_statement_quarterly = stock_data['Income Statement (Quarterly)'].iloc[0]

        # Convert string to dictionary
        income_statement_quarterly_dict = eval(income_statement_quarterly)
        df_quarterly = pd.DataFrame.from_dict(income_statement_quarterly_dict, orient='index')

        # Display the last quarter and previous quarter data with analysis
        st.write("### Quarterly Data")
        for column in df_quarterly.columns:
            last_qtr, prev_qtr, analysis_qtr = comparative_analysis(df_quarterly, column)
            st.write(f"{column}: Last Quarter: {last_qtr}, Previous Quarter: {prev_qtr}, Change: {analysis_qtr:.2f}%")

    # Display comparative analysis for Income Statement (Annual)
    if 'Income Statement (Annual)' in stock_data.columns:
        st.subheader("Income Statement (Annual) Comparative Analysis")
        income_statement_annual = stock_data['Income Statement (Annual)'].iloc[0]

        # Convert string to dictionary
        income_statement_annual_dict = eval(income_statement_annual)
        df_annual = pd.DataFrame.from_dict(income_statement_annual_dict, orient='index')

        # Display the last year and previous year data with analysis
        st.write("### Annual Data")
        for column in df_annual.columns:
            last_year, prev_year, analysis_year = comparative_analysis(df_annual, column)
            st.write(f"{column}: Last Year: {last_year}, Previous Year: {prev_year}, Change: {analysis_year:.2f}%")

else:
    st.write("No data available for the selected stock.")
