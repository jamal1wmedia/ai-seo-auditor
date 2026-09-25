from crawler import fetch_page
from seo_analyzer import analyze_html, find_seo_issues


url = input("Enter website URL: ").strip()

if not url.startswith(("http://", "https://")):
    url = "https://" + url
    
html = fetch_page(url)

result = analyze_html(html)

issues = find_seo_issues(result)


print("\n===== SEO AUDIT =====")

print(f"Title: {result['title']}")
print(f"Meta Description: {result['meta_description']}")
print(f"H1 Count: {result['h1_count']}")
print(f"H2 Count: {result['h2_count']}")
print(f"Images: {result['image_count']}")
print(f"Images Missing ALT: {result['images_missing_alt']}")
print(f"Links: {result['link_count']}")


print("\n===== SEO ISSUES =====")

if not issues:
    print("No issues found!")

else:
    for issue in issues:
        print(f"\n[{issue['severity']}] {issue['issue']}")
        print(f"Recommendation: {issue['recommendation']}")