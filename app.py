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

    # Create a summary DataFrame for specific categories
    summary = {
        "Total Revenue": merged_data[merged_data['Category'] == 'Revenue']['Balance'].sum(),
        "Cost of Sales": merged_data[merged_data['Category'] == 'Cost of Sales']['Balance'].sum(),
        "Total Income": merged_data[merged_data['Category'] == 'Income']['Balance'].sum(),
        "Total Expenses": merged_data[merged_data['Category'] == 'Expense']['Balance'].sum(),
        "Total Assets": merged_data[merged_data['Category'] == 'Asset']['Balance'].sum(),
        "Total Liabilities": merged_data[merged_data['Category'] == 'Liability']['Balance'].sum(),
        "Total Equity": merged_data[merged_data['Category'] == 'Equity']['Balance'].sum(),
    }
    
    return summary

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
        summary = generate_financial_statements(trial_balance, mapping)

        # Display Income Statement
        st.subheader("Income Statement")
        st.write(f"Total Revenue: {summary['Total Revenue']}")
        st.write(f"Cost of Sales: {summary['Cost of Sales']}")
        st.write(f"Total Income: {summary['Total Income']}")
        st.write(f"Total Expenses: {summary['Total Expenses']}")
        net_income = summary['Total Income'] - summary['Total Expenses']
        st.write(f"Net Income: {net_income}")

        # Display Balance Sheet
        st.subheader("Balance Sheet")
        st.write(f"Total Assets: {summary['Total Assets']}")
        st.write(f"Total Liabilities: {summary['Total Liabilities']}")
        st.write(f"Total Equity: {summary['Total Equity']}")

if __name__ == "__main__":
    main()
