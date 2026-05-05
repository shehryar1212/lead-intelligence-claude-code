import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def draft_outreach(enriched_lead: dict, sender_name: str = "Shehryar", sender_service: str = "AI automation workflows") -> dict:
    """
    Generate personalized cold outreach email based on enriched lead data.
    """

    if enriched_lead.get("lead_score", 0) < 6:
        return {
            "skip": True,
            "reason": f"Lead score too low: {enriched_lead.get('lead_score', 0)}/10"
        }

    lead_text = json.dumps(enriched_lead, indent=2)

    prompt = f"""You are an expert cold email copywriter. Write a personalized cold outreach email based on this lead data.

Lead Data:
{lead_text}

Sender: {sender_name}
Service offered: {sender_service}

Rules:
- Maximum 4 sentences in the body
- Subject line must reference something specific about this company
- Lead with their strongest pain signal
- No buzzwords: no synergy, leverage, cutting-edge, innovative, game-changer
- No exclamation marks
- Sound human, not like a template
- End with one low-friction CTA (15 min call or single question)

Return ONLY a JSON object with this exact structure:
{{
    "subject": "email subject line",
    "body": "full email body",
    "personalization_used": "what specific detail you used",
    "pain_signal_referenced": "which pain signal you led with"
}}

Return ONLY the JSON, no explanation."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )

        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.replace("```json", "").replace("```", "").strip()

        outreach = json.loads(content)
        return outreach

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
    sample_lead = {
        "company_name": "Acme Marketing Agency",
        "website": "acmemarketing.com",
        "decision_maker": {
            "name": "John Smith",
            "role": "Founder",
            "linkedin": ""
        },
        "industry": "Digital Marketing",
        "employee_count": "10-50",
        "pain_signals": ["manual client reporting", "no automation in place"],
        "lead_score": 8,
        "score_reason": "Strong pain signals, right size, good industry fit",
        "best_outreach_angle": "Automate their client reporting workflow"
    }

    result = draft_outreach(sample_lead)
    print(json.dumps(result, indent=2))
