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

# Function to get the latest and previous quarter data
def get_latest_and_previous_quarter_data(df):
    # Ensure columns are datetime
    df.columns = pd.to_datetime(df.columns, errors='coerce')
    
    # Drop columns that couldn't be parsed as dates
    df = df.loc[:, df.columns.notna()]
    
    # Print columns to debug
    st.write("Columns available:", df.columns)
    
    # Check if there are at least two valid dates
    if len(df.columns) < 2:
        st.error("Not enough valid columns for comparison.")
        return None, None
    
    # Sort columns by date
    sorted_cols = sorted(df.columns, reverse=True)
    st.write("Sorted columns:", sorted_cols)
    
    # Identify latest and previous columns
    latest_col = sorted_cols[0]
    previous_col = sorted_cols[1]
    
    if latest_col not in df.columns or previous_col not in df.columns:
        st.error("Columns for latest and previous quarters are missing.")
        return None, None
    
    # Print index to debug
    st.write("Index available:", df.index)
    
    # Check if the required rows are present in the DataFrame
    required_rows = ['Total Revenue', 'Gross Profit', 'Net Income']
    available_rows = df.index.tolist()
    
    st.write("Required rows:", required_rows)
    st.write("Available rows:", available_rows)
    
    if not all(row in available_rows for row in required_rows):
        st.error("Required rows for comparison are missing in the data.")
        return None, None
    
    latest_data = df.loc[required_rows, latest_col]
    previous_data = df.loc[required_rows, previous_col]
    
    return latest_data, previous_data

# Function to compare quarterly data
def compare_quarterly_data(df):
    latest_data, previous_data = get_latest_and_previous_quarter_data(df)
    
    if latest_data is None or previous_data is None:
        return {}
    
    comparisons = {}
    for row in ['Total Revenue', 'Gross Profit', 'Net Income']:
        if row in latest_data.index and row in previous_data.index:
            latest_value = latest_data[row]
            previous_value = previous_data[row]
            comparison = {
                'Latest': latest_value,
                'Previous': previous_value,
                'Change': latest_value - previous_value,
                'Percentage Change': (latest_value - previous_value) / previous_value * 100 if previous_value != 0 else float('inf')
            }
            comparisons[row] = comparison
    
    return comparisons

def main():
    st.title('Stock Income Statement Comparison')

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
                    st.write("Quarterly Data:")
                    st.write(df_quarterly.head())
                    
                    comparisons = compare_quarterly_data(df_quarterly)
                    
                    st.subheader('Comparison between Latest and Previous Quarter')
                    
                    if comparisons:
                        for metric, data in comparisons.items():
                            st.write(f"**{metric}**")
                            st.write(f"Latest: {data['Latest']}")
                            st.write(f"Previous: {data['Previous']}")
                            st.write(f"Change: {data['Change']}")
                            st.write(f"Percentage Change: {data['Percentage Change']:.2f}%")
                    else:
                        st.write("No relevant data found for comparison.")
                else:
                    st.error("The selected file does not contain the 'Income Statement (Quarterly)' sheet.")
            else:
                st.warning(f"No file found for stock name '{selected_stock}' in the specified folder.")
    else:
        st.warning("No Excel files found in the specified folder.")

if __name__ == "__main__":
    main()
