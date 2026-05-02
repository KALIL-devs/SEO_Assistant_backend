from typing import Dict, Any, List

def evaluate_page(attributes: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Evaluates extracted attributes against SEO rules.
    Returns a list of issues/statuses.
    """
    results = []

    # Helper to add result
    def add_result(attribute, status, score, priority, message, current_value):
        results.append({
            "attribute": attribute,
            "status": status, # Good, Needs Improvement, Missing
            "score": score,
            "priority": priority, # High, Medium, Low
            "message": message,
            "current_value": current_value
        })

    # 1. Title Tag
    title = attributes.get("title")
    if not title:
        add_result("Title Tag", "Missing", 0, "High", "Title tag is missing.", None)
    elif len(title) < 30:
        add_result("Title Tag", "Needs Improvement", 50, "Medium", "Title is too short (rec: 50-60 chars).", title)
    elif len(title) > 60:
        add_result("Title Tag", "Needs Improvement", 60, "Medium", "Title is too long (rec: 50-60 chars).", title)
    else:
        add_result("Title Tag", "Good", 100, "Low", "Title length is optimal.", title)

    # 2. Meta Description
    meta_desc = attributes.get("meta_description")
    if not meta_desc:
        add_result("Meta Description", "Missing", 0, "High", "Meta description is missing.", None)
    elif len(meta_desc) < 120:
        add_result("Meta Description", "Needs Improvement", 50, "Medium", "Meta description too short.", meta_desc)
    elif len(meta_desc) > 160:
        add_result("Meta Description", "Needs Improvement", 60, "Medium", "Meta description too long.", meta_desc)
    else:
        add_result("Meta Description", "Good", 100, "Low", "Meta description length is optimal.", meta_desc)

    # 3. H1 Tag
    h1_count = attributes.get("h1_count", 0)
    if h1_count == 0:
        add_result("H1 Tag", "Missing", 0, "High", "No H1 tag found.", 0)
    elif h1_count > 1:
        add_result("H1 Tag", "Needs Improvement", 40, "High", "Multiple H1 tags found (should be 1).", h1_count)
    else:
        add_result("H1 Tag", "Good", 100, "Low", "Exactly one H1 tag present.", 1)

    # 4. Word Count
    word_count = attributes.get("word_count", 0)
    if word_count < 300:
        add_result("Word Count", "Needs Improvement", 30, "High", "Content is thin (< 300 words).", word_count)
    else:
        add_result("Word Count", "Good", 100, "Low", "Sufficient content length.", word_count)

    # 5. Missing Alt Text
    missing_alt = attributes.get("missing_alt", 0)
    if missing_alt > 0:
        add_result("Image Alt Text", "Needs Improvement", 50, "Medium", f"{missing_alt} images missing ALT text.", missing_alt)
    else:
        add_result("Image Alt Text", "Good", 100, "Low", "All images have ALT text.", 0)

    # 6. Mobile Friendly
    if attributes.get("mobile_friendly"):
        add_result("Mobile Friendly", "Good", 100, "Low", "Viewport meta tag exists.", "Yes")
    else:
        add_result("Mobile Friendly", "Missing", 0, "High", "No viewport meta tag found.", "No")

    return results
