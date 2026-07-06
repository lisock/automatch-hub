from pydantic import BaseModel


class CarPreferences(BaseModel):
    budget: int
    fuel_type: str
    body_type: str
    min_seats: int
    priority: str
    daily_distance: int