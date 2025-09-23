# src/service/category_service.py
from typing import List, Dict, Optional
from src.dao.category_dao import CategoriesDAO

class CategoryService:
    def __init__(self):
        self.dao = CategoriesDAO()
    def add_category(self, name: str) -> Optional[Dict]:
        existing = self.dao.get_category_by_name(name)
        if existing:
            raise ValueError(f"Category with name '{name}' already exists.")
        
        return self.dao.add_category(name)

    def delete_category(self, name: str) -> Optional[Dict]:
        existing = self.dao.get_category_by_name(name)
        if not existing:
            raise ValueError(f"Category with name '{name}' not found.")

        return self.dao.delete_category(existing["category_id"])

    def list_categories(self) -> List[Dict]:
        categories = self.dao.list_categories()
        if not categories:
            raise ValueError("No categories found.")
        return categories
