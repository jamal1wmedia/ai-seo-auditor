import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def fallback_analysis(issues, pagespeed):

    output = []

    if issues:
        output.append("===== SEO ISSUES =====")

        for issue in issues:
            output.append(
                f"""
[{issue['severity']}] {issue['issue']}

Recommendation:
{issue['recommendation']}
"""
            )
    else:
        output.append("No technical SEO issues were detected.")

    output.append("\n===== PAGESPEED SUMMARY =====")

    output.append(
        f"""
Performance Score: {pagespeed['performance_score']}
FCP: {pagespeed['fcp']}
LCP: {pagespeed['lcp']}
CLS: {pagespeed['cls']}
Speed Index: {pagespeed['speed_index']}
"""
    )

    return "\n".join(output)


def analyze_with_ai(issues, pagespeed):

    if not client:
        print("\n[AI MODE] Local fallback")
        return fallback_analysis(issues, pagespeed)

    prompt = f"""
You are an expert Technical SEO and Web Performance consultant.

Analyze the following website audit data.

TECHNICAL SEO ISSUES:
{issues}

PAGESPEED DATA:
{pagespeed}

Create a practical website audit report.

For each important issue:

1. Explain what the issue means.
2. Explain why it matters for SEO, UX, or conversions.
3. Explain the likely impact.
4. Give a practical technical fix.
5. Prioritize issues as HIGH, MEDIUM, or LOW.

For PageSpeed:

- Evaluate Performance Score.
- Evaluate FCP.
- Evaluate LCP.
- Evaluate CLS.
- Evaluate Speed Index.
- Identify the most important performance problem.

Then provide:

## Executive Summary

## Priority Issues

## Recommended Actions

Keep the explanation simple, technical, and actionable.

Do not invent issues that are not present in the provided data.
"""

    try:

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        print("\n[AI MODE] Gemini")

        return interaction.output_text

    except Exception as e:

        print(f"\nGemini error: {e}")
        print("[AI MODE] Switching to local fallback...")

        return fallback_analysis(issues, pagespeed)