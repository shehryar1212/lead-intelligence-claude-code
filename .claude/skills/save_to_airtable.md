# Save to Airtable Skill

## Purpose
Save a complete lead profile and outreach draft to Airtable for tracking and follow-up.

## When to use
Use this skill after draft_outreach returns an approved outreach email. This is the final step in the pipeline.

## How to execute
1. Receive enriched lead + outreach draft
2. Call tools/airtable_sync.py with the combined data
3. Create a new record in the Leads table
4. Return the created record ID and Airtable URL

## Input
- enriched_lead: dict (output from enrich_lead skill)
- outreach_draft: dict (output from draft_outreach skill)
- status: string (default: "Pending Approval")

## Airtable fields to populate
- Company Name
- Website
- Decision Maker Name
- Decision Maker Role
- Industry
- Lead Score
- Pain Signals (comma separated)
- Outreach Subject
- Outreach Body
- Status
- Date Added

## Output
```json
{
  "success": true,
  "record_id": "",
  "airtable_url": ""
}
```

## Error handling
If Airtable API fails, log the error and save the lead data locally to a failed_leads.json file so no data is lost.
