# main.py
from datetime import datetime
from src.services.user_service import UserService
from src.services.category_service import CategoryService
from src.services.expense_service import ExpenseService
from src.services.monthly_summary_service import MonthlySummaryService

user_service = UserService()
category_service = CategoryService()
expense_service = ExpenseService()
summary_service = MonthlySummaryService()


def main_menu():
    print("\n===== Expense Tracker =====")
    print("1. Manage Users")
    print("2. Manage Categories")
    print("3. Manage Expenses")
    print("4. View Monthly Summaries")
    print("0. Exit")
    choice = input("Enter your choice: ")
    return choice.strip()


def users_menu():
    print("\n--- Users Menu ---")
    print("1. Add User")
    print("2. Update User")
    print("3. Delete User")
    print("4. List Users")
    print("0. Back")
    return input("Choice: ").strip()


def categories_menu():
    print("\n--- Categories Menu ---")
    print("1. Add Category")
    print("2. Delete Category")
    print("3. List Categories")
    print("0. Back")
    return input("Choice: ").strip()


def expenses_menu():
    print("\n--- Expenses Menu ---")
    print("1. Add Expense")
    print("2. Update Expense")
    print("3. Delete Expense")
    print("4. View User Expenses")
    print("0. Back")
    return input("Choice: ").strip()

def summaries_menu():
    print("\n--- Monthly Summary Menu ---")
    print("1. View User Summary (per month)")
    print("2. View All Summaries")
    print("3. View Overall Summary (Averages & Totals)")  
    print("0. Back")
    return input("Choice: ").strip()


def run_users():
    while True:
        choice = users_menu()
        try:
            if choice == "1":
                name = input("Enter name: ")
                email = input("Enter email: ")
                city = input("Enter city (optional): ")
                user = user_service.add_user(name, email, city)
                print("Added User:", user)
            elif choice == "2":
                user_id = int(input("Enter user ID to update: "))
                name = input("Enter new name (leave blank to skip): ")
                email = input("Enter new email (leave blank to skip): ")
                city = input("Enter new city (leave blank to skip): ")
                user = user_service.update_user(user_id, name or None, email or None, city or None)
                print("Updated User:", user)
            elif choice == "3":
                user_id = int(input("Enter user ID to delete: "))
                user = user_service.delete_user(user_id)
                print("Deleted User:", user)
            elif choice == "4":
                users = user_service.list_users()
                for u in users:
                    print(u)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)


def run_categories():
    while True:
        choice = categories_menu()
        try:
            if choice == "1":
                name = input("Enter category name: ")
                cat = category_service.add_category(name)
                print("Added Category:", cat)
            elif choice == "2":
                cat_id = int(input("Enter category ID to delete: "))
                cat = category_service.delete_category(cat_id)
                print("Deleted Category:", cat)
            elif choice == "3":
                categories = category_service.list_categories()
                for c in categories:
                    print(c)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)


def run_expenses():
    while True:
        choice = expenses_menu()
        try:
            if choice == "1":
                user_id = int(input("Enter user ID: "))
                category_id = int(input("Enter category ID: "))
                amount = float(input("Enter amount: "))
                date_input = input("Enter date (YYYY-MM-DD HH:MM:SS) or leave blank for now: ")
                expense_date = date_input.strip() or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Get salary for the month from monthly_summary or ask user
                salary = float(input("Enter salary for this month: "))
                result = expense_service.add_expense(user_id, category_id, amount, expense_date, salary)
                print("Expense Added:", result)
            elif choice == "2":
                user_id = int(input("Enter user ID: "))
                date_input = input("Enter expense date to update (YYYY-MM-DD HH:MM:SS): ")
                new_amount = float(input("Enter new amount: "))
                salary = float(input("Enter salary for this month: "))
                result = expense_service.update_expense(user_id, date_input, new_amount, salary)
                print("Expense Updated:", result)
            elif choice == "3":
                user_id = int(input("Enter user ID: "))
                date_input = input("Enter expense date to delete (YYYY-MM-DD HH:MM:SS): ")
                salary = float(input("Enter salary for this month: "))
                result = expense_service.delete_expense(user_id, date_input, salary)
                print("Expense Deleted:", result)
            elif choice == "4":
                user_id = int(input("Enter user ID: "))
                expenses = expense_service.get_expenses_by_user(user_id)
                for e in expenses:
                    print(e)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)



def run_summaries():
    while True:
        choice = summaries_menu()
        try:
            if choice == "1":
                user_id = int(input("Enter user ID: "))
                month_year = input("Enter month (YYYY-MM-01) or leave blank for all: ").strip() or None
                summaries = summary_service.get_summary(user_id, month_year)
                for s in summaries:
                    print(s)
            elif choice == "2":
                summaries = summary_service.list_all_summaries()
                for s in summaries:
                    print(s)
            elif choice == "3":   
                user_id = int(input("Enter user ID: "))
                result = expense_service.get_overall_summary(user_id)
                print("\n--- Overall Summary ---")
                print(f"Months Tracked: {result['months_tracked']}")
                print(f"Total Salary: {result['total_salary']}")
                print(f"Total Expense: {result['total_expense']}")
                print(f"Total Savings: {result['total_savings']}")
                print(f"Average Salary: {result['avg_salary']:.2f}")
                print(f"Average Expense: {result['avg_expense']:.2f}")
                print(f"Average Savings: {result['avg_savings']:.2f}")
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "1":
            run_users()
        elif choice == "2":
            run_categories()
        elif choice == "3":
            run_expenses()
        elif choice == "4":
            run_summaries()
        elif choice == "0":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
