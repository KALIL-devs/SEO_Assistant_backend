import requests
import json
import os

# You can set this via environment variable or hardcode it (though environment variable is safer)
API_KEY = os.getenv("PAGESPEED_API_KEY", "")
BASE_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

def run_audit(url, strategy="mobile"):
    params = {
        "url": url,
        "key": API_KEY,
        "strategy": strategy,
        "category": ["performance", "seo", "best-practices", "accessibility"]
    }
    
    # If no API key is present, the API might still work with lower quotas, 
    # but it's best to have one.
    if not API_KEY:
        print("Warning: No PAGESPEED_API_KEY found. Requests may be rate-limited.")

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        # Return a structure that indicates error, or raise
        print(f"Error fetching PageSpeed data: {e}")
        if response and response.content:
             print(f"Response content: {response.content}")
        raise e

    lighthouse = data.get("lighthouseResult", {})
    audits = lighthouse.get("audits", {})

    # -------- FIELD DATA (REAL USER DATA / CrUX) --------
    loading_experience = data.get("loadingExperience", {})
    metrics = loading_experience.get("metrics", {})
    
    # Fallback to origin data if page data is missing
    origin_loading_experience = data.get("originLoadingExperience", {})
    origin_metrics = origin_loading_experience.get("metrics", {})

    def get_metric(source_metrics, key):
        return source_metrics.get(key, {}).get("percentile")

    lcp = get_metric(metrics, "LARGEST_CONTENTFUL_PAINT_MS")
    cls = get_metric(metrics, "CUMULATIVE_LAYOUT_SHIFT_SCORE")
    inp = get_metric(metrics, "INTERACTION_TO_NEXT_PAINT")
    field_source = "page"

    if lcp is None and origin_metrics:
        lcp = get_metric(origin_metrics, "LARGEST_CONTENTFUL_PAINT_MS")
        cls = get_metric(origin_metrics, "CUMULATIVE_LAYOUT_SHIFT_SCORE")
        inp = get_metric(origin_metrics, "INTERACTION_TO_NEXT_PAINT")
        field_source = "origin"

    core_web_vitals = {
        "LCP (p75)": lcp,
        "CLS (p75)": cls,
        "INP (p75)": inp,
        "Field Source": field_source
    }

    # -------- LAB DATA (LIGHTHOUSE SIMULATED) --------
    # Helper to safely get displayValue and numericValue
    def get_audit_val(audit_key):
        return audits.get(audit_key, {}).get("displayValue", "N/A")

    lab_metrics = {
        "Performance Score": round(lighthouse.get("categories", {}).get("performance", {}).get("score", 0) * 100),
        "FCP": get_audit_val("first-contentful-paint"),
        "SI": get_audit_val("speed-index"),
        "LCP (Lab)": get_audit_val("largest-contentful-paint"),
        "TBT": get_audit_val("total-blocking-time"),
        "TTI": get_audit_val("interactive"),
        "CLS (Lab)": get_audit_val("cumulative-layout-shift"),
    }

    # -------- OPPORTUNITIES (ACTIONABLE FIXES) --------
    opportunities = []
    for op_key, op_val in audits.items():
        if op_val.get("details", {}).get("type") == "opportunity":
            opportunities.append({
                "title": op_val.get("title"),
                "description": op_val.get("description", ""),
                "estimated_savings": op_val.get("details", {}).get("overallSavingsMs", 0)
            })
    
    # Sort opportunities by savings (descending)
    opportunities.sort(key=lambda x: x["estimated_savings"], reverse=True)

    # -------- DIAGNOSTICS --------
    diagnostics = []
    # "diagnostics" is a specific audit key in lighthouse, but we can also extract general stats
    # The snippet user provided looked at 'diagnostics' audit specifically or constructed it.
    # Let's try to extract key diagnostics like payload size, etc.
    
    diag_audit = audits.get("diagnostics", {})
    diag_details = diag_audit.get("details", {}).get("items", [{}])[0]
    
    diagnostics.append({
        "Total Requests": diag_details.get("numRequests", 0),
        "Total Transfer Size (KB)": round((diag_details.get("transferSize", 0) / 1024), 2),
        "Main Thread Time (ms)": diag_details.get("mainThreadWorkMs", 0),
        "JS Execution Time (ms)": diag_details.get("scriptParseCompileEvaluate"),
        "DOM Nodes": diag_details.get("numNodes", 0)
    })

    # -------- SEO CHECKS --------
    seo_cat = lighthouse.get("categories", {}).get("seo", {})

    def safe_score(audit_name):
        return audits.get(audit_name, {}).get("score")

    seo_checks = {
        "SEO Score": round(seo_cat.get("score", 0) * 100),
        "Title Present": safe_score("document-title"),
        "Meta Description": safe_score("meta-description"),
        "Mobile Friendly": safe_score("viewport"), # viewport is a proxy for mobile friendly basics
        "Links Crawlable": safe_score("is-crawlable"),
        "Valid Status Code": safe_score("http-status-code"),
        "Canonical Tag": safe_score("canonical"),
    }

    # -------- BEST PRACTICES --------
    best_practices_cat = lighthouse.get("categories", {}).get("best-practices", {})
    best_practices = round(best_practices_cat.get("score", 0) * 100)
    
    # Accessibility
    accessibility_cat = lighthouse.get("categories", {}).get("accessibility", {})
    accessibility = round(accessibility_cat.get("score", 0) * 100)


    # -------- SCREENSHOT --------
    final_screenshot = audits.get("final-screenshot", {}).get("details", {}).get("data", None)

    # -------- RESOURCE SUMMARY --------
    # breakdown of resource types (images, scripts, etc.)
    resource_summary = []
    res_items = audits.get("resource-summary", {}).get("details", {}).get("items", [])
    for item in res_items:
        if item.get("label") != "Total": # Skip total, we can calc it or just use specific types
            resource_summary.append({
                "label": item.get("label"),
                "requestCount": item.get("requestCount"),
                "transferSize": item.get("transferSize")
            })

    # -------- METRIC DISTRIBUTIONS (CrUX) --------
    # Extract good/poor/avg percentages if available
    def get_distribution(source_metrics, key):
        dist = source_metrics.get(key, {}).get("distributions", [])
        if not dist: return None
        # Usually [ {min:0, max:2500, proportion: 0.9}, ... ]
        return [
            {"min": d.get("min"), "max": d.get("max"), "proportion": d.get("proportion")}
            for d in dist
        ]

    cwv_distributions = {
        "LCP": get_distribution(metrics, "LARGEST_CONTENTFUL_PAINT_MS"),
        "CLS": get_distribution(metrics, "CUMULATIVE_LAYOUT_SHIFT_SCORE"),
        "INP": get_distribution(metrics, "INTERACTION_TO_NEXT_PAINT"),
    }
    
    # Fill gaps with origin data if needed
    if not cwv_distributions["LCP"] and origin_metrics:
        cwv_distributions = {
            "LCP": get_distribution(origin_metrics, "LARGEST_CONTENTFUL_PAINT_MS"),
            "CLS": get_distribution(origin_metrics, "CUMULATIVE_LAYOUT_SHIFT_SCORE"),
            "INP": get_distribution(origin_metrics, "INTERACTION_TO_NEXT_PAINT"),
        }


    return {
        "strategy": strategy,
        "core_web_vitals": core_web_vitals,
        "cwv_distributions": cwv_distributions,
        "lab_metrics": lab_metrics,
        "opportunities": opportunities,
        "diagnostics": diagnostics,
        "seo_checks": seo_checks,
        "best_practices_score": best_practices,
        "accessibility_score": accessibility,
        "final_screenshot": final_screenshot,
        "resource_summary": resource_summary
    }
