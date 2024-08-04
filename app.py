import streamlit as st
import pandas as pd
import os

def load_excel_files(stock_folder):
    # Verify the folder path is correct
    if not stock_folder:
        st.error("Stock folder path is empty. Please enter a valid path.")
        return []
    
    # Ensure the path is an absolute path
    stock_folder = os.path.abspath(stock_folder)
    
    if not os.path.isdir(stock_folder):
        st.error(f"The path '{stock_folder}' is not a valid directory.")
        return []
    
    try:
        files = [f for f in os.listdir(stock_folder) if f.endswith('.xlsx')]
        if not files:
            st.warning("No Excel files found in the specified folder.")
        return files
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return []

def read_excel_sheets(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        sheets = {sheet: pd.read_excel(xls, sheet_name=sheet) for sheet in sheet_names}
        return sheets
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return {}

def get_latest_and_previous_quarter_data(df):
    cols = df.columns
    sorted_cols = sorted(cols, reverse=True)
    
    if len(sorted_cols) < 2:
        st.error("Not enough columns to compare latest and previous quarters.")
        return None, None
    
    latest_col = sorted_cols[0]
    previous_col = sorted_cols[1]
    
    latest_data = df[latest_col]
    previous_data = df[previous_col]
    
    return latest_data, previous_data

def compare_quarterly_data(df):
    latest_data, previous_data = get_latest_and_previous_quarter_data(df)
    
    if latest_data is None or previous_data is None:
        return {}
    
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

    # Provide the path to the cloned repository or stock folder
    stock_folder = st.text_input('Enter the path to the stock folder:', '')

    if stock_folder:
        st.write(f"Stock folder path: {stock_folder}")
        
        # Load Excel files from the provided folder path
        files = load_excel_files(stock_folder)
        
        if files:
            selected_file = st.selectbox('Select an Excel file:', files)
            
            if selected_file:
                file_path = os.path.join(stock_folder, selected_file)
                st.write(f"Selected file path: {file_path}")
                
                # Read sheets from the selected Excel file
                sheets = read_excel_sheets(file_path)
                
                if 'Income Statement (Quarterly)' in sheets:
                    df_quarterly = sheets['Income Statement (Quarterly)']
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
            st.warning("No Excel files found in the specified folder.")
    else:
        st.info('Please enter the path to the stock folder.')

if __name__ == "__main__":
    main()
