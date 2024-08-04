import streamlit as st
import pandas as pd
import os

def load_excel_files(stock_folder):
    # Load Excel files from the specified folder
    files = [f for f in os.listdir(stock_folder) if f.endswith('.xlsx')]
    return files

def read_excel_sheets(file_path):
    # Read all sheets from the Excel file
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    sheets = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in sheet_names}
    return sheets

def get_latest_and_previous_quarter_data(df):
    # Extract latest and previous quarter columns
    cols = df.columns
    sorted_cols = sorted(cols, reverse=True)
    
    latest_col = sorted_cols[0]
    previous_col = sorted_cols[1]
    
    latest_data = df[latest_col]
    previous_data = df[previous_col]
    
    return latest_data, previous_data

def compare_quarterly_data(df):
    # Compare Total Revenue, Gross Profit, and Net Income between latest and previous quarters
    latest_data, previous_data = get_latest_and_previous_quarter_data(df)
    
    comparisons = {}
    for row in ['Total Revenue', 'Gross Profit', 'Net Income']:
        if row in latest_data.index and row in previous_data.index:
            latest_value = latest_data[row].values[0]
            previous_value = previous_data[row].values[0]
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

    stock_folder = st.text_input('Enter the path to the stock folder:', '')

    if stock_folder:
        files = load_excel_files(stock_folder)
        
        selected_file = st.selectbox('Select an Excel file:', files)
        
        if selected_file:
            file_path = os.path.join(stock_folder, selected_file)
            sheets = read_excel_sheets(file_path)
            
            if 'Income Statement (Quarterly)' in sheets:
                df_quarterly = sheets['Income Statement (Quarterly)']
                comparisons = compare_quarterly_data(df_quarterly)
                
                st.subheader('Comparison between Latest and Previous Quarter')
                
                for metric, data in comparisons.items():
                    st.write(f"**{metric}**")
                    st.write(f"Latest: {data['Latest']}")
                    st.write(f"Previous: {data['Previous']}")
                    st.write(f"Change: {data['Change']}")
                    st.write(f"Percentage Change: {data['Percentage Change']:.2f}%")
            else:
                st.error("The selected file does not contain the 'Income Statement (Quarterly)' sheet.")
    else:
        st.info('Please enter the path to the stock folder.')

if __name__ == "__main__":
    main()
