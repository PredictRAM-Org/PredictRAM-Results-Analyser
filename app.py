import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data(filepath):
    return pd.read_excel(filepath, sheet_name=None)

# Select stock and industry
def get_stock_and_industry(stock_data):
    stocks = list(stock_data.keys())
    selected_stock = st.selectbox("Select a stock:", stocks)
    industry = stock_data[selected_stock].get('Industry')
    return selected_stock, industry

# Compare quarterly and annual income statements
def compare_income_statements(stock_data, selected_stock):
    income_statement_quarterly = stock_data[selected_stock].get('Income Statement (Quarterly)', {})
    income_statement_annual = stock_data[selected_stock].get('Income Statement (Annual)', {})

    if not income_statement_quarterly or not income_statement_annual:
        st.warning("Income statement data is missing.")
        return

    last_quarter = max(income_statement_quarterly.keys())
    last_year = max(income_statement_annual.keys())

    last_quarter_data = income_statement_quarterly[last_quarter]
    last_year_data = income_statement_annual[last_year]

    st.write(f"### Comparative Analysis for {selected_stock}")
    st.write(f"#### Last Quarter ({last_quarter}) vs Last Year ({last_year})")

    comparison_data = []
    for key in last_quarter_data:
        if key in last_year_data:
            quarterly_value = last_quarter_data[key]
            annual_value = last_year_data[key]
            change = quarterly_value - annual_value
            percent_change = (change / annual_value) * 100 if annual_value != 0 else 0
            comparison_data.append([key, quarterly_value, annual_value, change, percent_change])

    comparison_df = pd.DataFrame(comparison_data, columns=["Parameter", "Last Quarter Value", "Last Year Value", "Change", "Percent Change"])
    st.dataframe(comparison_df)

# Main function
def main():
    st.title("Stock Comparative Analysis")
    filepath = 'all_stocks_data.xlsx'
    stock_data = load_data(filepath)
    
    if stock_data:
        selected_stock, industry = get_stock_and_industry(stock_data)
        st.write(f"Selected Stock: {selected_stock}")
        st.write(f"Industry: {industry}")

        compare_income_statements(stock_data, selected_stock)
    else:
        st.error("Failed to load stock data.")

if __name__ == "__main__":
    main()
