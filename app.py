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

    # Calculate totals for the Income Statement
    total_revenue = merged_data[merged_data['Category'] == 'Revenue']['Balance'].sum()
    cost_of_sales = merged_data[merged_data['Category'] == 'Cost of Sales']['Balance'].sum()
    gross_profit = total_revenue - cost_of_sales
    
    # Assuming other income/expenses categories are labeled correctly in mapping
    operating_expenses = merged_data[merged_data['Category'] == 'Expense']['Balance'].sum()  # General and Administrative
    other_income = merged_data[merged_data['Category'] == 'Other Income']['Balance'].sum()
    other_expenses = merged_data[merged_data['Category'] == 'Other Expenses']['Balance'].sum()

    net_income = gross_profit + other_income - (operating_expenses + other_expenses)

    # Calculate totals for the Balance Sheet
    total_assets = merged_data[merged_data['Category'] == 'Asset']['Balance'].sum()
    total_liabilities = merged_data[merged_data['Category'] == 'Liability']['Balance'].sum()
    total_equity = merged_data[merged_data['Category'] == 'Equity']['Balance'].sum()

    return {
        "Income Statement": {
            "Total Revenue": total_revenue,
            "Cost of Sales": cost_of_sales,
            "Gross Profit": gross_profit,
            "Operating Expenses": operating_expenses,
            "Other Income": other_income,
            "Other Expenses": other_expenses,
            "Net Income": net_income
        },
        "Balance Sheet": {
            "Total Assets": total_assets,
            "Total Liabilities": total_liabilities,
            "Total Equity": total_equity
        }
    }

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
        statements = generate_financial_statements(trial_balance, mapping)

        # Display Income Statement
        st.subheader("Income Statement")
        for key, value in statements["Income Statement"].items():
            st.write(f"{key}: {value}")

        # Display Balance Sheet
        st.subheader("Balance Sheet")
        for key, value in statements["Balance Sheet"].items():
            st.write(f"{key}: {value}")

if __name__ == "__main__":
    main()
