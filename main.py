from crawler import fetch_page
from seo_analyzer import analyze_html, find_seo_issues
from ai_analyzer import analyze_with_ai
from pagespeed_analyzer import analyze_pagespeed


url = input("Enter website URL: ")

# =========================
# 1. CRAWL WEBSITE
# =========================

print("\nAnalyzing website...")

html = fetch_page(url)

# =========================
# 2. TECHNICAL SEO AUDIT
# =========================

result = analyze_html(html)

issues = find_seo_issues(result)

# HTTPS check
if not url.startswith("https://"):
    issues.append({
        "severity": "HIGH",
        "issue": "Website is not using HTTPS",
        "recommendation": "Configure HTTPS and redirect HTTP traffic to the HTTPS version."
    })

# =========================
# 3. PAGESPEED AUDIT
# =========================

print("Running PageSpeed analysis...")

pagespeed = analyze_pagespeed(url)

# =========================
# 4. TECHNICAL SEO REPORT
# =========================

print("\n================================")
print("       TECHNICAL SEO AUDIT")
print("================================")

print(f"URL: {url}")
print(f"Title: {result['title']}")
print(f"Meta Description: {result['meta_description']}")
print(f"H1 Count: {result['h1_count']}")
print(f"H2 Count: {result['h2_count']}")
print(f"Images: {result['image_count']}")
print(f"Images Missing ALT: {result['images_missing_alt']}")
print(f"Images Empty ALT: {result['images_empty_alt']}")
print(f"Links: {result['link_count']}")

print("\n===== SEO ISSUES =====")

if not issues:
    print("No SEO issues found!")
else:
    for issue in issues:
        print(f"\n[{issue['severity']}] {issue['issue']}")
        print(f"Recommendation: {issue['recommendation']}")

# =========================
# 5. PAGESPEED REPORT
# =========================

print("\n================================")
print("         PAGESPEED AUDIT")
print("================================")

print(f"Performance Score: {pagespeed['performance_score']}")
print(f"FCP: {pagespeed['fcp']}")
print(f"LCP: {pagespeed['lcp']}")
print(f"CLS: {pagespeed['cls']}")
print(f"Speed Index: {pagespeed['speed_index']}")

# =========================
# 6. AI SEO ANALYSIS
# =========================

print("\n================================")
print("          AI ANALYSIS")
print("================================")

ai_result = analyze_with_ai(issues, pagespeed)

print(ai_result)