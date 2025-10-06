import sys
import os

from src.services.user_service import UserService
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import streamlit as st
from src.services.user_service import UserService
from src.services.category_service import CategoryService
from src.services.expense_service import ExpenseService
from src.services.monthly_summary_service import MonthlySummaryService

# Initialize services
user_service = UserService()
category_service = CategoryService()
expense_service = ExpenseService()
summary_service = MonthlySummaryService()

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="centered")

st.title("💰 Expense Tracker App")
st.write("Manage your users, categories, and expenses easily!")

menu = st.sidebar.selectbox(
    "Navigate",
    ["Users", "Categories", "Expenses", "Monthly Summary"]
)

if menu == "Users":
    st.header("👤 Manage Users")
    name = st.text_input("Name")
    email = st.text_input("Email")
    city = st.text_input("City")
    if st.button("Add User"):
        user_service.add_user(name, email, city)
        st.success(f"User '{name}' added successfully!")

    if st.button("Show All Users"):
        users = user_service.list_users()
        st.table(users)

elif menu == "Categories":
    st.header("📂 Manage Categories")
    cat_name = st.text_input("Category Name")
    if st.button("Add Category"):
        category_service.add_category(cat_name)
        st.success(f"Category '{cat_name}' added!")

    if st.button("Show Categories"):
        cats = category_service.list_categories()
        st.table(cats)

elif menu == "Expenses":
    st.header("💸 Add Expense")
    user_id = st.text_input("User ID")
    cat_id = st.text_input("Category ID")
    amount = st.number_input("Amount", min_value=0.0)
    date = st.date_input("Date")
    if st.button("Add Expense"):
        expense_service.add_expense(user_id, cat_id, amount, str(date))
        st.success("Expense added successfully!")

elif menu == "Monthly Summary":
    st.header("📅 Monthly Summary")
    user_id = st.text_input("User ID for Summary")
    if st.button("View Summary"):
        summaries = summary_service.get_summary(user_id)
        st.table(summaries)
