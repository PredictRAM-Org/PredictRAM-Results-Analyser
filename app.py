import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch stock info
def fetch_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        history = stock.history(period='1y')
        return stock, info, history
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None, None, None

# Function to fetch income statement data
def fetch_income_statement(symbol):
    try:
        stock = yf.Ticker(symbol)
        income_statement = stock.financials.T
        income_statement.index = pd.to_datetime(income_statement.index)
        income_statement.sort_index(ascending=False, inplace=True)
        return income_statement
    except Exception as e:
        st.error(f"Error fetching income statement data: {e}")
        return pd.DataFrame()

# Function to fetch yearly income statement data
def fetch_yearly_income_statement(symbol):
    try:
        stock = yf.Ticker(symbol)
        yearly_income_statement = stock.financials.T.groupby(stock.financials.columns.year).sum()
        return yearly_income_statement
    except Exception as e:
        st.error(f"Error fetching yearly income statement data: {e}")
        return pd.DataFrame()

# Function to fetch quarterly income statement data
def fetch_quarterly_income_statement(symbol):
    try:
        stock = yf.Ticker(symbol)
        quarterly_income_statement = stock.quarterly_financials.T
        quarterly_income_statement.index = pd.to_datetime(quarterly_income_statement.index)
        quarterly_income_statement.sort_index(ascending=False, inplace=True)
        return quarterly_income_statement
    except Exception as e:
        st.error(f"Error fetching quarterly income statement data: {e}")
        return pd.DataFrame()

# Function to fetch yearly balance sheet data
def fetch_yearly_balance_sheet(symbol):
    try:
        stock = yf.Ticker(symbol)
        yearly_balance_sheet = stock.balance_sheet.T.groupby(stock.balance_sheet.columns.year).sum()
        return yearly_balance_sheet
    except Exception as e:
        st.error(f"Error fetching yearly balance sheet data: {e}")
        return pd.DataFrame()

# Function to calculate risk score for investors
def calculate_investor_score(info):
    try:
        pe_ratio = info.get('forwardEps', 1) / info.get('regularMarketPrice', 1)
        pb_ratio = info.get('priceToBook', 1)
        roe = info.get('returnOnEquity', 0)
        profit_margin = info.get('profitMargins', 0)
        debt_to_equity = info.get('debtToEquity', 1)
        
        score = 0
        score += 5 if pe_ratio < 10 else (4 if pe_ratio <= 15 else (3 if pe_ratio <= 20 else 2))
        score += 5 if pb_ratio < 1 else (4 if pb_ratio <= 2 else (3 if pb_ratio <= 3 else 2))
        score += 5 if roe >= 0.20 else (4 if roe >= 0.15 else (3 if roe >= 0.10 else 2))
        score += 5 if profit_margin >= 0.20 else (4 if profit_margin >= 0.15 else (3 if profit_margin >= 0.10 else 2))
        score += 5 if debt_to_equity < 0.5 else (4 if debt_to_equity <= 1 else (3 if debt_to_equity <= 1.5 else 2))
        
        return score
    except Exception as e:
        st.error(f"Error calculating investor score: {e}")
        return 0

# Function to calculate risk score for traders
def calculate_trader_score(info, history):
    try:
        beta = info.get('beta', 1)
        volume = info.get('averageVolume', 1)
        avg_volume = history['Volume'].mean()
        daily_range = (history['High'] - history['Low']).mean() / history['Close'].mean()
        recent_trend = (history['Close'].iloc[-1] - history['Close'].iloc[0]) / history['Close'].iloc[0]
        
        score = 0
        score += 5 if beta >= 1.5 else (4 if beta >= 1.2 else (3 if beta >= 1 else 2))
        volume_ratio = volume / avg_volume
        score += 5 if volume_ratio >= 2 else (4 if volume_ratio >= 1.5 else (3 if volume_ratio >= 1 else 2))
        score += 5 if info.get('bidAskSpread', 0) < 0.01 else (4 if info.get('bidAskSpread', 0) <= 0.02 else (3 if info.get('bidAskSpread', 0) <= 0.03 else 2))
        score += 5 if daily_range >= 0.05 else (4 if daily_range >= 0.03 else (3 if daily_range >= 0.01 else 2))
        score += 5 if recent_trend > 0.1 else (4 if recent_trend > 0 else (3 if recent_trend == 0 else 2))
        
        return score
    except Exception as e:
        st.error(f"Error calculating trader score: {e}")
        return 0

# Streamlit App
st.title("Stock Financials Dashboard")

# Input for stock symbol
stock_symbol = st.text_input("Enter the stock symbol", value='ITC.NS')

if stock_symbol:
    stock, info, history = fetch_stock_info(stock_symbol)
    
    if stock and info and history is not None:
        # Calculate and show risk scores
        investor_score = calculate_investor_score(info)
        trader_score = calculate_trader_score(info, history)
        
        st.subheader(f"Risk Meter for {stock_symbol}")

        # Display investor score
        st.subheader("Investor Risk Score")
        st.metric(label="Investor Score", value=f"{investor_score}/25")
        st.progress(min(investor_score / 25, 1))

        if investor_score >= 20:
            st.success("This stock is considered Investor-Friendly.")
        else:
            st.warning("This stock is not considered Investor-Friendly.")
        
        # Display trader score
        st.subheader("Trader Risk Score")
        st.metric(label="Trader Score", value=f"{trader_score}/25")
        st.progress(min(trader_score / 25, 1))

        if trader_score >= 20:
            st.success("This stock is considered Trader-Friendly.")
        else:
            st.warning("This stock is not considered Trader-Friendly.")
        
        # Fetch and show income statement
        income_statement = fetch_income_statement(stock_symbol)
        
        if not income_statement.empty:
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

        # Fetch and show yearly balance sheet data
        st.subheader(f"Yearly Balance Sheet for {stock_symbol}")
        yearly_balance_sheet = fetch_yearly_balance_sheet(stock_symbol)
        st.dataframe(yearly_balance_sheet)

        st.subheader("Select Parameters to Visualize (Yearly Balance Sheet)")
        selected_balance_sheet_parameters = st.multiselect("Choose parameters (Yearly):", yearly_balance_sheet.columns.tolist(), default=['Total Assets', 'Total Liabilities', 'Shareholder Equity'])
        
        if selected_balance_sheet_parameters:
            st.subheader("Yearly Balance Sheet Visualization")
            fig, ax = plt.subplots()
            yearly_balance_sheet[selected_balance_sheet_parameters].plot(ax=ax, kind='bar')
            plt.xticks(rotation=45)
            plt.ylabel('Amount')
            plt.title(f"Selected Yearly Balance Sheet Parameters for {stock_symbol}")
            st.pyplot(fig)

    else:
        st.warning(f"No data available for {stock_symbol}")
else:
    st.info("Please enter a stock symbol to start the analysis.")
