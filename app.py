import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to load Excel data from the stock folder
def load_stock_data(stock_folder, stock_name):
    # Construct the file path
    file_path = os.path.join(stock_folder, f'{stock_name}.xlsx')
    if not os.path.isfile(file_path):
        st.error(f"File {file_path} not found.")
        return None, None
    
    # Load data from the Excel file
    xl = pd.ExcelFile(file_path)
    
    # Load sheets
    try:
        quarterly_df = xl.parse('Income Statement (Quarterly)')
        annual_df = xl.parse('Income Statement (Annual)')
    except ValueError as e:
        st.error(f"Error loading sheets: {e}")
        return None, None

    return quarterly_df, annual_df

# Function to calculate percentage change
def calculate_percentage_change(df):
    # Ensure the metric row is set as the index
    df.set_index('Metric', inplace=True)
    
    # Calculate percentage change
    percentage_change = df.pct_change(axis=1) * 100
    return percentage_change

# Main function to display the app
def main():
    st.title("Stock Data Analysis")

    # Directory containing stock files
    stock_folder = 'path/to/stock_folder'  # Update with the actual path

    # List stock files
    stock_files = [f.replace('.xlsx', '') for f in os.listdir(stock_folder) if f.endswith('.xlsx')]
    
    # User selects a stock
    stock_name = st.selectbox("Select a Stock", stock_files)

    if stock_name:
        # Load data
        quarterly_df, annual_df = load_stock_data(stock_folder, stock_name)
        
        if quarterly_df is not None and annual_df is not None:
            st.subheader("Quarterly Income Statement Data")
            st.dataframe(quarterly_df)
            
            st.subheader("Annual Income Statement Data")
            st.dataframe(annual_df)

            # Process quarterly data
            if 'Metric' in quarterly_df.columns:
                quarterly_percentage_change = calculate_percentage_change(quarterly_df)
                
                st.subheader("Quarterly Data Percentage Change")
                st.dataframe(quarterly_percentage_change)

                # Plotting quarterly percentage changes
                fig, ax = plt.subplots(figsize=(12, 8))
                for metric in quarterly_percentage_change.index:
                    ax.plot(quarterly_percentage_change.columns, quarterly_percentage_change.loc[metric], marker='o', label=metric)
                
                ax.set_title('Quarterly Percentage Change')
                ax.set_xlabel('Quarter')
                ax.set_ylabel('Percentage Change (%)')
                ax.legend(loc='best')
                ax.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)

            # Process annual data
            if 'Metric' in annual_df.columns:
                annual_percentage_change = calculate_percentage_change(annual_df)
                
                st.subheader("Annual Data Percentage Change")
                st.dataframe(annual_percentage_change)

                # Plotting annual percentage changes
                fig, ax = plt.subplots(figsize=(12, 8))
                for metric in annual_percentage_change.index:
                    ax.plot(annual_percentage_change.columns, annual_percentage_change.loc[metric], marker='o', label=metric)
                
                ax.set_title('Annual Percentage Change')
                ax.set_xlabel('Year')
                ax.set_ylabel('Percentage Change (%)')
                ax.legend(loc='best')
                ax.grid(True)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)

if __name__ == "__main__":
    main()
