from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
from pydantic import BaseModel
from typing import List, Optional

# Import services
from services.crawler import fetch_sitemap_pages
from services.extractor import extract_attributes
from services.evaluator import evaluate_page
from services.ai_generator import generate_suggestion

app = FastAPI(title="AI SEO Optimizer", description="Final Year Project - Page Level SEO Analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class DiscoverRequest(BaseModel):
    url: str

class AnalyzeRequest(BaseModel):
    url: str

class SuggestRequest(BaseModel):
    issue_type: str
    current_value: Optional[str] = ""
    page_context: Optional[str] = ""

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SEO Optimizer API is running"}

@app.post("/api/discover")
def discover_pages(request: DiscoverRequest):
    """
    Discover pages from sitemap or internal links.
    """
    try:
        pages = fetch_sitemap_pages(request.url)
        return {"pages": pages, "count": len(pages)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
def analyze_page(request: AnalyzeRequest):
    """
    Extract attributes and evaluate SEO status.
    """
    try:
        # 1. Extract
        attributes = extract_attributes(request.url)
        if "error" in attributes:
            raise HTTPException(status_code=400, detail=attributes["error"])
        
        # 2. Evaluate
        results = evaluate_page(attributes)
        
        # Calculate overall score (simple average of scores)
        if results:
            total_score = sum(r["score"] for r in results)
            overall_score = round(total_score / len(results))
        else:
            overall_score = 0

        return {
            "attributes": attributes,
            "results": results,
            "overall_score": overall_score
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/suggest")
def get_suggestion(request: SuggestRequest):
    """
    Get AI-generated suggestion for a specific issue.
    """
    try:
        suggestion_data = generate_suggestion(
            request.issue_type, 
            request.current_value, 
            request.page_context
        )
        return suggestion_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PageSpeed Integration
from services.pagespeed import run_audit

class PageSpeedRequest(BaseModel):
    url: str
    strategy: str = "mobile"

@app.post("/api/pagespeed")
def pagespeed_audit(request: PageSpeedRequest):
    """
    Run Google PageSpeed Insights audit.
    """
    print(f"DEBUG: Received PageSpeed request for strategy: {request.strategy}")
    try:
        result = run_audit(request.url, request.strategy)
        return result
    except Exception as e:
        # Pass the error detail up
        raise HTTPException(status_code=500, detail=str(e))
