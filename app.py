import pandas as pd
import streamlit as st

# Function to generate financial statements
def generate_financial_statements(trial_balance):
    # Convert Account Name and Category to lower case for case insensitive comparisons
    trial_balance['Account'] = trial_balance['Account'].astype(str).str.lower()
    trial_balance['Category'] = trial_balance['Category'].astype(str).str.lower()

    # Calculate totals for the Income Statement
    total_revenue = trial_balance[trial_balance['Category'] == 'revenue']['Balance'].sum()
    cost_of_sales = trial_balance[trial_balance['Category'] == 'cost of sales']['Balance'].sum()
    gross_profit = total_revenue - cost_of_sales
    
    # Assuming other income/expenses categories are labeled correctly in trial balance
    operating_expenses = trial_balance[trial_balance['Category'] == 'expense']['Balance'].sum()  # General and Administrative
    other_income = trial_balance[trial_balance['Category'] == 'other income']['Balance'].sum()
    other_expenses = trial_balance[trial_balance['Category'] == 'other expenses']['Balance'].sum()

    net_income = gross_profit + other_income - (operating_expenses + other_expenses)

    # Calculate totals for the Balance Sheet
    total_assets = trial_balance[trial_balance['Category'] == 'asset']['Balance'].sum()
    total_liabilities = trial_balance[trial_balance['Category'] == 'liability']['Balance'].sum()
    total_equity = trial_balance[trial_balance['Category'] == 'equity']['Balance'].sum()

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

    if trial_balance_file:
        trial_balance = pd.read_excel(trial_balance_file)

        # Debug: Show loaded data
        st.write("Loaded Trial Balance Data:")
        st.dataframe(trial_balance)

        # Generate financial statements
        statements = generate_financial_statements(trial_balance)

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
