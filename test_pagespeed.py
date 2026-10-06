from pagespeed_analyzer import analyze_pagespeed


url = input("Enter website URL: ")

result = analyze_pagespeed(url)

print("\n===== PAGESPEED AUDIT =====")

print(f"Performance Score: {result['performance_score']}")
print(f"FCP: {result['fcp']}")
print(f"LCP: {result['lcp']}")
print(f"CLS: {result['cls']}")
print(f"Speed Index: {result['speed_index']}")