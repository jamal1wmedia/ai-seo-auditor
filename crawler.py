import requests


def fetch_page(url):
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "AI-SEO-Auditor/0.1"
        }
    )

    response.raise_for_status()

    return response.text
