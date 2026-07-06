from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.sample_data import CARS
from app.schemas import CarPreferences
from app.recommendation import recommend_cars

app = FastAPI(title="AutoMatch Hub API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "AutoMatch Hub API is running",
        "version": "1.0"
    }


@app.get("/cars")
def get_cars():
    return CARS


@app.get("/cars/{car_id}")
def get_car(car_id: int):
    for car in CARS:
        if car["id"] == car_id:
            return car

    return {"error": "Car not found"}


@app.post("/recommend")
def recommend(preferences: CarPreferences):
    recommendations = recommend_cars(CARS, preferences)

    return {
        "preferences": preferences,
        "recommendations": recommendations
    }