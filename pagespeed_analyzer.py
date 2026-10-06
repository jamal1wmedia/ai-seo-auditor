import os

import requests
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("PAGESPEED_API_KEY")


def analyze_pagespeed(url):

    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    params = {
        "url": url,
        "key": api_key,
        "strategy": "mobile"
    }

    response = requests.get(
        endpoint,
        params=params,
        timeout=60
    )

    if response.status_code != 200:
        print("\n===== PAGESPEED API ERROR =====")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        raise Exception("PageSpeed API request failed")

    data = response.json()

    lighthouse = data["lighthouseResult"]
    categories = lighthouse["categories"]

    performance_score = (
        categories["performance"]["score"] * 100
        if categories["performance"]["score"] is not None
        else None
    )

    audits = lighthouse["audits"]

    return {
        "performance_score": performance_score,
        "fcp": audits["first-contentful-paint"]["displayValue"],
        "lcp": audits["largest-contentful-paint"]["displayValue"],
        "cls": audits["cumulative-layout-shift"]["displayValue"],
        "speed_index": audits["speed-index"]["displayValue"],
    }