# src/dao/monthly_summary_dao.py
from datetime import datetime
from typing import List, Dict
from src.config.supabase_client import get_supabase

class MonthlySummaryDAO:
    def __init__(self):
        self.sb = get_supabase()
        self.table_name = "monthly_summary"
        self.expense_table = "expenses"
        
    def add_monthly_summary(self, user_id: int, month_year: str, salary: float, expense: float) -> Dict:
        response = self.sb.table(self.table_name).insert({
            "user_id": user_id,
            "month_year": month_year,
            "salary": salary,
            "expense": expense
        }).execute()
        return response.data

    def update_monthly_summary(self, user_id: int, month_year: str, salary: float) -> Dict:

        start_date = datetime.strptime(month_year, "%Y-%m-%d")
        end_month = start_date.month % 12 + 1
        end_year = start_date.year + (start_date.month // 12)
        end_date = datetime(end_year, end_month, 1)


        result = self.sb.table(self.expense_table).select("amount").eq("user_id", user_id)\
                    .gte("expense_date", start_date.isoformat())\
                    .lt("expense_date", end_date.isoformat()).execute()
        
        total_expense = sum([r['amount'] for r in result.data]) if result.data else 0


        existing = self.sb.table(self.table_name).select("*").eq("user_id", user_id).eq("month_year", month_year).execute()

        if existing.data and len(existing.data) > 0:

            resp = self.sb.table(self.table_name).update({
                "salary": salary,
                "expense": total_expense
            }).eq("user_id", user_id).eq("month_year", month_year).execute()
        else:

            resp = self.sb.table(self.table_name).insert({
                "user_id": user_id,
                "month_year": month_year,
                "salary": salary,
                "expense": total_expense
            }).execute()

        return resp.data

    def get_summary(self, user_id: int, month_year: str = None) -> List[Dict]:

        query = self.sb.table(self.table_name).select("*").eq("user_id", user_id)
        if month_year:
            query = query.eq("month_year", month_year)
        result = query.execute()
        return result.data

    def list_all_summaries(self) -> List[Dict]:

        result = self.sb.table(self.table_name).select("*").execute()
        return result.data
    def get_all_summaries(self, user_id: int) -> list[Dict]:
        return (
        self._sb()
        .from_("monthly_summary")
        .select("*")
        .eq("user_id", user_id)
        .execute()
        .data
    )