# src/service/monthly_summary_service.py
from typing import List, Dict
from datetime import datetime
from src.dao.monthly_summary_dao import MonthlySummaryDAO
from src.dao.expense_dao import ExpenseDAO

class MonthlySummaryService:
    def __init__(self):
        self.dao = MonthlySummaryDAO()
        self.expense_dao = ExpenseDAO()

    def add_summary(self, user_id: int, month_year: str, salary: float) -> Dict:

        start_date = datetime.strptime(month_year, "%Y-%m-%d")
        end_month = start_date.month % 12 + 1
        end_year = start_date.year + (start_date.month // 12)
        end_date = datetime(end_year, end_month, 1)

        result = self.expense_dao.get_expenses_by_date_range(
            user_id,
            start_date.strftime("%Y-%m-%d %H:%M:%S"),
            end_date.strftime("%Y-%m-%d %H:%M:%S")
        )
        total_expense = sum([r['amount'] for r in result]) if result else 0


        summary = self.dao.add_monthly_summary(user_id, month_year, salary, total_expense)
        if not summary:
            raise RuntimeError("Failed to add monthly summary.")
        return summary[0]

    def update_summary(self, user_id: int, month_year: str, salary: float) -> Dict:

        updated_summary = self.dao.update_monthly_summary(user_id, month_year, salary)
        if not updated_summary:
            raise RuntimeError("Failed to update monthly summary.")
        return updated_summary[0]

    def get_summary(self, user_id: int, month_year: str = None) -> List[Dict]:

        summaries = self.dao.get_summary(user_id, month_year)
        if not summaries:
            raise ValueError("No monthly summary found.")
        return summaries

    def list_all_summaries(self) -> List[Dict]:
        summaries = self.dao.list_all_summaries()
        if not summaries:
            raise ValueError("No monthly summaries found.")
        return summaries
    
    def get_overall_summary(self, user_id: int) -> Dict:

        all_summaries = self.dao.get_all_summaries(user_id)
        if not all_summaries:
            raise RuntimeError("No monthly summaries found for this user.")

        total_salary = sum(row["salary"] for row in all_summaries)
        total_expense = sum(row["total_expense"] for row in all_summaries)
        total_savings = sum(row["savings"] for row in all_summaries)
        months = len(all_summaries)

        avg_salary = total_salary / months
        avg_expense = total_expense / months
        avg_savings = total_savings / months

        return {
            "total_salary": total_salary,
            "total_expense": total_expense,
            "total_savings": total_savings,
            "avg_salary": avg_salary,
            "avg_expense": avg_expense,
            "avg_savings": avg_savings,
            "months_tracked": months
        }