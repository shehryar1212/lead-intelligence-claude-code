# Web Search Skill

## Purpose
Search the web for information about a company or person to gather lead intelligence.

## When to use
Use this skill when you need to find information about a company, its founders, tech stack, recent news, or pain points.

## How to execute
1. Call the tools/search.py script with the query parameter
2. Parse the results and extract relevant company information
3. Return structured data with: company_name, website, description, employee_count, industry, recent_news, tech_stack, pain_signals

## Input
- query: string (company name, domain, or person name)

## Output
```json
{
  "company_name": "",
  "website": "",
  "description": "",
  "industry": "",
  "employee_count": "",
  "recent_news": [],
  "tech_stack": [],
  "pain_signals": []
}
```

## Error handling
If no results found, return empty fields. Never hallucinate company data.
