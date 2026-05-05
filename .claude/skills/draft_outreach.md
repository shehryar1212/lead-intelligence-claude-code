# Draft Outreach Skill

## Purpose
Generate a personalized cold outreach email based on enriched lead data.

## When to use
Use this skill after enrich_lead returns a scored lead profile. Only draft outreach for leads with score 6 or above.

## How to execute
1. Receive enriched lead profile from enrich_lead skill
2. Identify the strongest pain signal to lead with
3. Write a concise cold email: 3-4 sentences max, no fluff
4. Subject line must be specific to the company, not generic
5. Email must reference one specific thing about the company
6. End with a single low-friction CTA (15 min call, quick question, etc)

## Tone
- Direct and confident, not salesy
- No buzzwords: no "synergy", "leverage", "cutting-edge", "innovative"
- No exclamation marks
- Sound like a human, not a template

## Input
- enriched_lead: dict (output from enrich_lead skill)
- sender_name: string (your name)
- sender_service: string (what you offer)

## Output
```json
{
  "subject": "",
  "body": "",
  "personalization_used": "",
  "pain_signal_referenced": ""
}
```

## Error handling
If lead score is below 6, return: {"skip": true, "reason": "Lead score too low for outreach"}
