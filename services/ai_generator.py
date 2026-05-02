import os
import json
import random

def generate_suggestion(issue_type: str, current_value: str, page_content: str = "") -> dict:
    """
    Generates an SEO suggestion.
    Uses a Mock if no API key is set for this academic project.
    """
    
    # MOCK MODE (Deterministic for academic stability)
    # in a real scenario we would call OpenAI/Gemini here
    
    suggestion = ""
    explanation = ""
    reasoning = ""

    if issue_type == "Title Tag":
        suggestion = "Best SEO Tips | Ultimate Guide 2024"
        explanation = "We added relevant keywords and kept it within 60 characters."
        reasoning = "Title tags are the primary relevancy signal for search engines."

    elif issue_type == "Meta Description":
        suggestion = "Learn how to optimize your website for SEO with our comprehensive guide. simple tips to boost your rankings."
        explanation = "Expanded to 150 characters with actionable language."
        reasoning = "Good meta descriptions improve Click-Through-Rate (CTR)."

    elif issue_type == "H1 Tag":
        suggestion = "Complete Guide to SEO Optimization"
        explanation = "Ensure there is exactly one H1 tag that describes the main topic."
        reasoning = "H1 tags help search engines understand the page structure."

    elif issue_type == "Image Alt Text":
        suggestion = "Example: 'Blue running shoes side view'"
        explanation = "Describe the image content specifically."
        reasoning = "Alt text helps screen readers and image search."
        
    else:
        suggestion = "Review this section manually."
        explanation = "Generic improvement advice."
        reasoning = "General best practice."

    return {
        "suggestion": suggestion,
        "explanation": explanation,
        "reasoning": reasoning
    }
