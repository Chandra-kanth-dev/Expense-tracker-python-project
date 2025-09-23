# src/service/users_service.py
from typing import List, Dict, Optional
from src.dao.user_dao import UsersDAO

class UsersService:
    def __init__(self):
        self.dao = UsersDAO()

    def add_user(self, name: str, email: str, city: str = None) -> Dict:
        name = name.strip()
        email = email.strip()
        if not name or not email:
            raise ValueError("Name and email are required.")

        existing_users = self.dao.list_users()
        if any(u['email'].lower() == email.lower() for u in existing_users):
            raise ValueError(f"User with email '{email}' already exists.")

        result = self.dao.add_user(name, email, city)
        if not result:
            raise RuntimeError("Failed to add user.")

        return result[0]

    def update_user(self, user_id: int, name: str = None, email: str = None, city: str = None) -> Dict:
        existing = self.dao.get_user(user_id)
        if not existing:
            raise ValueError(f"User with ID {user_id} not found.")

        update_data = {}
        if name:
            update_data["name"] = name.strip()
        if email:
            update_data["email"] = email.strip()
        if city:
            update_data["city"] = city.strip()

        if not update_data:
            raise ValueError("No fields provided to update.")

        result = self.dao.update_user(user_id, **update_data)
        if not result:
            raise RuntimeError("Failed to update user.")

        return result[0]

    def delete_user(self, user_id: int) -> Dict:
        existing = self.dao.get_user(user_id)
        if not existing:
            raise ValueError(f"User with ID {user_id} not found.")

        result = self.dao.delete_user(user_id)
        if not result:
            raise RuntimeError("Failed to delete user.")

        return result[0]

    def get_user(self, user_id: int) -> Dict:
        user = self.dao.get_user(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return user

    def list_users(self) -> List[Dict]:
        users = self.dao.list_users()
        if not users:
            raise ValueError("No users found.")
        return users
