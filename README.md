# SEO Assistant - Backend API

A FastAPI-based REST API for comprehensive website SEO analysis. This backend service provides page discovery, SEO evaluation, AI-powered suggestions, and PageSpeed metrics analysis.

**Frontend Repository:** [SEO Assistant Frontend](https://github.com/KALIL-devs/SEO_Assistant_frontend.git)

## Features

### 🔍 Website Crawling
- Automatic sitemap.xml discovery and parsing
- Fallback to homepage link crawling
- Handles large sitemaps with configurable limits
- Browser user-agent to bypass basic WAF protections

### 📊 SEO Analysis Engine
- **Title Tag Validation** - Length, content, keyword analysis
- **Meta Description Checks** - Character count, content quality
- **H1 Tag Analysis** - Presence, uniqueness, relevance
- **Open Graph Tags** - Social media optimization
- **Structured Data** - Schema.org validation
- **Mobile Optimization** - Responsive design checks
- **Page Performance** - Speed and Core Web Vitals

### 🤖 AI Suggestions
- Context-aware content recommendations
- Optimized title tag generation
- Meta description creation
- Heading hierarchy improvements
- Content suggestions based on page context

### ⚡ PageSpeed Integration
- Google PageSpeed Insights API integration
- Core Web Vitals metrics
- Mobile and desktop performance scores
- Actionable performance recommendations

## Technology Stack

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI application server
- **Pydantic** - Data validation and serialization
- **BeautifulSoup4** - HTML/XML parsing
- **Requests** - HTTP client library
- **SQLAlchemy** - ORM for database operations
- **python-dotenv** - Environment variable management

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd seo-assistant-backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   cp .env.example .env
   ```

5. **Update environment variables:**
   ```env
   # Backend Configuration
   API_BASE_URL=http://localhost:8000
   CORS_ORIGINS=http://localhost:5173,http://localhost:3000

   # Optional: Google PageSpeed API
   PAGESPEED_API_KEY=your_api_key_here

   # Optional: AI Services
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

### Development Server
```bash
uvicorn main:app --reload
```
- The API will be available at `http://localhost:8000`
- Auto-reload enabled for development changes
- Interactive API documentation at `http://localhost:8000/docs`

### Production Server
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Health Check
```
GET /
Response: {"status": "ok", "message": "SEO Optimizer API is running"}
```

### Discover Pages
```
POST /api/discover
Request Body:
{
  "url": "https://example.com"
}

Response:
{
  "pages": [
    "https://example.com",
    "https://example.com/about",
    "https://example.com/services"
  ],
  "count": 3
}
```

### Analyze Page
```
POST /api/analyze
Request Body:
{
  "url": "https://example.com/page"
}

Response:
{
  "url": "https://example.com/page",
  "results": [
    {
      "attribute": "Title Tag",
      "status": "Good",
      "score": 100,
      "priority": "High",
      "message": "Title length is optimal.",
      "current_value": "Your Page Title"
    },
    {
      "attribute": "Meta Description",
      "status": "Needs Improvement",
      "score": 60,
      "priority": "High",
      "message": "Meta description is too short (rec: 150-160 chars).",
      "current_value": "Short description"
    }
  ],
  "overall_score": 75
}
```

### Generate AI Suggestion
```
POST /api/suggest
Request Body:
{
  "issue_type": "Title Tag",
  "current_value": "Current Title",
  "page_context": "Page about SEO optimization"
}

Response:
{
  "suggestion": "Best SEO Tips | Ultimate Guide 2024",
  "explanation": "We added relevant keywords and kept it within 60 characters.",
  "reasoning": "Title tags are the primary relevancy signal for search engines."
}
```

### PageSpeed Analysis
```
POST /api/pagespeed
Request Body:
{
  "url": "https://example.com/page"
}

Response:
{
  "url": "https://example.com/page",
  "desktop_score": 85,
  "mobile_score": 78,
  "core_web_vitals": {
    "LCP": 2.5,
    "FID": 100,
    "CLS": 0.1
  },
  "metrics": { ... }
}
```

## Project Structure

```
backend/
├── main.py                    # FastAPI application & routes
├── requirements.txt           # Python dependencies
├── debug_pagespeed.py        # PageSpeed debugging utilities
├── test_pagespeed_strategy.py # Unit tests
├── services/
│   ├── __init__.py
│   ├── crawler.py            # Website discovery & crawling
│   ├── extractor.py          # HTML attribute extraction
│   ├── evaluator.py          # SEO rule evaluation
│   ├── ai_generator.py       # AI suggestion generation
│   └── pagespeed.py          # PageSpeed API integration
├── .env                       # Environment variables (not in git)
└── README.md                  # This file
```

## Service Modules

### crawler.py
Handles website discovery and page fetching:
- `fetch_sitemap_pages(base_url)` - Extract URLs from sitemap.xml
- `crawl_homepage_links(base_url)` - Fallback link extraction from homepage
- Configurable timeout and size limits
- Browser-like user-agent headers

### extractor.py
Extracts SEO attributes from HTML:
- `extract_attributes(html)` - Parse page HTML for SEO elements
- Retrieves: title, meta description, H1, Open Graph tags, canonical URL
- Structured data extraction
- Error handling for malformed HTML

### evaluator.py
Evaluates extracted attributes against SEO best practices:
- `evaluate_page(attributes)` - Score page against SEO rules
- Returns issues with severity levels
- Provides actionable improvement messages
- Scoring system (0-100)

### ai_generator.py
Generates AI-powered SEO suggestions:
- `generate_suggestion(issue_type, current_value, page_context)` - Create suggestions
- Mock mode for academic stability
- Ready for integration with ChatGPT/Gemini APIs
- Context-aware recommendations

### pagespeed.py
Integrates with Google PageSpeed Insights:
- `get_pagespeed_metrics(url)` - Fetch performance data
- Mobile and desktop scores
- Core Web Vitals metrics
- Opportunity analysis

## Configuration

### Environment Variables

```env
# API Configuration
API_BASE_URL=http://localhost:8000
DEBUG=True

# CORS Settings
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:8080

# External APIs
PAGESPEED_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key

# Database (optional)
DATABASE_URL=sqlite:///./seo_analysis.db

# Crawler Settings
CRAWLER_TIMEOUT=10
SITEMAP_SIZE_LIMIT=5242880  # 5MB
```

## Development

### Running Tests
```bash
pytest test_pagespeed_strategy.py -v
```

### Code Style
```bash
# Format code
black services/ main.py

# Lint
flake8 services/ main.py

# Type checking
mypy services/ main.py
```

### Debugging
```bash
python debug_pagespeed.py
```

## Performance Considerations

- **Caching**: Implement Redis for sitemap and analysis caching
- **Async Processing**: Consider background tasks for large site audits
- **Rate Limiting**: Implement rate limiting for API endpoints
- **Database**: Use database for storing analysis history
- **Batch Processing**: Support batch URL analysis jobs

## Security

- CORS configured for frontend integration
- Input validation using Pydantic models
- Error handling without exposing sensitive information
- Rate limiting recommended for production
- Environment variables for sensitive data

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - CORS_ORIGINS=http://localhost:5173
    volumes:
      - ./backend:/app
```

### Cloud Deployment
- **Heroku**: `git push heroku main`
- **AWS Lambda**: Configure as serverless function
- **Google Cloud Run**: Container-based deployment
- **DigitalOcean**: App Platform or Droplet

## Dependencies

| Package | Purpose |
|---------|---------|
| fastapi | Web framework |
| uvicorn | ASGI server |
| requests | HTTP client |
| beautifulsoup4 | HTML parsing |
| pydantic | Data validation |
| sqlalchemy | ORM |
| python-multipart | Form data handling |
| python-dotenv | Environment configuration |

## Troubleshooting

### Common Issues

**Issue:** "Connection refused" to localhost:8000
- **Solution:** Ensure backend is running: `uvicorn main:app --reload`

**Issue:** CORS errors from frontend
- **Solution:** Check `CORS_ORIGINS` in environment matches frontend URL

**Issue:** Sitemap parsing fails
- **Solution:** Verify sitemap.xml is valid XML and URL is accessible

**Issue:** PageSpeed API errors
- **Solution:** Verify `PAGESPEED_API_KEY` is valid and has proper permissions

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## Future Enhancements

- [ ] Database integration for analysis history
- [ ] Real-time WebSocket updates for long-running analysis
- [ ] Advanced AI integration (ChatGPT/Gemini API)
- [ ] Batch audit scheduling
- [ ] Webhook notifications
- [ ] Authentication and user management
- [ ] Multi-language support
- [ ] Custom SEO rule configuration

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Backend API for SEO Assistant - Optimize your website with confidence! 🚀**
