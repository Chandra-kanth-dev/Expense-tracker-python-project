# src/service/expense_service.py
from datetime import datetime
from typing import List, Dict
from src.dao.expense_dao import ExpenseDAO
from src.dao.monthly_summary_dao import MonthlySummaryDAO

class ExpenseService:
    def __init__(self):
        self.expense_dao = ExpenseDAO()
        self.summary_dao = MonthlySummaryDAO()

    def add_expense(self, user_id: int, category_id: int, amount: float, expense_date: str, salary: float) -> Dict:

        expense_result = self.expense_dao.add_expense(user_id, category_id, amount, expense_date)
        if not expense_result:
            raise RuntimeError("Failed to add expense.")


        dt = datetime.strptime(expense_date, "%Y-%m-%d %H:%M:%S")
        month_year = dt.replace(day=1).strftime("%Y-%m-%d")

        summary_result = self.summary_dao.update_monthly_summary(user_id, month_year, salary)
        if not summary_result:
            raise RuntimeError("Failed to update monthly summary.")

        return {"expense": expense_result[0], "monthly_summary": summary_result[0]}

    def update_expense(self, user_id: int, expense_date: str, new_amount: float, salary: float) -> Dict:
        updated_expense = self.expense_dao.update_expense(user_id, expense_date, new_amount)
        if not updated_expense:
            raise RuntimeError("Failed to update expense.")

        dt = datetime.strptime(expense_date, "%Y-%m-%d %H:%M:%S")
        month_year = dt.replace(day=1).strftime("%Y-%m-%d")

        updated_summary = self.summary_dao.update_monthly_summary(user_id, month_year, salary)
        if not updated_summary:
            raise RuntimeError("Failed to update monthly summary.")

        return {"expense": updated_expense[0], "monthly_summary": updated_summary[0]}

    def delete_expense(self, user_id: int, expense_date: str, salary: float) -> Dict:
        deleted_expense = self.expense_dao.delete_expense(user_id, expense_date)
        if not deleted_expense:
            raise RuntimeError("Failed to delete expense.")

        dt = datetime.strptime(expense_date, "%Y-%m-%d %H:%M:%S")
        month_year = dt.replace(day=1).strftime("%Y-%m-%d")

        updated_summary = self.summary_dao.update_monthly_summary(user_id, month_year, salary)
        if not updated_summary:
            raise RuntimeError("Failed to update monthly summary.")

        return {"expense": deleted_expense[0], "monthly_summary": updated_summary[0]}

    def get_expenses_by_user(self, user_id: int) -> List[Dict]:
        return self.expense_dao.get_expenses_by_user(user_id)

    def get_expenses_by_category(self, user_id: int, category_id: int) -> List[Dict]:
        return self.expense_dao.get_expenses_by_category(user_id, category_id)

    def get_expenses_by_date_range(self, user_id: int, start_date: str, end_date: str) -> List[Dict]:
        return self.expense_dao.get_expenses_by_date_range(user_id, start_date, end_date)
