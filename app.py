import pandas as pd
import streamlit as st

# Function to generate financial statements
def generate_financial_statements(trial_balance, mapping):
    # Rename the column to match for merging
    trial_balance = trial_balance.rename(columns={'Account': 'Account Name'})

    # Merge trial balance with mapping on 'Account Name'
    merged_data = pd.merge(
        trial_balance[['Account Name', 'Balance']], 
        mapping[['Account Name', 'Category']], 
        on='Account Name', 
        how='left'
    )
    
    # Debug: Show merged data
    st.write("Merged Data:")
    st.dataframe(merged_data)

    # Separate Income Statement and Balance Sheet
    income_statement = merged_data[merged_data['Category'] == 'Income']
    expenses_statement = merged_data[merged_data['Category'] == 'Expense']
    balance_sheet_assets = merged_data[merged_data['Category'] == 'Asset']
    balance_sheet_liabilities = merged_data[merged_data['Category'] == 'Liability']
    equity_statement = merged_data[merged_data['Category'] == 'Equity']

    # Summarize Income Statement
    total_income = income_statement['Balance'].sum()
    total_expenses = expenses_statement['Balance'].sum()
    net_income = total_income - total_expenses

    # Summarize Balance Sheet
    total_assets = balance_sheet_assets['Balance'].sum()
    total_liabilities = balance_sheet_liabilities['Balance'].sum()
    total_equity = equity_statement['Balance'].sum()
    
    return total_income, total_expenses, net_income, total_assets, total_liabilities, total_equity

# Main Streamlit app
def main():
    st.title("Financial Statement Generator According to IAS")

    # File upload
    trial_balance_file = st.file_uploader("Upload Trial Balance Excel File", type=["xlsx"])
    mapping_file = st.file_uploader("Upload Mapping Excel File", type=["xlsx"])

    if trial_balance_file and mapping_file:
        trial_balance = pd.read_excel(trial_balance_file)
        mapping = pd.read_excel(mapping_file)

        # Debug: Show loaded data
        st.write("Loaded Trial Balance Data:")
        st.dataframe(trial_balance)

        st.write("Loaded Mapping Data:")
        st.dataframe(mapping)

        # Generate financial statements
        total_income, total_expenses, net_income, total_assets, total_liabilities, total_equity = generate_financial_statements(trial_balance, mapping)

        # Display Income Statement
        st.subheader("Income Statement")
        st.write(f"Total Income: {total_income}")
        st.write(f"Total Expenses: {total_expenses}")
        st.write(f"Net Income: {net_income}")

        # Display Balance Sheet
        st.subheader("Balance Sheet")
        st.write(f"Total Assets: {total_assets}")
        st.write(f"Total Liabilities: {total_liabilities}")
        st.write(f"Total Equity: {total_equity}")

if __name__ == "__main__":
    main()
