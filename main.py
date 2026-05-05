import json
from tools.search import search_company
from tools.enrichment import enrich_lead
from tools.outreach import draft_outreach
from tools.airtable_sync import save_lead


def run_lead_agent(company_query: str, sender_name: str = "Shehryar", sender_service: str = "AI automation workflows"):
    """
    Full lead intelligence pipeline with human handoff gate.
    """

    print(f"\n{'='*60}")
    print(f"LEAD INTELLIGENCE AGENT")
    print(f"{'='*60}")
    print(f"Researching: {company_query}\n")

    # Step 1 - Search
    print("Step 1/4 - Searching the web...")
    search_results = search_company(company_query)

    if search_results.get("error"):
        print(f"Search failed: {search_results['error']}")
        return

    print(f"Found {len(search_results.get('results', []))} results\n")

    # Step 2 - Enrich
    print("Step 2/4 - Enriching lead data with AI...")
    enriched = enrich_lead(search_results)

    if enriched.get("error"):
        print(f"Enrichment failed: {enriched['error']}")
        return

    print(f"\nCompany: {enriched.get('company_name')}")
    print(f"Industry: {enriched.get('industry')}")
    print(f"Decision Maker: {enriched.get('decision_maker', {}).get('name')} - {enriched.get('decision_maker', {}).get('role')}")
    print(f"Lead Score: {enriched.get('lead_score')}/10")
    print(f"Score Reason: {enriched.get('score_reason')}")
    print(f"Pain Signals: {', '.join(enriched.get('pain_signals', []))}")
    print(f"Best Angle: {enriched.get('best_outreach_angle')}\n")

    # Step 3 - Draft outreach
    print("Step 3/4 - Drafting personalized outreach...")
    outreach = draft_outreach(enriched, sender_name, sender_service)

    if outreach.get("skip"):
        print(f"Skipping outreach: {outreach.get('reason')}")
        return

    if outreach.get("error"):
        print(f"Outreach drafting failed: {outreach['error']}")
        return

    print(f"\nSubject: {outreach.get('subject')}")
    print(f"\nEmail Body:\n{outreach.get('body')}")
    print(f"\nPersonalization used: {outreach.get('personalization_used')}")
    print(f"Pain signal referenced: {outreach.get('pain_signal_referenced')}\n")

    # Step 4 - Human handoff gate
    print("="*60)
    print("HUMAN APPROVAL REQUIRED")
    print("="*60)
    print(f"Lead: {enriched.get('company_name')} | Score: {enriched.get('lead_score')}/10")
    print("\nOptions:")
    print("  [y] Approve and save to Airtable")
    print("  [n] Reject this lead")
    print("  [e] Edit outreach before saving")

    choice = input("\nYour decision: ").strip().lower()

    if choice == "n":
        print("Lead rejected. Not saved.")
        return

    if choice == "e":
        print("\nCurrent subject:", outreach.get("subject"))
        new_subject = input("New subject (press Enter to keep current): ").strip()
        if new_subject:
            outreach["subject"] = new_subject

        print("\nCurrent body:")
        print(outreach.get("body"))
        print("\nNew body (press Enter to keep current):")
        new_body = input().strip()
        if new_body:
            outreach["body"] = new_body

    # Step 4 - Save to Airtable
    print("\nStep 4/4 - Saving to Airtable...")
    result = save_lead(enriched, outreach)

    if result.get("success"):
        print(f"\nSaved successfully!")
        print(f"Record ID: {result.get('record_id')}")
        print(f"View in Airtable: {result.get('airtable_url')}")
    else:
        print(f"\nAirtable save failed: {result.get('error')}")
        print("Lead saved to failed_leads.json as backup")

    print(f"\n{'='*60}")
    print("PIPELINE COMPLETE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter company name to research: ").strip()

    run_lead_agent(query)
