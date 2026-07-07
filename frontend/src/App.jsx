import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = "/api";

function App() {
  const [formData, setFormData] = useState({
    budget: 160000,
    fuel_type: "ev",
    body_type: "suv",
    min_seats: 5,
    priority: "technology",
    daily_distance: 40,
  });

  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData({
      ...formData,
      [name]: name === "budget" || name === "min_seats" || name === "daily_distance"
        ? Number(value)
        : value,
    });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/recommend`, formData);
      setRecommendations(response.data.recommendations);
    } catch (error) {
      console.error("Error getting recommendations:", error);
      alert("Could not get recommendations. Make sure the backend is running.");
    }

    setLoading(false);
  }

  return (
    <div className="app">
      <header className="hero">
        <h1>AutoMatch Hub</h1>
        <p>Find the car that actually fits your life.</p>
      </header>

      <main className="container">
        <section className="card">
          <h2>Car Recommendation Quiz</h2>

          <form onSubmit={handleSubmit} className="quiz-form">
            <label>
              Maximum Budget
              <input
                type="number"
                name="budget"
                value={formData.budget}
                onChange={handleChange}
              />
            </label>

            <label>
              Fuel Type
              <select
                name="fuel_type"
                value={formData.fuel_type}
                onChange={handleChange}
              >
                <option value="any">Any</option>
                <option value="petrol">Petrol</option>
                <option value="diesel">Diesel</option>
                <option value="hybrid">Hybrid</option>
                <option value="ev">Electric</option>
              </select>
            </label>

            <label>
              Body Type
              <select
                name="body_type"
                value={formData.body_type}
                onChange={handleChange}
              >
                <option value="any">Any</option>
                <option value="sedan">Sedan</option>
                <option value="suv">SUV</option>
                <option value="hatchback">Hatchback</option>
                <option value="pickup">Pickup</option>
                <option value="coupe">Coupe</option>
              </select>
            </label>

            <label>
              Minimum Seats
              <input
                type="number"
                name="min_seats"
                value={formData.min_seats}
                onChange={handleChange}
              />
            </label>

            <label>
              Main Priority
              <select
                name="priority"
                value={formData.priority}
                onChange={handleChange}
              >
                <option value="balanced">Balanced</option>
                <option value="low_cost">Low running cost</option>
                <option value="family">Family and safety</option>
                <option value="performance">Performance</option>
                <option value="comfort">Comfort</option>
                <option value="technology">Technology</option>
              </select>
            </label>

            <label>
              Daily Driving Distance, km
              <input
                type="number"
                name="daily_distance"
                value={formData.daily_distance}
                onChange={handleChange}
              />
            </label>

            <button type="submit">
              {loading ? "Finding cars..." : "Find My Car"}
            </button>
          </form>
        </section>

        <section className="results">
          {recommendations.map((item) => (
            <div key={item.car.id} className="car-card">
              <div className="car-header">
                <h2>
                  {item.car.brand} {item.car.model} {item.car.year}
                </h2>
                <span className="score">{item.score}% match</span>
              </div>

              <p>{item.car.description}</p>

              <div className="car-details">
                <span>Price: {item.car.price}</span>
                <span>Fuel: {item.car.fuel_type}</span>
                <span>Body: {item.car.body_type}</span>
                <span>Seats: {item.car.seats}</span>
                <span>Range: {item.car.range_km} km</span>
                <span>HP: {item.car.horsepower}</span>
              </div>

              <h3>Why it matches you</h3>
              <ul>
                {item.reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>

              <h3>Possible weaknesses</h3>
              <ul>
                {item.weaknesses.map((weakness, index) => (
                  <li key={index}>{weakness}</li>
                ))}
              </ul>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}

export default App;