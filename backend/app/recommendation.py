def score_car(car, preferences):
    score = 0
    reasons = []
    weaknesses = []

    budget = preferences.budget
    fuel_type = preferences.fuel_type
    body_type = preferences.body_type
    min_seats = preferences.min_seats
    priority = preferences.priority
    daily_distance = preferences.daily_distance

    # 1. Budget scoring
    if car["price"] <= budget:
        score += 25
        reasons.append("Fits within your budget.")
    else:
        over_budget_percent = ((car["price"] - budget) / budget) * 100

        if over_budget_percent <= 10:
            score += 10
            weaknesses.append("Slightly above your budget.")
        else:
            weaknesses.append("Above your budget.")

    # 2. Fuel type scoring
    if fuel_type == "any":
        score += 10
        reasons.append("Fuel type is flexible based on your preference.")
    elif car["fuel_type"] == fuel_type:
        score += 15
        reasons.append(f"Matches your preferred fuel type: {fuel_type}.")
    else:
        weaknesses.append(f"Does not match your preferred fuel type: {fuel_type}.")

    # 3. Body type scoring
    if body_type == "any":
        score += 10
        reasons.append("Body type is flexible based on your preference.")
    elif car["body_type"] == body_type:
        score += 12
        reasons.append(f"Matches your preferred body type: {body_type}.")
    else:
        weaknesses.append(f"Different body type from your preference: {car['body_type']}.")

    # 4. Seat scoring
    if car["seats"] >= min_seats:
        score += 10
        reasons.append("Has enough seats for your needs.")
    else:
        weaknesses.append("Does not have enough seats for your requirement.")

    # 5. Priority scoring
    if priority == "low_cost":
        score += car["maintenance_cost_score"] * 0.15
        reasons.append("Scored higher because you care about low running and maintenance cost.")

    elif priority == "family":
        score += car["safety_score"] * 0.12
        score += car["comfort_score"] * 0.08
        reasons.append("Scored higher for safety and comfort.")

    elif priority == "performance":
        score += car["performance_score"] * 0.18
        reasons.append("Scored higher for performance.")

    elif priority == "comfort":
        score += car["comfort_score"] * 0.18
        reasons.append("Scored higher for comfort.")

    elif priority == "technology":
        score += car["tech_score"] * 0.18
        reasons.append("Scored higher for technology features.")

    else:
        score += car["safety_score"] * 0.05
        score += car["reliability_score"] * 0.05
        score += car["comfort_score"] * 0.05
        score += car["performance_score"] * 0.05
        reasons.append("Scored using balanced safety, reliability, comfort, and performance.")

    # 6. EV range scoring
    if car["fuel_type"] == "ev":
        weekly_distance = daily_distance * 7

        if car["range_km"] >= weekly_distance:
            score += 8
            reasons.append("EV range is suitable for your weekly driving distance.")
        else:
            weaknesses.append("EV range may be low for your weekly driving distance.")

    final_score = min(round(score), 100)

    return {
        "car": car,
        "score": final_score,
        "reasons": reasons,
        "weaknesses": weaknesses,
    }


def recommend_cars(cars, preferences):
    results = []

    for car in cars:
        result = score_car(car, preferences)
        results.append(result)

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:5]