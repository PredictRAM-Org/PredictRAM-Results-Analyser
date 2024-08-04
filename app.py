import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

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

# Function to compare data for each metric
def compare_data(df, metrics):
    df.columns = pd.to_datetime(df.columns, errors='coerce')
    df = df.loc[:, df.columns.notna()]
    df = df.sort_index(axis=1, ascending=False)

    comparisons = {}
    
    for metric in metrics:
        if metric in df.index:
            metric_data = df.loc[metric]
            metric_comparisons = []
            
            for i in range(len(metric_data) - 1):
                current_period = metric_data.index[i]
                previous_period = metric_data.index[i + 1]
                current_value = metric_data[current_period]
                previous_value = metric_data[previous_period]
                
                comparison = {
                    'Period': current_period,
                    'Previous Period': previous_period,
                    'Change': current_value - previous_value,
                    'Percentage Change': (current_value - previous_value) / previous_value * 100 if previous_value != 0 else float('inf')
                }
                
                metric_comparisons.append(comparison)
            
            comparisons[metric] = metric_comparisons
    
    return comparisons

# Function to plot data
def plot_comparisons(comparisons, metric_name):
    df_comparison = pd.DataFrame(comparisons[metric_name])
    if df_comparison.empty:
        st.write(f"No data available for {metric_name} comparisons.")
        return
    
    df_comparison.set_index('Period', inplace=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    df_comparison[['Change', 'Percentage Change']].plot(kind='bar', ax=ax)
    plt.title(f'{metric_name} Comparison')
    plt.xlabel('Period')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

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
                    
                    metrics = ['Total Revenue', 'Operating Expense', 'Operating Income', 'Net Income']
                    comparisons_quarterly = compare_data(df_quarterly, metrics)
                    
                    st.subheader('Quarterly Data Comparison')
                    
                    if comparisons_quarterly:
                        for metric, comparisons in comparisons_quarterly.items():
                            st.write(f"**{metric}**")
                            st.write(pd.DataFrame(comparisons))
                            plot_comparisons(comparisons, metric)
                    else:
                        st.write("No relevant quarterly data found for comparison.")
                
                if 'Income Statement (Annual)' in sheets:
                    df_annual = sheets['Income Statement (Annual)']
                    st.subheader("Annual Data")
                    st.write(df_annual)
                    
                    comparisons_annual = compare_data(df_annual, metrics)
                    
                    st.subheader('Annual Data Comparison')
                    
                    if comparisons_annual:
                        for metric, comparisons in comparisons_annual.items():
                            st.write(f"**{metric}**")
                            st.write(pd.DataFrame(comparisons))
                            plot_comparisons(comparisons, metric)
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
