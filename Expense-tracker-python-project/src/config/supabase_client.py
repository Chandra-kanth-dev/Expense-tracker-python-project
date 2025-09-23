import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

def get_supabase() -> Client:

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials are missing. Check your .env file.")

    return create_client(SUPABASE_URL, SUPABASE_KEY)
