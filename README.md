# AI Lead Generation & Hyper-Personalized Outreach Pipeline

<div align="center">

[![n8n](https://img.shields.io/badge/Orchestrator-n8n-EA4B71.svg?style=flat-square&logo=n8n&logoColor=white)](https://n8n.io/)
[![OpenAI GPT-4o-mini](https://img.shields.io/badge/LLM-GPT--4o--mini-412991.svg?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![Docker](https://img.shields.io/badge/Container-Docker_Compose-2496ED.svg?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Telegram](https://img.shields.io/badge/Notification-Telegram-24A1DE.svg?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org/)
[![Google Sheets](https://img.shields.io/badge/CRM_Sync-Google_Sheets-34A853.svg?style=flat-square&logo=googlesheets&logoColor=white)](https://workspace.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-2ea44f.svg?style=flat-square)](./LICENSE)
[![Workflow Status](https://img.shields.io/badge/Workflow-13_Nodes_Validated-success.svg?style=flat-square)](#workflow-architecture)

**Autonomous B2B lead generation workflow in n8n. Scrapes company websites, identifies operational friction points via regex heuristics, synthesizes hyper-tailored outreach pitches with GPT-4o-mini, and delivers real-time Telegram previews before CRM logging.**

[Workflow Architecture](#workflow-architecture) • [Quick Start](#quick-start) • [Sample Generated Pitches](#sample-generated-pitches) • [Unit Economics](#unit-economics--cost-breakdown) • [Design Decisions](#engineering-design-decisions)

</div>

---

## Overview

Cold outreach typically suffers from generic mass-mailing templates that achieve low response rates. This repository implements an automated n8n pipeline that researches each prospect's website individually, identifies concrete operational bottlenecks (e.g. phone-only booking, slow response times), and drafts high-context value propositions.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Target Lead: BrightSmile Dental Care (Austin, TX)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  🔍 Scraped Gap:   Requires phone calls during office hours (Mon-Fri 9-5).   │
│  ✍️ Tailored Pitch: "Hi Marcus, I noticed BrightSmile Dental Care currently │
│                    requires patients to call during office hours to book    │
│                    visits. Adding a 24/7 AI booking assistant would capture │
│                    high-intent after-hours patients automatically without   │
│                    adding front-desk overhead."                             │
│  📱 Action:        Instant Telegram preview + Google Sheets CRM sync.       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Features

- 🔄 **Loop-Safe Error Recovery:** Both successful scraping (HTTP 200) and failed connections (HTTP 404/500) route back to the loop counter, preventing batch stalls.
- ⏱️ **Built-in Rate Limiting:** Enforces a 2-second polite delay between outbound requests to prevent IP throttling and API rate limits.
- 🔍 **Lightweight Heuristic Extraction:** Fast regex-based parser extracts operational friction points without requiring heavy headless browsers.
- 🎯 **Hyper-Personalized Generation:** Constrained prompt template generates concise 2–3 sentence pitches focused on concrete pain points.
- 🛡️ **Zero Hardcoded Secrets:** Configured for native n8n Credential Manager and `.env.example` templates.
- 🧪 **Offline Pipeline Simulator:** Includes [`simulate_pipeline.py`](./simulate_pipeline.py) for testing extraction logic and cost calculations locally.

---

## Workflow Architecture

<div align="center">
  <img src="assets/architecture.svg?v=2026" alt="n8n LeadGen Pipeline Architecture" width="100%">
</div>

---

## Repository Structure

```text
n8n-ai-leadgen-outreach/
├── n8n-workflow.json        # Complete 13-node n8n workflow export
├── simulate_pipeline.py     # Standalone offline simulation & test suite
├── docker-compose.yml       # Production-ready local n8n container stack
├── demo-data/
│   └── leads-sample.csv     # Synthetic lead fixtures (-example.com domains)
├── .env.example             # Environment template (N8N encryption key, ports)
├── .gitignore               # Standard git ignore rules
└── LICENSE                  # MIT License
```

---

## Verification Status

| Component | Status | Verification Method |
| :--- | :---: | :--- |
| **Workflow Schema** | `Verified` | Validated JSON structure with 13 connected nodes and explicit loop closing |
| **Python Offline Simulation** | `Verified` | [`simulate_pipeline.py`](./simulate_pipeline.py) validates end-to-end logic across test fixtures |
| **Live n8n Execution** | `Reference` | Importable into any n8n v1.0+ instance via [`n8n-workflow.json`](./n8n-workflow.json) |
| **Live OpenAI API Call** | `Reference` | Configured for Header Auth / OpenAI integration in n8n Credentials |

---

## Quick Start

### 1. Offline Simulation (No Credentials Required)

Test the end-to-end pipeline logic, text extraction, pitch assembly, and cost calculation locally:

```bash
# Clone the repository
git clone https://github.com/therealfullmetal55555/n8n-ai-leadgen-outreach.git
cd n8n-ai-leadgen-outreach

# Run offline simulator
python3 simulate_pipeline.py
```

<details>
<summary><b>🔍 Click to view Sample Simulator Output</b></summary>

```text
================================================================================
N8N LEADGEN & OUTREACH PIPELINE SIMULATION (OFFLINE DRY-RUN)
================================================================================

[Lead 1/3] Processing: BrightSmile Dental Care (Marcus Vance)
  • Target URL: https://brightsmile-demo.org
  • Scrape Status: HTTP 200 OK
  • Detected Gap: Office-hours phone-only booking (Mon-Fri 9am-5pm)
  • Generated Pitch:
    "Hi Marcus, I noticed BrightSmile Dental Care currently requires patients to call during office hours to book visits. Adding a 24/7 AI booking assistant would capture high-intent after-hours patients automatically without adding front-desk overhead."
  • Telemetry: Prompt: 218 tok | Comp: 44 tok | Cost: $0.000059 USD
  • Telegram Dispatch: SIMULATED_SENT
  • CRM Sync: SIMULATED_SAVED

[Lead 2/3] Processing: Apex Pediatric Dentistry (Dr. Sarah Jenkins)
  • Target URL: https://apexpediatric-example.com
  • Scrape Status: HTTP 200 OK
  • Detected Gap: Slow contact form (2-3 business day response window)
  • Generated Pitch:
    "Hi Sarah, I saw that inquiries on Apex Pediatric Dentistry's site take 2-3 business days for a reply. An automated intake bot could instantly qualify insurance and schedule appointments on the spot, preventing patient churn."
  • Telemetry: Prompt: 212 tok | Comp: 39 tok | Cost: $0.000055 USD
  • Telegram Dispatch: SIMULATED_SENT
  • CRM Sync: SIMULATED_SAVED
================================================================================
```
</details>

### 2. Live n8n Deployment

1. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

2. Start the n8n container:
   ```bash
   docker compose up -d
   ```

3. Open `http://localhost:5678` in your browser.
4. Import [`n8n-workflow.json`](./n8n-workflow.json) into your workspace.
5. Configure credentials in n8n Credentials Manager:
   - **OpenAI API Key** (Header Auth)
   - **Telegram Bot Token** (Telegram account)
6. Click **Test workflow** or connect to a live Google Sheet trigger.

---

## Sample Generated Pitches

| Prospect & Niche | Detected Friction Point | Tailored Outreach Pitch |
| :--- | :--- | :--- |
| **BrightSmile Dental**<br>`Austin, TX` | Phone-only booking during standard 9–5 office hours. | *"Hi Marcus, I noticed BrightSmile Dental Care currently requires patients to call during office hours to book visits. Adding a 24/7 AI booking assistant would capture high-intent after-hours patients automatically without adding front-desk overhead."* |
| **Apex Pediatric Dentistry**<br>`Seattle, WA` | Contact form specifies 2–3 business day response window. | *"Hi Sarah, I saw that inquiries on Apex Pediatric Dentistry's site take 2-3 business days for a reply. An automated intake bot could instantly qualify insurance and schedule appointments on the spot, preventing patient churn."* |
| **Metro Spine & Wellness**<br>`Denver, CO` | Static intake PDF forms requiring manual printing and scanning. | *"Hi David, I noticed new patients at Metro Spine need to print and fill out PDF forms manually. An interactive digital onboarding flow could collect medical history directly into your EHR, saving 15 minutes per check-in."* |

---

## Unit Economics & Cost Breakdown

*Calculated with `gpt-4o-mini` pricing ($0.150 / 1M prompt tokens, $0.600 / 1M output tokens):*

$$\text{Cost per Lead} = \left(\frac{215}{10^6} \times \$0.150\right) + \left(\frac{42}{10^6} \times \$0.600\right) \approx \mathbf{\$0.000057 \text{ USD}}$$

| Scale Volume | Prompt Tokens | Completion Tokens | Total LLM Cost | Cost per 1,000 Leads |
| :---: | :---: | :---: | :---: | :---: |
| **100 Leads** | ~21.5k | ~4.2k | **$0.006 USD** | ~$0.057 |
| **1,000 Leads** | ~215.0k | ~42.0k | **$0.057 USD** | ~$0.057 |
| **10,000 Leads** | ~2.15M | ~420.0k | **$0.575 USD** | ~$0.057 |

---

## Engineering Design Decisions

| Architectural Decision | Implementation | Why it matters |
| :--- | :--- | :--- |
| **Dual-Branch Loop Closure** | Both 200 OK and Error paths route to Sheet node | Prevents workflow deadlocks when encountering 404s, DNS timeouts, or Cloudflare blocks. |
| **2-Second Politeness Delay** | n8n Wait Node | Avoids hammering target web servers and prevents HTTP 429 rate limit exceptions. |
| **Encrypted Credential Storage** | n8n Credential Manager | Ensures API keys and bot tokens are never stored in plain text inside JSON workflow files. |
| **Regex Heuristic Classifier** | Lightweight JavaScript Node | Extracts key operational patterns rapidly without requiring resource-heavy browser rendering. |
| **Synthetic Test Data** | RFC 2606 `-example.com` domains | Safe for public demonstration and continuous integration testing. |

---

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for full details.
