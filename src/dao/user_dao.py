# src/dao/users_dao.py
import email
from typing import Optional, List, Dict
from urllib import response
from src.config.supabase_client import get_supabase

class UserDAO:
    def __init__(self):
        self.sb = get_supabase()
        self.table_name = "users"

    def add_user(self, name: str, email: str, city: str = None) -> Optional[Dict]:
        pay_load={"name": name, "email": email, "city": city}
        response = self.sb.table(self.table_name).insert(pay_load).execute()
        return response.data

    def update_user(self, user_id: int, name: str = None, email: str = None, city: str = None) -> Optional[Dict]:

        update_data = {}
        if name:
            update_data["name"] = name
        if email:
            update_data["email"] = email
        if city:
            update_data["city"] = city

        if not update_data:
            return None  # Nothing to update

        response = self.sb.table(self.table_name).update(update_data).eq("id", user_id).execute()
        return response.data

    def delete_user(self, user_id: int) -> Optional[Dict]:

        response = self.sb.table(self.table_name).delete().eq("id", user_id).execute()
        return response.data

    def get_user(self, user_id: int) -> Optional[Dict]:
        response = self.sb.table(self.table_name).select("*").eq("id", user_id).execute()
        return response.data[0] if response.data else None

    def list_users(self) -> List[Dict]:

        response = self.sb.table(self.table_name).select("*").execute()
        return response.data
    def get_user_by_email(self, email: str):
        response = self.sb.table(self.table_name).select("*").eq("email", email).execute()
        return response.data[0] if response.data else None

