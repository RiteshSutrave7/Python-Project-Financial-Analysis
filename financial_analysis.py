import xml.etree.ElementTree as ET
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load XML file
xml_file = "Profit_and_Loss_Apr24_to_Jul24.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# Extract financial data
def extract_data(tag_name, category):
    data = []
    for bsname, bsamt in zip(root.findall(".//BSNAME"), root.findall(".//BSAMT")):
        name_elem = bsname.find("DSPACCNAME/DSPDISPNAME")
        amount_elem = bsamt.find("BSSUBAMT")
        if name_elem is not None and amount_elem is not None and amount_elem.text:
            try:
                amount = float(amount_elem.text.strip())
            except ValueError:
                amount = 0  # Default if conversion fails
            data.append({"Category": category, "Account": name_elem.text.strip(), "Amount": amount})
    return data

# Extract different financial data
sales_data = extract_data("BSNAME", "Direct Income")
expenses_data = extract_data("BSNAME", "Indirect Expense")

df_sales = pd.DataFrame(sales_data)
df_expenses = pd.DataFrame(expenses_data)

total_income = df_sales["Amount"].sum()
total_expenses = df_expenses["Amount"].sum()
cost_of_sales = -566207.84  # Extracted from XML manually

gross_profit = total_income - cost_of_sales
net_profit = total_income - total_expenses

gross_profit_ratio = gross_profit / total_income if total_income != 0 else 0
net_profit_ratio = net_profit / total_income if total_income != 0 else 0
expense_ratio = total_expenses / total_income if total_income != 0 else 0

# Create DataFrame for financial ratios
ratios = pd.DataFrame({
    "Ratio": ["Gross Profit Ratio", "Net Profit Ratio", "Expense Ratio"],
    "Value": [gross_profit_ratio, net_profit_ratio, expense_ratio]
})

# Visualization
fig_bar = px.bar(df_sales, x="Account", y="Amount", title="Breakdown of Direct Incomes", labels={"Amount": "Value"})
fig_pie = px.pie(df_expenses, names="Account", values="Amount", title="Distribution of Indirect Expenses")
fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=["Total Income", "Total Expenses"], y=[total_income, total_expenses], mode='lines+markers', name='Trend'))
fig_line.update_layout(title="Trend of Total Income vs. Total Expenses", xaxis_title="Category", yaxis_title="Amount")

# Display charts
fig_bar.show()
fig_pie.show()
fig_line.show()

# Create summary tables
top5_income = df_sales.nlargest(5, "Amount")
top5_expenses = df_expenses.nlargest(5, "Amount")
total_summary = pd.DataFrame({"Category": ["Total Income", "Total Expenses", "Net Profit"], "Amount": [total_income, total_expenses, net_profit]})

# Save outputs
df_sales.to_csv("direct_income.csv", index=False)
df_expenses.to_csv("indirect_expenses.csv", index=False)
ratios.to_csv("financial_ratios.csv", index=False)
top5_income.to_csv("top5_income.csv", index=False)
top5_expenses.to_csv("top5_expenses.csv", index=False)
total_summary.to_csv("total_summary.csv", index=False)

print("Data processing and visualization completed. Output saved as CSV files.")
