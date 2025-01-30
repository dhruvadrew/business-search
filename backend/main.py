from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# ✅ Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],  # Allow only your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

supabase: Client = create_client(url, key)

table = supabase.table("businesses")

# Define request model
class BusinessNamesRequest(BaseModel):
    names: list[str]  # ✅ Ensures input is a JSON array

@app.post("/businesses")
async def get_multiple_businesses(request: BusinessNamesRequest):
    results = []
    print("Received names:", request.names)

    for name in request.names:
        response = supabase.table("businesses").select("*").eq("name", name).execute()
        
        # Extract data from Supabase response
        data = response.data
        if data:
            results.extend(data)  # Append results if found

    if not results:
        return JSONResponse(content={"detail": "No businesses found"}, status_code=404)

    return results

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
        names = await crawl_and_save_html(user_input)
        
        # Return success response
        return JSONResponse(content={"message": "Crawl successful", "names": names}, status_code=200)
    except Exception as e:
        # Return error response if the process fails
        return JSONResponse(content={"message": "Crawl failed", "error": str(e)}, status_code=500)
    
@app.get("/business/{business_name}")
async def get_business_info(business_name: str):
    response = table.select("*").eq("name", business_name).execute()
    
    if response.data:
        return response.data[0]  # Return the first matching business
    else:
        raise HTTPException(status_code=404, detail="Business not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
