from src.config.supabase_client import get_supabase

class ExpenseDAO:
    def __init__(self):
        self.sb = get_supabase()

    def add_expense(self, user_id: int, category_id: int, amount: float, expense_date):

        return self.sb.table('expenses').insert({
            'user_id': user_id,
            'expense_date': expense_date,
            'category_id': category_id,
            'amount': amount,
            
        }).execute()

    def update_expense(self, user_id: int, expense_date, new_amount: float):

        return self.sb.table('expenses') .update({'amount': new_amount}) .eq('user_id', user_id) .eq('expense_date', expense_date) .execute()

    def delete_expense(self, user_id: int, expense_date):

        return self.sb.table('expenses') \
            .delete() \
            .eq('user_id', user_id) \
            .eq('expense_date', expense_date) \
            .execute()

    def get_expenses_by_user(self, user_id: int):
 
        return self.sb.table('expenses') \
            .select('*') \
            .eq('user_id', user_id) \
            .execute()

    def get_expenses_by_category(self, user_id: int, category_id: int):

        return self.sb.table('expenses') \
            .select('*') \
            .eq('user_id', user_id) \
            .eq('category_id', category_id) \
            .execute()

    def get_expenses_by_date_range(self, user_id: int, start_date, end_date):

        return self.sb.table('expenses') \
            .select('*') \
            .eq('user_id', user_id) \
            .gte('expense_date', start_date) \
            .lte('expense_date', end_date) \
            .execute()
