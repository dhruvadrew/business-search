from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
from crawling import crawl_and_save_html

app = FastAPI()

# Define the request body model
class UserData(BaseModel):
    user_input: str

@app.post("/crawl")
async def crawl(user_data: UserData):
    try:
        user_input = user_data.user_input
        print(user_input)
        
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
