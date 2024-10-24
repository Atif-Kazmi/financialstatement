import pandas as pd
import streamlit as st

# Function to generate financial statements
def generate_financial_statements(trial_balance):
    # Convert Category to lower case for case insensitive comparisons
    trial_balance['Category'] = trial_balance['Category'].astype(str).str.lower()

    # Convert Balance to absolute values (positive) to flip negative values
    trial_balance['Balance'] = trial_balance['Balance'].abs()
    
    # Calculate totals for the Income Statement
    total_revenue = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'total revenue')]['Balance'].sum()
    cost_of_sales = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'cost of sales')]['Balance'].sum()
    material_cost = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'material cost')]['Balance'].sum()
    manufacturing_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'manufacturing expenses')]['Balance'].sum()
    
    # Calculate gross profit as specified
    gross_profit = total_revenue - material_cost - manufacturing_expenses
    
    # Calculate other costs
    selling_costs = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'selling costs')]['Balance'].sum()
    advertising_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'advertising and publicity')]['Balance'].sum()
    carriage_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'carriage and forwarding expense')]['Balance'].sum()
    administrative_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'administrative expenses')]['Balance'].sum()
    impairment_loss = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'impairment loss on trade debts')]['Balance'].sum()
    other_operating_income = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'other operating income')]['Balance'].sum()
    other_operating_expenses = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'other operating expenses')]['Balance'].sum()
    finance_cost = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'finance cost')]['Balance'].sum()
    
    # Total marketing, selling, and distribution costs
    total_marketing_selling_costs = selling_costs + advertising_expenses + carriage_expenses

    # Total expenses before operating profit
    total_expenses_before_profit = administrative_expenses + impairment_loss + other_operating_expenses

    # Calculate profit before tax
    profit_before_tax = gross_profit - (total_marketing_selling_costs + total_expenses_before_profit + finance_cost)

    # Taxation (dummy values as placeholders, adjust as needed)
    current_tax = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'current tax')]['Balance'].sum()
    deferred_tax = trial_balance[(trial_balance['Type'] == 'Income Statement') & (trial_balance['Category'] == 'deferred tax')]['Balance'].sum()
    
    profit_after_tax = profit_before_tax - (current_tax + deferred_tax)

    return {
        "Income Statement": {
            "Net Sales": total_revenue,
            "Material Cost": material_cost,
            "Manufacturing Expenses": manufacturing_expenses,
            "Gross Profit": gross_profit,
            "Selling Costs": selling_costs,
            "Advertising and Publicity": advertising_expenses,
            "Carriage and Forwarding Expense": carriage_expenses,
            "Total Marketing, Selling & Distribution Costs": total_marketing_selling_costs,
            "Administrative Expenses": administrative_expenses,
            "Impairment Loss on Trade Debts": impairment_loss,
            "Other Operating Expenses": other_operating_expenses,
            "Other Operating Income": other_operating_income,
            "Operating Profit / (Loss)": profit_before_tax,
            "Finance Cost": finance_cost,
            "Profit / (Loss) Before Income Tax": profit_before_tax,
            "Current Tax": current_tax,
            "Deferred Tax": deferred_tax,
            "Profit / (Loss) After Tax": profit_after_tax
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
            st.write(f"{key: <45} {value:,.2f}")

if __name__ == "__main__":
    main()
