# src/service/category_service.py
from typing import List, Dict, Optional
from src.dao.category_dao import CategoriesDAO

class CategoryService:
    def __init__(self):
        self.dao = CategoriesDAO()

    def add_category(self, name: str) -> str:
        existing = self.dao.get_category_by_name(name)
        if existing:
            raise ValueError(f"Category with name '{name}' already exists.")

        result = self.dao.add_category(name)
        if result:
            return f"Category added successfully: {result[0]['name']} (ID: {result[0]['category_id']})"
        else:
            return "Failed to add category."

    def delete_category(self, name: str) -> str:
        existing = self.dao.get_category_by_name(name)
        if not existing:
            raise ValueError(f"Category with name '{name}' not found.")

        result = self.dao.delete_category(existing["category_id"])
        if result:
            return f"Category deleted successfully: {existing['name']} (ID: {existing['category_id']})"
        else:
            return "Failed to delete category."

    def list_categories(self) -> List[str]:
        categories = self.dao.list_categories()
        if not categories:
            return ["No categories found."]
        # Return a readable list of strings
        return [f"ID: {c['category_id']} | Name: {c['name']}" for c in categories]
