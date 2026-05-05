# Lead Intelligence Agent

A Claude Code-native agentic pipeline that researches companies, scores leads, drafts personalized outreach, and saves qualified leads to Airtable — with a human approval gate before any data is committed.

## Architecture
User Input (company name)
↓
[Skill: web_search] → Serper API → Raw search results
↓
[Skill: enrich_lead] → OpenAI GPT-4o-mini → Structured lead profile + score
↓
[Skill: draft_outreach] → OpenAI GPT-4o-mini → Personalized cold email
↓
[HUMAN HANDOFF GATE] → Approve / Reject / Edit
↓
[Skill: save_to_airtable] → Airtable API → Lead saved with full profile

## Claude Code Skills

| Skill | Purpose |
|-------|---------|
| `web_search` | Search the web for company intelligence using Serper API |
| `enrich_lead` | Analyze raw search data and extract structured lead profile with AI scoring |
| `draft_outreach` | Generate personalized cold email based on pain signals and company context |
| `save_to_airtable` | Persist qualified leads to Airtable with full metadata |

## Human Handoff Gate

Before any lead is saved, the agent pauses and presents the enriched profile and outreach draft for human review. The operator can:

- **Approve** — save to Airtable as-is
- **Reject** — discard the lead
- **Edit** — modify subject or body before saving

This pattern ensures no outreach is sent without human oversight.

## Tech Stack

- **Claude Code** — skills architecture and agent orchestration
- **Python 3.11** — core runtime
- **Serper API** — Google search results
- **OpenAI GPT-4o-mini** — lead enrichment and outreach generation
- **Airtable** — lead database and CRM
- **python-dotenv** — environment management

## Project Structure
lead-intelligence-agent/
├── .claude/
│   └── skills/
│       ├── web_search.md          # Search skill definition
│       ├── enrich_lead.md         # Enrichment skill definition
│       ├── draft_outreach.md      # Outreach skill definition
│       └── save_to_airtable.md    # Storage skill definition
├── tools/
│   ├── search.py                  # Serper API integration
│   ├── enrichment.py              # OpenAI enrichment logic
│   ├── outreach.py                # OpenAI outreach generation
│   └── airtable_sync.py           # Airtable API integration
├── main.py                        # Pipeline orchestrator with human gate
├── .env                           # API keys (not committed)
├── .gitignore
└── README.md

## Setup

1. Clone the repo
```bash
git clone https://github.com/shehryar1212/lead-intelligence-agent.git
cd lead-intelligence-agent
```

2. Install dependencies
```bash
pip install requests python-dotenv openai pyairtable
```

3. Create `.env` file
SERPER_API_KEY=your_serper_key
OPENAI_API_KEY=your_openai_key
AIRTABLE_API_KEY=your_airtable_token
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_NAME=Agent Leads

4. Run the agent
```bash
python main.py "Company Name Here"
```

## Example Output
============================================================
LEAD INTELLIGENCE AGENT
Researching: Acme Marketing Agency
Step 1/4 - Searching the web...
Found 5 results
Step 2/4 - Enriching lead data with AI...
Company: Acme Digital Marketing
Industry: digital marketing agency
Decision Maker: Unknown - Founder/CEO
Lead Score: 8/10
Score Reason: Strong industry match with clear pain signals
Pain Signals: manual client reporting, no automation in place
Best Angle: Automate client reporting workflow
Step 3/4 - Drafting personalized outreach...
Subject: Acme's client reporting workflow
Email Body:
Hi there, I noticed Acme is still handling client reports manually...
============================================================
HUMAN APPROVAL REQUIRED
Lead: Acme Digital Marketing | Score: 8/10
Options:
[y] Approve and save to Airtable
[n] Reject this lead
[e] Edit outreach before saving
Your decision: y
Step 4/4 - Saving to Airtable...
Saved successfully!
Record ID: rechZIJVHFMTgyez9
PIPELINE COMPLETE

## Airtable Schema

| Field | Type | Description |
|-------|------|-------------|
| Company Name | Text | Target company |
| Website | URL | Company website |
| Decision Maker Name | Text | Key contact |
| Decision Maker Role | Text | Their title |
| Industry | Text | Industry category |
| Lead Score | Number | AI quality score 1-10 |
| Pain Signals | Long text | Identified pain points |
| Outreach Subject | Text | Email subject line |
| Outreach Body | Long text | Full email draft |
| Status | Select | Pending Approval / Approved / Rejected |
| Date Added | Date | Pipeline run date |

## Extending the Agent

To add a new skill:
1. Create a new `.md` file in `.claude/skills/` following the existing skill format
2. Create the corresponding Python tool in `tools/`
3. Import and call it in `main.py`
