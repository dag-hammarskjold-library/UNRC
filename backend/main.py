from fastapi import FastAPI
import aiohttp
import asyncio
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import json
from fastapi.middleware.cors import CORSMiddleware


# Instantiate the FastAPI app
app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (or replace with ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# API Response Model
class APIResponse(BaseModel):
    url: HttpUrl
    response: Optional[str] = None
    error: Optional[str] = None

# List of APIs
API_ENDPOINTS = [
    "https://randomuser.me/api/",
    "https://ipinfo.io/json",
    "https://api.coindesk.com/v1/bpi/currentprice.json",
    "https://api.exchangerate-api.com/v4/latest/USD",
    "https://api.spacexdata.com/v4/launches/latest",
    "https://dog.ceo/api/breeds/image/random",
    "https://catfact.ninja/fact",
    "https://official-joke-api.appspot.com/random_joke",
    "https://api.open-meteo.com/v1/forecast?latitude=40.71&longitude=-74.01&current_weather=true",
    "https://api.chucknorris.io/jokes/random",
    "https://pokeapi.co/api/v2/pokemon/ditto",
    "https://api.adviceslip.com/advice",
    "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY",
    "https://api.kanye.rest/",
    "https://api.publicapis.org/entries",
    "https://www.boredapi.com/api/activity",
    "https://api.agify.io?name=michael",
    "https://api.genderize.io?name=michael",
    "https://api.nationalize.io?name=michael",
    "https://openlibrary.org/api/books?bibkeys=ISBN:0451526538&format=json&jscmd=data",
]

# Async function to fetch API data
async def fetch_api(session: aiohttp.ClientSession, url: str) -> APIResponse:
    try:
        async with session.get(url, timeout=5) as response:
            if response.status != 200:
                return APIResponse(url=url, error=f"HTTP {response.status} - {response.reason}")

            data = await response.text()
            return APIResponse(url=url, response=data)

    except asyncio.TimeoutError:
        return APIResponse(url=url, error="Request timed out")
    except aiohttp.ClientError as e:
        return APIResponse(url=url, error=f"Network error: {str(e)}")

# Endpoint to fetch all APIs
@app.get("/fetch-apis", response_model=List[APIResponse])
async def fetch_all_apis():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_api(session, url) for url in API_ENDPOINTS]
        return await asyncio.gather(*tasks)
    
@app.get("/")
def home():
    return {"message": "Welcome to the Common Research API Fetcher! Use /fetch-apis to get data."}

# Run the server: uvicorn main:app --reload
