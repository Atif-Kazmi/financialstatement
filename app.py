import pandas as pd
import streamlit as st

# Function to generate financial statements
def generate_financial_statements(trial_balance):
    # Convert Category to lower case for case insensitive comparisons
    trial_balance['Category'] = trial_balance['Category'].astype(str).str.lower()
    
    # Calculate totals for the Income Statement
    total_revenue = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'total revenue')]['Balance'].sum()
    other_operating_income = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'other operating income')]['Balance'].sum()
    share_of_profit = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'share of profit from associates')]['Balance'].sum()
    impairment_on_investment = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'impairment on investment in associate -')]['Balance'].sum()
    cost_of_sales = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'cost of sales')]['Balance'].sum()
    operating_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'manufacturing, selling and administration expenses')]['Balance'].sum()
    other_operating_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'other operating expenses')]['Balance'].sum()
    finance_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'finance expenses')]['Balance'].sum()
    taxation_pnl = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'taxation & pnl')]['Balance'].sum()
    taxation_oci = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'taxation - oci')]['Balance'].sum()

    gross_profit = total_revenue - cost_of_sales
    total_expenses = operating_expenses + other_operating_expenses + finance_expenses + taxation_pnl + taxation_oci
    net_income = gross_profit + other_operating_income + share_of_profit - total_expenses - impairment_on_investment

    # Calculate totals for the Balance Sheet
    total_assets = trial_balance[(trial_balance['Type'] == 'Balance Sheet')]['Balance'].sum()
    total_liabilities = trial_balance[(trial_balance['Type'] == 'Balance Sheet') & (trial_balance['Category'].str.contains('liabilities', case=False))]['Balance'].sum()
    total_equity = trial_balance[(trial_balance['Type'] == 'Balance Sheet') & (trial_balance['Category'].str.contains('equity', case=False))]['Balance'].sum()

    return {
        "Income Statement": {
            "Total Revenue": total_revenue,
            "Other Operating Income": other_operating_income,
            "Share Of Profit": share_of_profit,
            "Cost of Sales": cost_of_sales,
            "Gross Profit": gross_profit,
            "Operating Expenses": operating_expenses,
            "Other Operating Expenses": other_operating_expenses,
            "Finance Expenses": finance_expenses,
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
