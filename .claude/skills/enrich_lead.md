# Enrich Lead Skill

## Purpose
Take raw search results and extract structured lead intelligence for sales outreach.

## When to use
Use this skill after web_search returns results. Takes raw data and enriches it into a clean lead profile.

## How to execute
1. Receive raw search data from web_search skill
2. Identify the key decision maker (founder, CEO, marketing director)
3. Extract pain signals — hiring posts, negative reviews, recent funding, product launches
4. Score lead quality 1-10 based on: company size, pain signals, industry fit
5. Return enriched lead profile

## Input
- raw_search_data: dict (output from web_search skill)
- target_industry: string (e.g. "digital marketing agency")

## Output
```json
{
  "company_name": "",
  "website": "",
  "decision_maker": {
    "name": "",
    "role": "",
    "linkedin": ""
  },
  "industry": "",
  "employee_count": "",
  "pain_signals": [],
  "lead_score": 0,
  "score_reason": "",
  "best_outreach_angle": ""
}
```

## Error handling
If decision maker cannot be identified, set name to "Unknown" and role to "Founder/CEO". Never guess LinkedIn URLs.
