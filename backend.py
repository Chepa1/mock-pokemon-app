import os
from supabase import create_client
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

# SUPABASE SETUP
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {SUPABASE_URL[:20]}...") # Only shows first 20 characters
print(f"SUPABASE_KEY: {SUPABASE_KEY[:10]}...") # Only shows first 10 characters

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Test different query approaches
print("Testing queries...")
try:
    # Test 1: Basic select
    result1 = supabase.table("pokemon-data").select("*").execute()
    print(f"Test 1 result count: {len(result1.data)}")
    
    # Test 2: Specific column select
    result2 = supabase.table("pokemon-data").select("Name").execute()
    print(f"Test 2 result count: {len(result2.data)}")
    
    # Test 3: Limited select
    result3 = supabase.table("pokemon-data").select("*").limit(1).execute()
    print(f"Test 3 result count: {len(result3.data)}")
    
except Exception as e:
    print(f"Error during test queries: {str(e)}")
    print(f"Error type: {type(e)}")

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

