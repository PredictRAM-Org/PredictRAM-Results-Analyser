import streamlit as st

# Load the data
data = load_data('all_stocks_data.xlsx')

# Extract stock symbols
stocks = list(data.keys())

# Streamlit app
st.title("Stock Comparative Analysis")

# Stock selection
selected_stock = st.selectbox("Select a stock:", stocks)

# Display industry information
stock_data = data[selected_stock]
industry = stock_data.get('Industry', 'Unknown')
st.write(f"**Industry:** {industry}")

# Comparative analysis
st.write("### Income Statement Comparative Analysis")

# Extract income statements
income_statement_quarterly = stock_data.get('Income Statement (Quarterly)')
income_statement_annual = stock_data.get('Income Statement (Annual)')

def compare_income_statements(income_statement, period1, period2):
    period1_data = income_statement.get(period1, {})
    period2_data = income_statement.get(period2, {})
    
    comparison = {}
    for key in period1_data.keys():
        value1 = period1_data.get(key, 0)
        value2 = period2_data.get(key, 0)
        comparison[key] = (value2 - value1) / value1 * 100 if value1 else 0
    
    return comparison

# Get last quarter and last year data
if income_statement_quarterly:
    quarters = list(income_statement_quarterly.keys())
    last_quarter = quarters[0]
    previous_quarter = quarters[1]
    
    st.write(f"**Comparison from Last Quarter ({previous_quarter.date()} to {last_quarter.date()})**")
    quarterly_comparison = compare_income_statements(income_statement_quarterly, previous_quarter, last_quarter)
    st.write(pd.DataFrame(quarterly_comparison, index=['Change (%)']).transpose())

if income_statement_annual:
    years = list(income_statement_annual.keys())
    last_year = years[0]
    previous_year = years[1]
    
    st.write(f"**Comparison from Last Year ({previous_year.date()} to {last_year.date()})**")
    annual_comparison = compare_income_statements(income_statement_annual, previous_year, last_year)
    st.write(pd.DataFrame(annual_comparison, index=['Change (%)']).transpose())
