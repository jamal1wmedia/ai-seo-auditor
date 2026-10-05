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

    # Canonical
    canonical_tag = soup.find(
        "link",
        attrs={"rel": "canonical"}
    )

    canonical_url = (
        canonical_tag.get("href", "").strip()
        if canonical_tag
        else None
    )

    # Open Graph
    og_title_tag = soup.find(
        "meta",
        attrs={"property": "og:title"}
    )

    og_description_tag = soup.find(
        "meta",
        attrs={"property": "og:description"}
    )

    og_image_tag = soup.find(
        "meta",
        attrs={"property": "og:image"}
    )

    og_title = (
        og_title_tag.get("content", "").strip()
        if og_title_tag
        else None
    )

    og_description = (
        og_description_tag.get("content", "").strip()
        if og_description_tag
        else None
    )

    og_image = (
        og_image_tag.get("content", "").strip()
        if og_image_tag
        else None
    )

    # Headings
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")

    # Images
    images = soup.find_all("img")
    
    images_missing_alt = []
    images_empty_alt = []

    for img in images:
        alt = img.get("alt")
        src = img.get("src")

        # ALT attribute does not exist
        if alt is None:
            images_missing_alt.append({
                "src": src,
                "alt": None
            })

        # ALT attribute exists but is empty
        elif alt.strip() == "":
            images_empty_alt.append({
                "src": src,
                "alt": ""
            })

    # Links
    links = soup.find_all("a")

    return {
        "title": title,
        "meta_description": meta_description,
        "canonical_url": canonical_url,
        "og_title": og_title,
        "og_description": og_description,
        "og_image": og_image,
        "h1_count": len(h1_tags),
        "h2_count": len(h2_tags),
        "image_count": len(images),
        "images_missing_alt": len(images_missing_alt),
        "images_empty_alt": len(images_empty_alt),
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

    # Title length
    if result["title"]:
        title_length = len(result["title"])

        if title_length < 30:
            issues.append({
                "severity": "LOW",
                "issue": f"Title is short ({title_length} characters)",
                "recommendation": "Consider making the title more descriptive and relevant to the page."
            })

        elif title_length > 60:
            issues.append({
                "severity": "MEDIUM",
                "issue": f"Title is long ({title_length} characters)",
                "recommendation": "Consider shortening the title so the main topic is clear and concise."
            })

    # Meta description
    if not result["meta_description"]:
        issues.append({
            "severity": "HIGH",
            "issue": "Missing meta description",
            "recommendation": "Add a unique meta description."
        })

    # Meta description length
    if result["meta_description"]:
        meta_length = len(result["meta_description"])

        if meta_length < 70:
            issues.append({
                "severity": "LOW",
                "issue": f"Meta description is short ({meta_length} characters)",
                "recommendation": "Consider adding more useful information that clearly describes the page."
            })

        elif meta_length > 160:
            issues.append({
                "severity": "MEDIUM",
                "issue": f"Meta description is long ({meta_length} characters)",
                "recommendation": "Consider shortening the meta description so the main message is concise."
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

    # Canonical
    if not result["canonical_url"]:
        issues.append({
            "severity": "MEDIUM",
            "issue": "Missing canonical URL",
            "recommendation": "Add a canonical URL to indicate the preferred version of the page."
        })

    # Open Graph
    if not result["og_title"]:
        issues.append({
            "severity": "LOW",
            "issue": "Missing Open Graph title",
            "recommendation": "Add an og:title tag for better social sharing."
        })

    if not result["og_description"]:
        issues.append({
            "severity": "LOW",
            "issue": "Missing Open Graph description",
            "recommendation": "Add an og:description tag for better social sharing previews."
        })

    if not result["og_image"]:
        issues.append({
            "severity": "LOW",
            "issue": "Missing Open Graph image",
            "recommendation": "Add an og:image tag with a suitable social sharing image."
        })

    return issues