import pandas as pd
import streamlit as st

# Function to generate financial statements
def generate_financial_statements(trial_balance, mapping):
    # Rename the column to match for merging
    trial_balance = trial_balance.rename(columns={'Account': 'Account Name'})

    # Merge trial balance with mapping on 'Account Name'
    merged_data = pd.merge(trial_balance[['Account Name', 'Balance']], 
                            mapping[['Account Name', 'Category']], 
                            on='Account Name', 
                            how='left')

    # Summarize by category
    financial_summary = merged_data.groupby('Category').sum(numeric_only=True).reset_index()
    
    return financial_summary

# Main Streamlit app
def main():
    st.title("Financial Statement Generator")

    # File upload
    trial_balance_file = st.file_uploader("Upload Trial Balance Excel File", type=["xlsx"])
    mapping_file = st.file_uploader("Upload Mapping Excel File", type=["xlsx"])

    if trial_balance_file and mapping_file:
        trial_balance = pd.read_excel(trial_balance_file)
        mapping = pd.read_excel(mapping_file)
        
        st.write("Trial Balance Data:")
        st.dataframe(trial_balance)
        
        st.write("Mapping Data:")
        st.dataframe(mapping)
        
        # Generate financial statements
        financial_statements = generate_financial_statements(trial_balance, mapping)
        
        st.write("Generated Financial Statements:")
        st.dataframe(financial_statements)

if __name__ == "__main__":
    main()
