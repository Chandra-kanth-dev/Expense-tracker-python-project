# app.py - Expense Tracker SmartLit Application

from smartlit import SmartLitApp, Page, Component

class ExpenseCard(Component):
    def __init__(self, category, amount, date):
        self.category = category
        self.amount = amount
        self.date = date

    def render(self):
        return f"""
        <div style='background:white;padding:16px;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.05);margin-bottom:12px;display:flex;justify-content:space-between;'>
            <div>
                <div style='font-weight:bold;color:#2196f3;'>{self.category}</div>
                <div>{self.date}</div>
            </div>
            <div style='font-weight:bold;color:#4CAF50;'>₹{self.amount}</div>
        </div>
        """


class ExpenseTrackerApp(SmartLitApp):
    def __init__(self):
        super().__init__(title="Expense Tracker")
        self.expenses = [
            {"category": "Food", "amount": 450, "date": "2025-10-05"},
            {"category": "Transport", "amount": 120, "date": "2025-10-04"}
        ]

    def dashboard(self):
        total_expense = sum(e['amount'] for e in self.expenses)
        savings = 5000 - total_expense

        return f"""
        <h2>Dashboard</h2>
        <div style='margin-bottom:12px;'>
            <div style='padding:16px;background:white;border-radius:12px;'>
                <strong>Total Expenses:</strong> ₹{total_expense}
            </div>
        </div>
        <div style='margin-bottom:12px;'>
            <div style='padding:16px;background:white;border-radius:12px;'>
                <strong>Savings:</strong> ₹{savings}
            </div>
        </div>
        """

    def expenses_page(self):
        cards_html = "".join(
            ExpenseCard(e['category'], e['amount'], e['date']).render()
            for e in self.expenses
        )
        return f"""
        <h2>Expenses</h2>
        {cards_html}
        """

    def render(self):
        return Page("Dashboard", self.dashboard), Page("Expenses", self.expenses_page)


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()