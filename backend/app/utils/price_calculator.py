

def calculate_price(popularity_score: float, weight: float, gold_price: float) -> float:
    return round((popularity_score + 1) * weight * gold_price)
