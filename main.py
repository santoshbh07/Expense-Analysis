import os #for file path operations
import pandas as pd #for data manipulation
import matplotlib.pyplot as plt #for plotting graphs
from matplotlib.backends.backend_pdf import PdfPages #for saving multiple plots in one pdf

def main(file_path="Expense_data.xlsx"):
    # Analysing data using pandas
    data = pd.read_excel(file_path)

    expenses = pd.DataFrame(data)

    month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    missing_vals = expenses.isnull().sum() #checks if there is missing value

    expenses = expenses.drop("Total Expenses", axis=1)

    expenses_long = expenses.melt(id_vars=["Month"], var_name="Category", value_name="Amount")
    expenses_long["Month"] = pd.Categorical(expenses_long["Month"], categories=month_order, ordered=True)

    # Basic Analysis
    total = expenses_long["Amount"].sum()
    avg = expenses_long["Amount"].mean().round(2)
    category_totals = expenses_long.groupby("Category")["Amount"].sum()
    monthly_totals = expenses_long.groupby("Month")["Amount"].sum()
    monthly_totals = monthly_totals.reindex(month_order)


    print(f"Total expenses: ${total}")
    print(f"Average expense: ${avg} per month")
    print("\nTotal by category:\n", category_totals)
    print("\nMonthly totals:\n", monthly_totals)

    # Visualizing data using matplotlib
    
    os.makedirs("plots", exist_ok=True) #making plots folder to save charts png file

    with PdfPages("Expense_report.pdf") as pdf:
        # Pie chart of spending by category
        category_totals.plot(kind="pie", autopct="%1.1f%%", startangle=90, figsize=(6,6))
        plt.title("Expenses by Category")
        plt.ylabel("")
        pdf.savefig()
        plt.savefig("plots/expenses_by_category.png", bbox_inches="tight")
        plt.close()

        # Line chart of monthly spending
        max_month = monthly_totals.idxmax()
        max_value = monthly_totals.max()
        plt.plot(monthly_totals.index, monthly_totals.values, marker="o")
        plt.title("Monthly expenses over time")
        plt.xlabel("Months")
        plt.ylabel("Amount $")
        plt.xticks(ticks=range(len(month_order)), labels=month_order ,rotation=45)
        plt.grid(True)
        idx = monthly_totals.index.get_loc(max_month)
        plt.annotate(f"Peak: ${max_value}", xy=(idx, max_value), xytext=(idx, max_value+20), arrowprops=dict(facecolor='red', shrink=0.05))
        plt.subplots_adjust(bottom=0.2) #gives more room at bottom
        pdf.savefig()
        plt.savefig("plots/monthly_expenses.png", bbox_inches="tight")
        plt.close()

        # category comparison bar chart
        ax = category_totals.plot(kind="bar", color="skyblue", figsize=(10,5))
        plt.title("Total Spending per Category")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=20)

        for i, v in enumerate(category_totals):
            ax.text(i, v+50, f"${v:.0f}", ha = 'center')

        plt.tight_layout()
        pdf.savefig()
        plt.savefig("plots/category_totals.png", bbox_inches="tight")
        plt.close()

        # stacked bar showing monthly expenses by category
        expenses_long.pivot(index="Month", columns="Category", values="Amount").plot(kind="bar", stacked=True, figsize=(12,6))
        plt.title("Monthly Expenses by Category")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        pdf.savefig()
        plt.savefig("plots/monthly_expenses_by_category.png", bbox_inches="tight")
        plt.close()


    # if needed, export results to excel/csv files
    with pd.ExcelWriter("Expense_summary.xlsx") as writer:
        pd.DataFrame({"Total": [total], "Average": [avg]}).to_excel(writer, sheet_name="Summary", index=False)
        category_totals.to_frame("Amount").to_excel(writer, sheet_name="Category_totals")
        monthly_totals.to_frame("Amount").to_excel(writer, sheet_name="Monthly Totals")

if __name__ == "__main__":
    main()