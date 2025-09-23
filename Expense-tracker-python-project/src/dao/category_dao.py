# src/dao/categories_dao.py
from typing import List, Dict, Optional
from src.config.supabase_client import get_supabase

class CategoriesDAO:
    def __init__(self):
        self.sb = get_supabase()
        self.table_name = "categories"

    def add_category(self, name: str) -> Optional[Dict]:

        response = self.sb.table(self.table_name).insert({"name": name}).execute()
        return response.data

    def get_category_by_name(self, name: str) -> Optional[Dict]:

        response = self.sb.table(self.table_name).select("*").eq("name", name).execute()
        return response.data[0] if response.data else None

    def delete_category(self, category_id: int) -> Optional[Dict]:

        response = self.sb.table(self.table_name).delete().eq("category_id", category_id).execute()
        return response.data

    def list_categories(self) -> List[Dict]:

        response = self.sb.table(self.table_name).select("*").execute()
        return response.data
