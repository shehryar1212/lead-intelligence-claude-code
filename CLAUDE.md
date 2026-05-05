# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a lead intelligence agent that researches, scores, and surfaces insights on potential business leads or prospects. It follows the **WAT framework** (Workflows, Agents, Tools) to separate AI reasoning from deterministic execution.

## Architecture

**Layer 1: Agents (The Instructions)**
- Markdown SOPs stored in `agents/`
- Each agent file defines an objective, required inputs, which tools to call, expected outputs, and edge case handling

**Layer 2: Claude (The Decision-Maker)**
- Read the relevant agent file, run tools in sequence, handle failures, and ask for clarification when inputs are ambiguous
- Do not attempt tasks directly that a tool can handle — delegate execution to `tools/`

**Layer 3: Tools (The Execution)**
- Python scripts in `tools/` for deterministic work: API calls, data fetching, scoring logic, file I/O
- Credentials and API keys go in `.env` only

## How to Operate

1. **Check `tools/` before building anything new** — only create a new script if nothing covers the task
2. **When a tool fails**: read the full error, fix the script, retest, then update the relevant agent file with what you learned
3. **Do not create or overwrite agent files without asking** — they are the source of truth for how workflows run
4. **Temporary files** go in `.tmp/` (create it if needed); treat everything there as disposable

## Directory Layout

```
agents/     # Markdown SOPs — what to do and in what order
tools/      # Python scripts — deterministic execution
.tmp/       # Intermediate files (scraped data, exports). Regenerated as needed.
.env        # API keys and secrets (never stored elsewhere)
```

## Environment Setup

Create a `.env` file at the project root before running any tools. Add keys as tools require them (e.g., search APIs, enrichment services, CRM credentials).

Install dependencies into a local virtualenv:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run a tool directly to test it:
```
python tools/<tool_name>.py
```
