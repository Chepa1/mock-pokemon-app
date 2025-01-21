import os
from supabase import create_client, Client
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

# SUPABASE SETUP
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my Pokemon filter!"}

