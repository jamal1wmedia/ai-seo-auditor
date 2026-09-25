from bs4 import BeautifulSoup


def analyze_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else None

    # Meta description
    meta_tag = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    meta_description = (
        meta_tag.get("content", "").strip()
        if meta_tag
        else None
    )

    # Headings
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")

    # Images
    images = soup.find_all("img")

    missing_alt = [
        img for img in images
        if not img.get("alt")
    ]

    # Links
    links = soup.find_all("a")

    return {
        "title": title,
        "meta_description": meta_description,
        "h1_count": len(h1_tags),
        "h2_count": len(h2_tags),
        "image_count": len(images),
        "images_missing_alt": len(missing_alt),
        "link_count": len(links),
    }


def find_seo_issues(result):

    issues = []

    # Title
    if not result["title"]:
        issues.append({
            "severity": "HIGH",
            "issue": "Missing page title",
            "recommendation": "Add a descriptive <title> tag."
        })

    # Meta description
    if not result["meta_description"]:
        issues.append({
            "severity": "HIGH",
            "issue": "Missing meta description",
            "recommendation": "Add a unique meta description."
        })

    # H1
    if result["h1_count"] == 0:
        issues.append({
            "severity": "HIGH",
            "issue": "Missing H1 heading",
            "recommendation": "Add one clear H1 heading."
        })

    elif result["h1_count"] > 1:
        issues.append({
            "severity": "MEDIUM",
            "issue": "Multiple H1 headings",
            "recommendation": "Review the page structure and keep one primary H1 where appropriate."
        })

    # H2
    if result["h2_count"] == 0:
        issues.append({
            "severity": "LOW",
            "issue": "No H2 headings found",
            "recommendation": "Consider using H2 headings to structure longer content."
        })

    # Images
    if result["images_missing_alt"] > 0:
        issues.append({
            "severity": "MEDIUM",
            "issue": f"{result['images_missing_alt']} images missing ALT text",
            "recommendation": "Add meaningful ALT text to relevant images."
        })

    return issues