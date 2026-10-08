import os

import requests
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("PAGESPEED_API_KEY")


def analyze_pagespeed(url):

    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    params = {
        "url": url,
        "key": api_key,
        "strategy": "mobile"
    }

   
    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = requests.get(
                endpoint,
                params=params,
                timeout=60
            )

            if response.status_code == 200:
                break

            if response.status_code in [500, 502, 503, 504]:

                print(
                    f"\nPageSpeed temporary error "
                    f"({response.status_code}). "
                    f"Retry {attempt + 1}/{max_retries}..."
                )

                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue

            print("\n===== PAGESPEED API ERROR =====")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

            raise Exception("PageSpeed API request failed")

        except requests.RequestException as e:

            if attempt < max_retries - 1:
                print(
                    f"\nPageSpeed connection error. "
                    f"Retry {attempt + 1}/{max_retries}..."
                )

                time.sleep(5)
                continue

            raise e

    if response.status_code != 200:
        print("\n===== PAGESPEED API ERROR =====")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        raise Exception("PageSpeed API request failed")

    data = response.json()

    lighthouse = data["lighthouseResult"]
    categories = lighthouse["categories"]
    audits = lighthouse["audits"]

    performance_score = (
        categories["performance"]["score"] * 100
        if categories["performance"]["score"] is not None
        else None
    )

    fcp_value = audits["first-contentful-paint"]["numericValue"]
    lcp_value = audits["largest-contentful-paint"]["numericValue"]
    cls_value = audits["cumulative-layout-shift"]["numericValue"]
    speed_index_value = audits["speed-index"]["numericValue"]

    return {
        "performance_score": performance_score,

        "fcp": audits["first-contentful-paint"]["displayValue"],
        "fcp_value": fcp_value,

        "lcp": audits["largest-contentful-paint"]["displayValue"],
        "lcp_value": lcp_value,

        "cls": audits["cumulative-layout-shift"]["displayValue"],
        "cls_value": cls_value,

        "speed_index": audits["speed-index"]["displayValue"],
        "speed_index_value": speed_index_value,
    }


def find_pagespeed_issues(pagespeed):

    issues = []

    # Performance Score
    score = pagespeed["performance_score"]

    if score is not None:

        if score < 50:
            issues.append({
                "severity": "HIGH",
                "issue": f"Poor PageSpeed performance score ({score}/100)",
                "recommendation": "Improve page loading performance, rendering, resource delivery, and server response time."
            })

        elif score < 90:
            issues.append({
                "severity": "MEDIUM",
                "issue": f"PageSpeed performance needs improvement ({score}/100)",
                "recommendation": "Optimize critical resources and improve loading performance."
            })

    # FCP
    fcp = pagespeed["fcp_value"] / 1000

    if fcp > 3:
        issues.append({
            "severity": "HIGH",
            "issue": f"Poor First Contentful Paint ({fcp:.1f}s)",
            "recommendation": "Reduce render-blocking resources, improve server response time, and optimize critical rendering resources."
        })

    elif fcp > 1.8:
        issues.append({
            "severity": "MEDIUM",
            "issue": f"FCP needs improvement ({fcp:.1f}s)",
            "recommendation": "Optimize critical CSS, JavaScript, fonts, and server response time."
        })

    # LCP
    lcp = pagespeed["lcp_value"] / 1000

    if lcp > 4:
        issues.append({
            "severity": "HIGH",
            "issue": f"Poor Largest Contentful Paint ({lcp:.1f}s)",
            "recommendation": "Optimize the LCP element, preload important resources, improve image delivery, and reduce server/rendering delays."
        })

    elif lcp > 2.5:
        issues.append({
            "severity": "MEDIUM",
            "issue": f"LCP needs improvement ({lcp:.1f}s)",
            "recommendation": "Optimize the largest visible element and improve critical resource loading."
        })

    # CLS
    cls = pagespeed["cls_value"]

    if cls > 0.25:
        issues.append({
            "severity": "HIGH",
            "issue": f"Poor Cumulative Layout Shift ({cls:.3f})",
            "recommendation": "Reserve space for images, ads, embeds, and dynamically injected content."
        })

    elif cls > 0.1:
        issues.append({
            "severity": "MEDIUM",
            "issue": f"CLS needs improvement ({cls:.3f})",
            "recommendation": "Define dimensions for visual elements and prevent unexpected layout shifts."
        })

    # Speed Index
    speed_index = pagespeed["speed_index_value"] / 1000

    if speed_index > 5.8:
        issues.append({
            "severity": "HIGH",
            "issue": f"Poor Speed Index ({speed_index:.1f}s)",
            "recommendation": "Optimize critical rendering, reduce render-blocking resources, and improve image and asset delivery."
        })

    elif speed_index > 3.4:
        issues.append({
            "severity": "MEDIUM",
            "issue": f"Speed Index needs improvement ({speed_index:.1f}s)",
            "recommendation": "Improve above-the-fold rendering and optimize critical resources."
        })

    return issues