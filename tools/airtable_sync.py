import os
import json
from datetime import datetime
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME", "Leads")


def save_lead(enriched_lead: dict, outreach_draft: dict, status: str = "Pending Approval") -> dict:
    """
    Save complete lead profile and outreach draft to Airtable.
    """

    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        raise ValueError("Airtable credentials missing from environment variables")

    try:
        api = Api(AIRTABLE_API_KEY)
        table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

        decision_maker = enriched_lead.get("decision_maker", {})
        pain_signals = enriched_lead.get("pain_signals", [])

        fields = {
            "Company Name": enriched_lead.get("company_name", ""),
            "Website": enriched_lead.get("website", ""),
            "Decision Maker Name": decision_maker.get("name", ""),
            "Decision Maker Role": decision_maker.get("role", ""),
            "Industry": enriched_lead.get("industry", ""),
            "Lead Score": enriched_lead.get("lead_score", 0),
            "Pain Signals": ", ".join(pain_signals) if pain_signals else "",
            "Outreach Subject": outreach_draft.get("subject", ""),
            "Outreach Body": outreach_draft.get("body", ""),
            "Status": status,
            "Date Added": datetime.now().strftime("%Y-%m-%d")
        }

        record = table.create(fields)

        return {
            "success": True,
            "record_id": record["id"],
            "airtable_url": f"https://airtable.com/{AIRTABLE_BASE_ID}"
        }

    except Exception as e:
        # Fallback: save to local file if Airtable fails
        failed_lead = {
            "enriched_lead": enriched_lead,
            "outreach_draft": outreach_draft,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

        with open("failed_leads.json", "a") as f:
            f.write(json.dumps(failed_lead) + "\n")

        return {
            "success": False,
            "error": str(e),
            "fallback": "Saved to failed_leads.json"
        }


if __name__ == "__main__":
    sample_lead = {
        "company_name": "Acme Marketing Agency",
        "website": "acmemarketing.com",
        "decision_maker": {
            "name": "John Smith",
            "role": "Founder"
        },
        "industry": "Digital Marketing",
        "employee_count": "10-50",
        "pain_signals": ["manual reporting", "no automation"],
        "lead_score": 8,
        "score_reason": "Strong fit",
        "best_outreach_angle": "Automate reporting"
    }

    sample_outreach = {
        "subject": "Acme's reporting workflow",
        "body": "Hi John, noticed Acme is still doing client reports manually...",
        "personalization_used": "Manual reporting pain signal",
        "pain_signal_referenced": "manual reporting"
    }

    result = save_lead(sample_lead, sample_outreach)
    print(json.dumps(result, indent=2))
