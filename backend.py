import os
from supabase.client import create_client
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

@app.get("/letter_filter/{filter_type}/{letter}")
async def letter_filter(filter_type: str, letter: str):
    try:
        letter = letter.upper()
        result = supabase.table("pokemon-data").select("*").execute()
        
        # Filter Pokemon based on selected criteria
        if filter_type == "Starts with":
            filtered_data = [p for p in result.data if p['Name'].upper().startswith(letter)]
        elif filter_type == "Contains":
            filtered_data = [p for p in result.data if letter in p['Name'].upper()]
        elif filter_type == "Ends with":
            filtered_data = [p for p in result.data if p['Name'].upper().endswith(letter)]
        
        return filtered_data
    except Exception as e:
        print(f"Error in backend: {str(e)}")
        raise e

