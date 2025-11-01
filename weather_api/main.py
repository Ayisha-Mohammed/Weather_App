from fastapi import FastAPI
from pydantic import BaseModel
from weather_api.config import Settings
import httpx,time


app=FastAPI()

class weatherresponse(BaseModel):
     city: str
     country: str
     temperature: float
     feels_like: float
     description: str

     # Simple in-memory cache
cache = {}
CACHE_TTL = 3600


@app.get("/weather/{city}",response_model=weatherresponse)
async def get_weather(city:str):
     if city in cache:
      cached_data = cache[city]
      if time.time() - cached_data["timestamp"] < CACHE_TTL:
        print(" Returning cached data")
        return cached_data["data"]

     """Fetch live weather data for a city using OpenWeatherMap API."""
     url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Settings.OPENWEATHER_API_KEY}&units=metric"
     async with httpx.AsyncClient() as client:
      response = await client.get(url)
      data = response.json()
      
      # Cleaned and simplified response
     result = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "description": data["weather"][0]["description"]
    }
     cache = {"data":result, "timestamp": time.time() }
     return result


