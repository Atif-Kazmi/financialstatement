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

    # Debug: Show merged data and its info
    st.write("Merged Data:")
    st.dataframe(merged_data)
    st.write("Merged Data Info:")
    st.write(merged_data.info())

    # Check unique categories
    st.write("Unique Categories in Merged Data:")
    st.write(merged_data['Category'].unique())

    # Calculate totals for each category
    totals = merged_data.groupby('Category')['Balance'].sum().reset_index()
    totals.rename(columns={'Balance': 'Total'}, inplace=True)
    
    # Show totals in the merged data output
    st.write("Totals for Each Category:")
    st.dataframe(totals)

    return merged_data, totals

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
        merged_data, totals = generate_financial_statements(trial_balance, mapping)

        # Display Income Statement
        st.subheader("Income Statement")
        total_income = totals[totals['Category'] == 'Income']['Total'].sum()
        total_expenses = totals[totals['Category'] == 'Expense']['Total'].sum()
        net_income = total_income - total_expenses

        st.write(f"Total Income: {total_income}")
        st.write(f"Total Expenses: {total_expenses}")
        st.write(f"Net Income: {net_income}")

        # Display Balance Sheet
        st.subheader("Balance Sheet")
        total_assets = totals[totals['Category'] == 'Asset']['Total'].sum()
        total_liabilities = totals[totals['Category'] == 'Liability']['Total'].sum()
        total_equity = totals[totals['Category'] == 'Equity']['Total'].sum()

        st.write(f"Total Assets: {total_assets}")
        st.write(f"Total Liabilities: {total_liabilities}")
        st.write(f"Total Equity: {total_equity}")

if __name__ == "__main__":
    main()
