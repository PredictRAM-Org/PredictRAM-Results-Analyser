import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch quarterly income statement data
def fetch_quarterly_income_statement(symbol):
    stock = yf.Ticker(symbol)
    quarterly_income_statement = stock.quarterly_financials.T
    quarterly_income_statement.index = pd.to_datetime(quarterly_income_statement.index)
    quarterly_income_statement.sort_index(ascending=False, inplace=True)
    return quarterly_income_statement

# Existing functions and Streamlit code ...

# Streamlit App
st.title("Stock Financials Dashboard")

# Input for stock symbol
stock_symbol = st.text_input("Enter the stock symbol", value='AAPL')

if stock_symbol:
    # Fetch stock data
    stock = yf.Ticker(stock_symbol)

    # Calculate and show risk score
    risk_score = calculate_risk_score(stock)
    st.subheader(f"Risk Meter for {stock_symbol}")
    
    # Normalize risk score for progress bar
    normalized_risk_score = min(max(risk_score / 5, 0), 1)
    
    # Determine risk level
    if risk_score < 1:
        risk_level = 'Low'
        risk_color = 'green'
    elif risk_score < 2:
        risk_level = 'Medium'
        risk_color = 'orange'
    else:
        risk_level = 'High'
        risk_color = 'red'
    
    # Display risk level as a progress bar or metric
    st.metric(label="Risk Score", value=f"{risk_score:.2f}", delta=risk_level)
    st.progress(normalized_risk_score)

    # Fetch income statement
    income_statement = fetch_income_statement(stock_symbol)
    
    if not income_statement.empty:
        # Show the full income statement in a dashboard view
        st.subheader(f"Full Income Statement for {stock_symbol}")
        st.dataframe(income_statement)

        # Allow user to select specific parameters to visualize
        st.subheader("Select Parameters to Visualize (Income Statement)")
        selected_parameters = st.multiselect("Choose parameters:", income_statement.columns.tolist(), default=['Total Revenue', 'Operating Expense', 'Net Income'])
        
        if selected_parameters:
            st.subheader("Income Statement Parameters Visualization")
            fig, ax = plt.subplots()
            income_statement[selected_parameters].plot(ax=ax, kind='line', marker='o')
            plt.xticks(rotation=45)
            plt.ylabel('Amount')
            plt.title(f"Selected Income Statement Parameters for {stock_symbol}")
            st.pyplot(fig)

        # Fetch and show yearly income statement data
        st.subheader(f"Yearly Income Statement for {stock_symbol}")
        yearly_income_statement = fetch_yearly_income_statement(stock_symbol)
        st.dataframe(yearly_income_statement)

        st.subheader("Select Parameters to Visualize (Yearly Income Statement)")
        selected_yearly_parameters = st.multiselect("Choose parameters (Yearly):", yearly_income_statement.columns.tolist(), default=['Total Revenue', 'Operating Expense', 'Net Income'])
        
        if selected_yearly_parameters:
            st.subheader("Yearly Income Statement Visualization")
            fig, ax = plt.subplots()
            yearly_income_statement[selected_yearly_parameters].plot(ax=ax, kind='bar')
            plt.xticks(rotation=45)
            plt.ylabel('Amount')
            plt.title(f"Selected Yearly Income Statement Parameters for {stock_symbol}")
            st.pyplot(fig)

            # Calculate percentage change for selected parameters
            st.subheader("Percentage Change in Yearly Income Statement")
            yearly_income_statement_pct_change = yearly_income_statement[selected_yearly_parameters].pct_change() * 100
            st.dataframe(yearly_income_statement_pct_change)

            st.subheader("Percentage Change in Yearly Income Statement (Chart)")
            fig, ax = plt.subplots()
            yearly_income_statement_pct_change.plot(ax=ax, kind='bar')
            plt.xticks(rotation=45)
            plt.ylabel('Percentage Change')
            plt.title(f"Yearly Income Statement Percentage Change for {stock_symbol}")
            st.pyplot(fig)

        # Fetch and show quarterly income statement data
        st.subheader(f"Quarterly Income Statement for {stock_symbol}")
        quarterly_income_statement = fetch_quarterly_income_statement(stock_symbol)
        st.dataframe(quarterly_income_statement)

        st.subheader("Select Parameters to Visualize (Quarterly Income Statement)")
        selected_quarterly_parameters = st.multiselect("Choose parameters (Quarterly):", quarterly_income_statement.columns.tolist(), default=['Total Revenue', 'Operating Expense', 'Net Income'])
        
        if selected_quarterly_parameters:
            st.subheader("Quarterly Income Statement Visualization")
            fig, ax = plt.subplots()
            quarterly_income_statement[selected_quarterly_parameters].plot(ax=ax, kind='line', marker='o')
            plt.xticks(rotation=45)
            plt.ylabel('Amount')
            plt.title(f"Selected Quarterly Income Statement Parameters for {stock_symbol}")
            st.pyplot(fig)

            # Calculate percentage change for selected parameters
            st.subheader("Percentage Change in Quarterly Income Statement")
            quarterly_income_statement_pct_change = quarterly_income_statement[selected_quarterly_parameters].pct_change() * 100
            st.dataframe(quarterly_income_statement_pct_change)

            st.subheader("Percentage Change in Quarterly Income Statement (Chart)")
            fig, ax = plt.subplots()
            quarterly_income_statement_pct_change.plot(ax=ax, kind='bar')
            plt.xticks(rotation=45)
            plt.ylabel('Percentage Change')
            plt.title(f"Quarterly Income Statement Percentage Change for {stock_symbol}")
            st.pyplot(fig)

        # Fetch and show yearly balance sheet data
        st.subheader(f"Yearly Balance Sheet for {stock_symbol}")
        yearly_balance_sheet = fetch_yearly_balance_sheet(stock_symbol)
        st.dataframe(yearly_balance_sheet)

        # Check if default parameters exist in the DataFrame
        default_balance_sheet_parameters = ['Total Assets', 'Total Liabilities']
        available_balance_sheet_parameters = [param for param in default_balance_sheet_parameters if param in yearly_balance_sheet.columns]

        st.subheader("Select Parameters to Visualize (Yearly Balance Sheet)")
        selected_balance_sheet_parameters = st.multiselect(
            "Choose parameters (Balance Sheet):", 
            yearly_balance_sheet.columns.tolist(), 
            default=available_balance_sheet_parameters
        )
        
        if selected_balance_sheet_parameters:
            st.subheader("Yearly Balance Sheet Visualization")
            fig, ax = plt.subplots()
            yearly_balance_sheet[selected_balance_sheet_parameters].plot(ax=ax, kind='bar')
            plt.xticks(rotation=45)
            plt.ylabel('Amount')
            plt.title(f"Selected Yearly Balance Sheet Parameters for {stock_symbol}")
            st.pyplot(fig)
    else:
        st.warning(f"No income statement data found for {stock_symbol}")
else:
    st.info("Please enter a stock symbol to start the analysis.")
