## 🚀 Features

### Backend Features
- **Real-time Gold Price Integration**: Fetches current gold prices from goldapi.io
- **Dynamic Price Calculation**: Calculates product prices based on weight, popularity, and current gold market rates
- **Advanced Filtering**: Filter products by price range and popularity score
- **Caching System**: Optimized performance with in-memory caching and cache refresh endpoint
- **CORS Configuration**: Properly configured for development environments
- **RESTful API**: Clean, documented API endpoints with automatic OpenAPI documentation

### Frontend Features
- **Responsive Design**: Mobile-first Bootstrap 5 implementation
- **Interactive Product Carousel**: Swiper.js powered product showcase
- **Color Picker**: Dynamic gold type selection (Yellow, White, Rose Gold)
- **Star Rating System**: Visual popularity indicators
- **Environment Detection**: Automatic API URL detection for development/production

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for Python
- **Python 3.11** - Latest Python runtime
- **Pydantic** - Data validation and settings management
- **Requests** - HTTP client for external API calls
- **Uvicorn** - ASGI server for production
- **python-dotenv** - Environment variable management

### Frontend
- **Bootstrap 5** - Modern CSS framework
- **Swiper.js** - Touch-enabled slider/carousel
- **Vanilla JavaScript** - No framework dependencies
- **Responsive Design** - Mobile-first approach

### DevOps & Deployment
- **Docker** - Containerization support
- **Render.com** - Cloud deployment platform
- **Git** - Version control

## 📋 Prerequisites

- Python 3.11 or higher
- Node.js 18+ (for frontend development)
- Git
- Gold API key from [goldapi.io](https://goldapi.io/)

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

5. **Start the backend server:**
```powershell
uvicorn app.main:app --reload --port 8000
```

Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```powershell
cd frontend-bootstrap
```

2. **Install dependencies:**
```powershell
npm install
```

3. **Start development server:**
```powershell
npm start
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | `/products` | Get all products with calculated prices | Query filters available |
| POST | `/refresh-cache` | Refresh product cache and gold price | None |
| GET | `/docs` | Interactive API documentation | None |

### Query Parameters

**Price Filtering:**
- `min_price` (float): Minimum price filter
- `max_price` (float): Maximum price filter

**Popularity Filtering:**
- `min_popularity` (float): Minimum popularity score (0-1)
- `max_popularity` (float): Maximum popularity score (0-1)

### Response Format

```json
{
  "products": [
    {
      "id": 1,
      "name": "Diamond Ring",
      "price": 1250.75,
      "weight": 5.2,
      "popularityScore": 0.8,
      "images": {
        "yellow": "image_url",
        "white": "image_url",
        "rose": "image_url"
      }
    }
  ]
}
```

## 🎨 Frontend Features Detail

### Color Picker
- **Yellow Gold**: #E6CA97
- **White Gold**: #D9D9D9  
- **Rose Gold**: #E1A4A9

### Interactive Elements
- **Swiper Carousel**: Touch-enabled product navigation
- **Star Rating**: Visual popularity indicators (1-5 stars)
- **Responsive Grid**: Adapts to different screen sizes
- **Hover Effects**: Enhanced user interaction

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🔍 API Integration Details

### Gold Price Service
- **Provider**: goldapi.io
- **Update Frequency**: Real-time on cache refresh
- **Fallback**: Cached price if API unavailable
- **Rate Limiting**: Handled with caching strategy

### Price Calculation Formula
```
Final Price = (Weight × Gold Price × Popularity Multiplier) + Base Markup
```