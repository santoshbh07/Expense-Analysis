# Expense Data Analysis

A Python project that analyzes and visualizes monthly family expenses using Excel data.  
The workflow processes raw expense data, generates insights, and produces visual and report outputs.

## Features
- Reads expense data from `Expense_data.xlsx`
- Cleans and reshapes data using pandas
- Computes:
  - Total expenses
  - Average monthly expense
  - Category-wise totals
  - Monthly totals
- Generates visualizations:
  - Pie chart: expenses by category
  - Line chart: monthly expenses over time
  - Bar chart: category totals
  - Stacked bar chart: monthly expenses by category
- Outputs:
  - All plots saved as `.png` in `plots/`
  - Summary Excel file: `Expense_summary.xlsx`
  - PDF report: `Expense_report.pdf`

## Tools
Python, pandas, matplotlib, seaborn, openpyxl
