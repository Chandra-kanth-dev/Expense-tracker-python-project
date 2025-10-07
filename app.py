import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os, sys
from streamlit_lottie import st_lottie
import json
import requests

# Local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from src.services.user_service import UserService
from src.services.category_service import CategoryService
from src.services.expense_service import ExpenseService
from src.services.monthly_summary_service import MonthlySummaryService

# Initialize services
user_service = UserService()
category_service = CategoryService()
expense_service = ExpenseService()
summary_service = MonthlySummaryService()

# Streamlit page setup
st.set_page_config(
    page_title="💰 Expense Tracker",
    page_icon="💵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
def load_css():
    st.markdown("""
    <style>
    /* General look */
    body {
        background: linear-gradient(to right, #e3f2fd, #f3e5f5);
        font-family: "Poppins", sans-serif;
        color: #333333;
    }

    /* Titles and Headers */
    h1, h2, h3, h4 {
        color: #4a148c;
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ede7f6;
        border-right: 2px solid #d1c4e9;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #7b1fa2;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #4a148c;
        transform: scale(1.03);
    }

    /* Metrics cards */
    [data-testid="stMetricValue"] {
        color: #4a148c;
    }

    /* Tabs */
    div[data-baseweb="tab-list"] {
        background-color: #ede7f6;
        border-radius: 12px;
        padding: 5px;
    }

    div[data-baseweb="tab"] {
        font-weight: bold;
        color: #4a148c;
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stDateInput input, .stSelectbox select {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

load_css()

# ---------------- ANIMATIONS ----------------
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

expense_anim = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_6ZpP3f.json")
login_anim = load_lottie_url("https://assets10.lottiefiles.com/private_files/lf30_editor_aqkzj3z5.json")
dashboard_anim = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_jcikwtux.json")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN PAGE ----------------
def login_page():
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("🔐 Welcome to Expense Tracker")
        st.markdown("### Manage your money smartly with insights, graphs, and trends 📊")

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            email = st.text_input("📧 Email")
            if st.button("Login"):
                try:
                    user = user_service.get_user_by_email(email)
                    if user:
                        st.session_state.user = user
                        st.success(f"Welcome back, {user['name']} 👋")
                        st.rerun()
                    else:
                        st.error("No account found with this email.")
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")

        with tab2:
            name = st.text_input("👤 Name")
            email2 = st.text_input("📧 Email for Signup")
            city = st.text_input("🏙️ City (optional)")
            if st.button("Create Account"):
                try:
                    result = user_service.add_user(name, email2, city)
                    if result:
                        st.success(f"Account created successfully for {result[0]['name']} 🎉")
                    else:
                        st.error("Account creation failed.")
                except Exception as e:
                    st.error(f"Signup failed: {str(e)}")

    with col2:
        if login_anim:
            st_lottie(login_anim, height=350, key="login")

# ---------------- DASHBOARD ----------------
def dashboard(user):
    st.sidebar.header(f"👤 {user['name']} | {user['email']}")
    st.sidebar.markdown(f"🏙️ City: {user.get('city', 'Unknown')}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.rerun()

    menu = st.sidebar.radio("📂 Navigation", ["🏠 Overview", "💸 Add Expense", "📊 Analytics"])

    # --- Overview ---
    if menu == "🏠 Overview":
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("🏠 Your Dashboard")
            st.write(f"Welcome, **{user['name']}** 👋 Here's your monthly summary.")
        with col2:
            if dashboard_anim:
                st_lottie(dashboard_anim, height=150, key="dash")

        try:
            summaries = summary_service.dao.get_all_summaries(user["id"])
            if summaries:
                df = pd.DataFrame(summaries)
                total_exp = df["expense"].sum()
                total_sal = df["salary"].sum()
                total_save = df["saving"].sum()

                col1, col2, col3 = st.columns(3)
                col1.metric("💰 Total Salary", f"₹{total_sal:,.2f}")
                col2.metric("💸 Total Expenses", f"₹{total_exp:,.2f}")
                col3.metric("💵 Total Savings", f"₹{total_save:,.2f}")

                st.divider()
                st.subheader("📆 Monthly Trend")
                fig, ax = plt.subplots()
                ax.plot(df["month_year"], df["expense"], marker="o", label="Expenses", linewidth=2)
                ax.plot(df["month_year"], df["salary"], marker="s", label="Salary", linewidth=2)
                ax.plot(df["month_year"], df["saving"], marker="^", label="Savings", linewidth=2)
                ax.legend()
                st.pyplot(fig)
            else:
                st.info("No summary data available yet.")
        except Exception as e:
            st.warning(str(e))

    # --- Add Expense ---
    elif menu == "💸 Add Expense":
        st.title("💸 Add New Expense")
        if expense_anim:
            st_lottie(expense_anim, height=120, key="addexpense")

        try:
            cats = category_service.dao.list_categories()
        except Exception:
            cats = []

        cat_map = {c["name"]: c["category_id"] for c in cats} if cats else {}

        col1, col2, col3, col4 = st.columns(4)
        cat_name = col1.selectbox("📂 Category", list(cat_map.keys()) or ["No categories"])
        amount = col2.number_input("💰 Amount (₹)", min_value=0.0)
        date = col3.date_input("📅 Date", datetime.now())
        salary = col4.number_input("🏦 Monthly Salary (₹)", min_value=0.0)

        if st.button("💾 Save Expense"):
            try:
                expense_service.add_expense(
                    user["id"], cat_map.get(cat_name, None), amount,
                    date.strftime("%Y-%m-%d %H:%M:%S"), salary
                )
                st.success("Expense added successfully ✅")
            except Exception as e:
                st.error(str(e))

    # --- Analytics ---
    elif menu == "📊 Analytics":
        st.title("📊 Expense Analytics")
        try:
            summaries = summary_service.dao.get_all_summaries(user["id"])
            if not summaries:
                st.info("No analytics data found yet.")
            else:
                df = pd.DataFrame(summaries)

                st.subheader("💸 Expense vs Savings Distribution")
                fig1, ax1 = plt.subplots()
                ax1.pie(
                    [df["expense"].sum(), df["saving"].sum()],
                    labels=["Expenses", "Savings"],
                    autopct="%1.1f%%",
                    startangle=90
                )
                st.pyplot(fig1)

                st.subheader("📈 Expense Over Time")
                fig2, ax2 = plt.subplots()
                ax2.bar(df["month_year"], df["expense"], label="Expenses")
                ax2.plot(df["month_year"], df["salary"], label="Salary", color="orange", marker="o")
                ax2.legend()
                st.pyplot(fig2)
        except Exception as e:
            st.error(str(e))

# ---------------- MAIN ----------------
if st.session_state.user is None:
    login_page()
else:
    dashboard(st.session_state.user)
