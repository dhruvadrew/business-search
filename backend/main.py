from fastapi import FastAPI
from fastapi.responses import JSONResponse
from databases import Database
from pydantic import BaseModel
import asyncio
from fastapi import HTTPException
from crawling import crawl_and_save_html
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")
key = os.getenv("DATABASE_KEY")

app = FastAPI()

supabase: Client = create_client(url, key)

table = supabase.table("businesses")

@app.get("/business/{business_name}")
async def get_business_info(business_name: str):
    query = f"SELECT * FROM businesses WHERE name = :name"
    result = await table.fetch_one(query, values={"name": business_name})
    
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Business not found")

# Define the request body model
class UserData(BaseModel):
    user_input: str

@app.post("/crawl")
async def crawl(user_data: UserData):
    try:
        user_input = user_data.user_input
        
        # Run the async crawling function
        await crawl_and_save_html(user_input)
        
        # Return success response
        return JSONResponse(content={"message": "Crawl successful"}, status_code=200)
    except Exception as e:
        # Return error response if the process fails
        return JSONResponse(content={"message": "Crawl failed", "error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
