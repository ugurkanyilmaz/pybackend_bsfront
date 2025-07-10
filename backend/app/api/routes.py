from fastapi import APIRouter, Query
from app.models.product import Product
from app.utils.price_calculator import calculate_price
import json
from pathlib import Path
from app.services.gold_price import get_current_gold_price
from typing import Optional

router = APIRouter()

_products_cache = None
_last_gold_price = None

@router.get("/")
async def root():
    return {"message": "Jewelry Products API is running"}

async def load_products_with_prices():
   
    global _products_cache, _last_gold_price
    
    if _products_cache is None:
        current_gold_price = await get_current_gold_price()
        _last_gold_price = current_gold_price
        print(f"current gold price: ${current_gold_price}/gram (cached)")
        
        file_path = Path(__file__).parent.parent / "data" / "products.json"
        with open(file_path) as f:
            products_raw = json.load(f)

        products = []
        for item in products_raw:
            price = calculate_price(
                popularity_score=item["popularityScore"],
                weight=item["weight"],
                gold_price=current_gold_price
            )
            
            # Create a new product dict with calculated price
            product_with_price = {**item, "price": price}
            products.append(product_with_price)
            print(f"{item['name']} => ${price} (calculated)")
        
        _products_cache = products
        print(f"✅ {len(products)} products cached")

    return _products_cache

@router.get("/products", response_model=list[Product])
async def get_products(
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    min_popularity: Optional[float] = Query(None, description="Minimum popularity score (0-1)"),
    max_popularity: Optional[float] = Query(None, description="Maximum popularity score (0-1)")
):
    """
    Get products with optional filtering (uses cached data after first load):
    - min_price: Filter products with price >= min_price
    - max_price: Filter products with price <= max_price
    - min_popularity: Filter products with popularity >= min_popularity
    - max_popularity: Filter products with popularity <= max_popularity
    """
    #get all products with prices (cached)
    all_products = await load_products_with_prices()

    # Apply filtering
    filtered_products = []
    for product in all_products:
        # Apply filters
        if min_price is not None and product["price"] < min_price:
            continue
        if max_price is not None and product["price"] > max_price:
            continue
        if min_popularity is not None and product["popularityScore"] < min_popularity:
            continue
        if max_popularity is not None and product["popularityScore"] > max_popularity:
            continue
        
        filtered_products.append(product)
    
    print(f"🔍 {len(filtered_products)}/{len(all_products)} ürün filtrelendi")
    return filtered_products

@router.get("/gold-price")
async def gold_price():
    """Get current gold price (uses cached value if available)"""
    global _last_gold_price
    
    if _last_gold_price is None:
        # if cached value is not available, fetch it
        _last_gold_price = await get_current_gold_price()
    
    return {
        "gold_price": _last_gold_price,
        "currency": "USD",
        "unit": "per_gram",
        "cached": True
    }

@router.post("/refresh-cache")
async def refresh_cache():
    """Refresh products cache with new gold price"""
    global _products_cache, _last_gold_price

    # Clear cache
    _products_cache = None
    _last_gold_price = None

    # Reload
    await load_products_with_prices()
    
    return {
        "message": "Cache refreshed successfully",
        "products_count": len(_products_cache),
        "gold_price": _last_gold_price
    }