import streamlit as st
import pandas as pd
import os

# Function to load Excel files from a given directory
def load_excel_files(stock_folder):
    stock_folder = os.path.abspath(stock_folder)
    if not os.path.isdir(stock_folder):
        st.error(f"The path '{stock_folder}' is not a valid directory.")
        return []
    
    try:
        files = [f for f in os.listdir(stock_folder) if f.endswith('.xlsx')]
        return files
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return []

# Function to find the Excel file for the selected stock
def find_stock_file(stock_name, stock_folder):
    files = load_excel_files(stock_folder)
    for file in files:
        if stock_name in file:
            return file
    return None

# Function to read all sheets from an Excel file
def read_excel_sheets(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        sheets = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in sheet_names}
        return sheets
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return {}

# Function to compare quarterly data for each year
def compare_quarterly_data(df):
    df.columns = pd.to_datetime(df.columns, errors='coerce')
    df = df.loc[:, df.columns.notna()]
    df = df.sort_index(axis=1, ascending=False)

    # Print columns to debug
    st.write("Quarterly Columns available:", df.columns)

    if df.shape[1] < 2:
        st.error("Not enough valid columns for comparison.")
        return None
    
    # Define metrics of interest
    metrics = ['Total Revenue', 'Gross Profit', 'Net Income']
    comparisons = {}
    
    for metric in metrics:
        if metric in df.index:
            metric_data = df.loc[metric]
            metric_comparisons = []
            
            for i in range(len(metric_data) - 1):
                current_quarter = metric_data.index[i]
                previous_quarter = metric_data.index[i + 1]
                current_value = metric_data[current_quarter]
                previous_value = metric_data[previous_quarter]
                
                comparison = {
                    'Current Quarter': current_quarter,
                    'Previous Quarter': previous_quarter,
                    'Change': current_value - previous_value,
                    'Percentage Change': (current_value - previous_value) / previous_value * 100 if previous_value != 0 else float('inf')
                }
                
                metric_comparisons.append(comparison)
            
            comparisons[metric] = metric_comparisons
    
    return comparisons

# Function to compare annual data for each year
def compare_annual_data(df):
    df.columns = pd.to_datetime(df.columns, errors='coerce')
    df = df.loc[:, df.columns.notna()]
    df = df.sort_index(axis=1, ascending=False)

    # Print columns to debug
    st.write("Annual Columns available:", df.columns)

    if df.shape[1] < 2:
        st.error("Not enough valid columns for comparison.")
        return None
    
    # Define metrics of interest
    metrics = ['Total Revenue', 'Gross Profit', 'Net Income']
    comparisons = {}
    
    for metric in metrics:
        if metric in df.index:
            metric_data = df.loc[metric]
            metric_comparisons = []
            
            for i in range(len(metric_data) - 1):
                current_year = metric_data.index[i]
                previous_year = metric_data.index[i + 1]
                current_value = metric_data[current_year]
                previous_value = metric_data[previous_year]
                
                comparison = {
                    'Current Year': current_year,
                    'Previous Year': previous_year,
                    'Change': current_value - previous_value,
                    'Percentage Change': (current_value - previous_value) / previous_value * 100 if previous_value != 0 else float('inf')
                }
                
                metric_comparisons.append(comparison)
            
            comparisons[metric] = metric_comparisons
    
    return comparisons

def main():
    st.title('Stock Income Statement Comparative Analysis')

    stock_folder = '/mount/src/predictram-results-analyser/stock_folder'
    
    files = load_excel_files(stock_folder)

    if files:
        stock_names = [os.path.splitext(file)[0] for file in files]
        selected_stock = st.selectbox('Select a stock:', stock_names)
        
        if selected_stock:
            stock_file = find_stock_file(selected_stock, stock_folder)
            
            if stock_file:
                file_path = os.path.join(stock_folder, stock_file)
                st.write(f"Selected file path: {file_path}")
                
                sheets = read_excel_sheets(file_path)
                
                if 'Income Statement (Quarterly)' in sheets:
                    df_quarterly = sheets['Income Statement (Quarterly)']
                    st.subheader("Quarterly Data")
                    st.write(df_quarterly)
                    
                    comparisons_quarterly = compare_quarterly_data(df_quarterly)
                    
                    st.subheader('Quarterly Data Comparison')
                    
                    if comparisons_quarterly:
                        for metric, comparisons in comparisons_quarterly.items():
                            st.write(f"**{metric}**")
                            for comparison in comparisons:
                                st.write(f"Current Quarter: {comparison['Current Quarter']}")
                                st.write(f"Previous Quarter: {comparison['Previous Quarter']}")
                                st.write(f"Change: {comparison['Change']}")
                                st.write(f"Percentage Change: {comparison['Percentage Change']:.2f}%")
                    else:
                        st.write("No relevant quarterly data found for comparison.")
                
                if 'Income Statement (Annual)' in sheets:
                    df_annual = sheets['Income Statement (Annual)']
                    st.subheader("Annual Data")
                    st.write(df_annual)
                    
                    comparisons_annual = compare_annual_data(df_annual)
                    
                    st.subheader('Annual Data Comparison')
                    
                    if comparisons_annual:
                        for metric, comparisons in comparisons_annual.items():
                            st.write(f"**{metric}**")
                            for comparison in comparisons:
                                st.write(f"Current Year: {comparison['Current Year']}")
                                st.write(f"Previous Year: {comparison['Previous Year']}")
                                st.write(f"Change: {comparison['Change']}")
                                st.write(f"Percentage Change: {comparison['Percentage Change']:.2f}%")
                    else:
                        st.write("No relevant annual data found for comparison.")
                
                else:
                    st.error("The selected file does not contain the required sheets.")
            else:
                st.warning(f"No file found for stock name '{selected_stock}' in the specified folder.")
    else:
        st.warning("No Excel files found in the specified folder.")

if __name__ == "__main__":
    main()
