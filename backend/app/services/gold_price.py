import os
import requests
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

FALLBACK_PRICE = 75.5  # USD/gram (varsayılan)

async def get_current_gold_price() -> float:
   
    api_key = os.getenv("GOLDAPI_KEY")
    symbol = os.getenv("GOLDAPI_SYMBOL", "XAU")
    curr = os.getenv("GOLDAPI_CURRENCY", "USD")
    date = ""
    base_url = os.getenv("GOLDAPI_URL", "https://www.goldapi.io/api")

    url = f"{base_url}/{symbol}/{curr}{date}"
    headers = {
        "x-access-token": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5.0)
        response.raise_for_status()
        
        data = response.json()
        # from the JSON response, extract the gold price for 24K gold
        gold_price = data.get("price_gram_24k", FALLBACK_PRICE)
        print(f"Güncel altın fiyatı: {gold_price} USD/gram")
        
        return float(gold_price)
        
    except requests.exceptions.RequestException as e:
        print(f"couldnt fetch gold price: {e}")
        return FALLBACK_PRICE
    except (KeyError, ValueError) as e:
        print(f"JSON parse error: {e}")
        return FALLBACK_PRICE