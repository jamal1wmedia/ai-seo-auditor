import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None


def fallback_analysis(issues):

    if not issues:
        return "No SEO issues were detected."

    output = []

    for issue in issues:
        output.append(
            f"""
[{issue['severity']}] {issue['issue']}

Recommendation:
{issue['recommendation']}
"""
        )

    return "\n".join(output)


def analyze_with_ai(issues):

    if not issues:
        return "No SEO issues were detected."

    if not client:
        print("\n[AI MODE] Local fallback")
        return fallback_analysis(issues)

    prompt = f"""
You are an expert technical SEO consultant.

Analyze the following SEO issues found on a website:

{issues}

For each issue:

1. Explain why it matters.
2. Explain the possible SEO or business impact.
3. Give a practical fix.
4. Prioritize HIGH, then MEDIUM, then LOW.
5. Keep the explanation simple and actionable.
6. Do not invent issues that are not present.

Format the answer with clear headings and bullet points.
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

        return fallback_analysis(issues)