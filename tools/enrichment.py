import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def enrich_lead(raw_search_data: dict, target_industry: str = "digital marketing agency") -> dict:
    """
    Use OpenAI to analyze raw search results and extract structured lead intelligence.
    """

    search_text = json.dumps(raw_search_data, indent=2)

    prompt = f"""You are a B2B sales intelligence analyst. Analyze this search data about a company and extract structured lead intelligence.

Search Data:
{search_text}

Target Industry: {target_industry}

Extract and return ONLY a JSON object with this exact structure:
{{
    "company_name": "company name",
    "website": "website URL",
    "decision_maker": {{
        "name": "name or Unknown",
        "role": "role or Founder/CEO",
        "linkedin": ""
    }},
    "industry": "industry type",
    "employee_count": "estimated size",
    "pain_signals": ["pain signal 1", "pain signal 2"],
    "lead_score": 7,
    "score_reason": "why this score",
    "best_outreach_angle": "what angle to use in outreach"
}}

Score 1-10 based on: company size fit, pain signals found, industry match.
Return ONLY the JSON, no explanation."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )

        content = response.choices[0].message.content.strip()

        # Strip markdown code blocks if present
        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        enriched = json.loads(content)
        return enriched

    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse OpenAI response",
            "raw_response": content,
            "details": str(e)
        }
    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    sample_data = {
        "query": "Acme Marketing Agency",
        "results": [
            {
                "title": "Acme Marketing Agency - Digital Growth",
                "link": "https://acmemarketing.com",
                "snippet": "We help B2B companies generate leads through content marketing and SEO. Founded 2018."
            }
        ],
        "knowledge_graph": {
            "title": "Acme Marketing Agency",
            "type": "Marketing Agency",
            "description": "Full service digital marketing agency",
            "website": "acmemarketing.com"
        }
    }

    result = enrich_lead(sample_data)
    print(json.dumps(result, indent=2))
