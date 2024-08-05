import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def fetch_income_statement(symbol):
    stock = yf.Ticker(symbol)  # Corrected the typo here
    income_statement = stock.financials.T
    income_statement.index = pd.to_datetime(income_statement.index)
    income_statement.sort_index(ascending=False, inplace=True)
    return income_statement

def fetch_yearly_income_statement(symbol):
    stock = yf.Ticker(symbol)
    yearly_income_statement = stock.financials.T.groupby(stock.financials.columns.year).sum()
    return yearly_income_statement

def fetch_yearly_balance_sheet(symbol):
    stock = yf.Ticker(symbol)
    yearly_balance_sheet = stock.balance_sheet.T.groupby(stock.balance_sheet.columns.year).sum()
    return yearly_balance_sheet

def compare_income_statements(current_quarter, previous_quarter):
    change_percentage = ((current_quarter - previous_quarter) / previous_quarter.replace(0, pd.NA)) * 100
    change_percentage.fillna(0, inplace=True)  
    comparison = pd.DataFrame({
        'Current Quarter': current_quarter,
        'Previous Quarter': previous_quarter,
        'Change (%)': change_percentage
    })
    return comparison

st.title("Stock Income Statement and Balance Sheet Comparison")

# Input for stock symbol
stock_symbol = st.text_input("Enter the stock symbol", value='AAPL')

if stock_symbol:
    income_statement = fetch_income_statement(stock_symbol)

    if not income_statement.empty:
        st.subheader(f"Income Statement for {stock_symbol}")
        st.dataframe(income_statement)
        
        # Select the most recent quarters for comparison
        if len(income_statement) >= 2:
            latest_quarter = income_statement.iloc[0]
            previous_quarter = income_statement.iloc[1]
            
            comparison = compare_income_statements(latest_quarter, previous_quarter)
            
            st.subheader(f"Comparison of the latest quarter with the previous quarter for {stock_symbol}")
            st.dataframe(comparison)
            
            # Plotting the growth chart for Total Revenue, Operating Expense, and Net Income
            st.subheader("Growth Chart for Total Revenue, Operating Expense, and Net Income (Quarterly)")
            fig, ax = plt.subplots()
            income_statement[['Total Revenue', 'Operating Expense', 'Net Income']].plot(ax=ax, kind='bar')
            plt.xticks(rotation=45)
            plt.ylabel('Amount')
            plt.title(f"Growth Chart for {stock_symbol}")
            st.pyplot(fig)
        else:
            st.warning("Not enough data to compare quarters.")

        # Fetch and display yearly income statement data
        st.subheader(f"Yearly Income Statement for {stock_symbol}")
        yearly_income_statement = fetch_yearly_income_statement(stock_symbol)
        st.dataframe(yearly_income_statement)
        
        st.subheader("Yearly Income Statement Parameters")
        fig, ax = plt.subplots()
        yearly_income_statement[['Total Revenue', 'Net Income']].plot(ax=ax, kind='bar')
        plt.xticks(rotation=45)
        plt.ylabel('Amount')
        plt.title(f"Yearly Income Statement for {stock_symbol}")
        st.pyplot(fig)

        # Fetch and display yearly balance sheet data
        st.subheader(f"Yearly Balance Sheet for {stock_symbol}")
        yearly_balance_sheet = fetch_yearly_balance_sheet(stock_symbol)
        st.dataframe(yearly_balance_sheet)
        
        st.subheader("Yearly Balance Sheet Parameters")
        fig, ax = plt.subplots()
        yearly_balance_sheet[['Total Assets', 'Total Liabilities']].plot(ax=ax, kind='bar')
        plt.xticks(rotation=45)
        plt.ylabel('Amount')
        plt.title(f"Yearly Balance Sheet for {stock_symbol}")
        st.pyplot(fig)
    else:
        st.warning(f"No income statement data found for {stock_symbol}")
else:
    st.info("Please enter a stock symbol to start the comparison.")
