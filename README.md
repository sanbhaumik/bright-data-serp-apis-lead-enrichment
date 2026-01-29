# Custom Lead Enrichment Engine

A production-ready lead enrichment system that tracks buying signals using [Bright Data's SERP API](https://get.brightdata.com/2039fnr15xfy). This engine identifies high-intent leads by monitoring hiring patterns, pain points, technology adoption, and strategic initiatives across the web.

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command-Line Interface](#command-line-interface)
- [Configuration Guide](#configuration-guide)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Production Deployment](#production-deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

---

## Overview

### What It Does

The Custom Lead Enrichment Engine analyzes publicly available search engine data to identify buying signals that indicate when companies are ready to purchase. Unlike traditional enrichment tools that only provide firmographic data, this engine detects:

- **Active Hiring**: Companies expanding teams in relevant areas
- **Pain Points**: Public mentions of challenges your product solves
- **Technology Adoption**: Companies using or migrating to complementary tools
- **Strategic Initiatives**: High-level transformations that create buying opportunities

Each lead receives a **0-100 intent score** and is classified as High, Medium, or Low intent, with personalized conversation starters for outreach.

### Key Benefits

- **Identify high-intent leads before competitors**: Catch companies at the perfect moment
- **Personalize outreach at scale**: Auto-generated conversation starters based on detected signals
- **Reduce wasted sales effort**: Focus on leads showing active buying signals
- **Track competitor customers**: Monitor companies using competing technologies
- **Custom signal definitions**: Tailor to your specific ICP and value proposition

### Use Cases

| Industry | Use Case | Signals to Track |
|----------|----------|------------------|
| **DevOps Tools** | Find companies with infrastructure challenges | API performance issues, Kubernetes adoption, DevOps hiring |
| **HR Tech** | Identify rapidly growing companies | Hiring surges, onboarding challenges, ATS problems |
| **Security** | Target companies post-breach or seeking compliance | Security incidents, SOC 2 mentions, CISO hiring |
| **Data Tools** | Locate companies with data challenges | Data quality issues, Snowflake adoption, data engineer hiring |

---

## Installation

### Prerequisites

- **Python 3.8+** (Check: `python --version`)
- **Bright Data Account** with SERP API access ([Sign up here]([https://brightdata.com](https://get.brightdata.com/2039fnr15xfy))
- **SERP API Credentials**: API key and zone name

### Step-by-Step Setup

#### 1. Clone or Download Repository

```bash
cd custom-enrichment-layer
```

#### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed requests-2.31.0 python-dotenv-1.0.0
```

#### 4. Configure API Credentials

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```bash
SERP_API_KEY=your_bright_data_api_key_here
SERP_ZONE=your_serp_zone_name_here
DEFAULT_COUNTRY=us
DEFAULT_LANGUAGE=en
```

**Where to find your credentials:**
- Log in to [Bright Data Dashboard]([https://brightdata.com/c](https://get.brightdata.com/2039fnr15xfy))
- Navigate to: Proxies & Scraping Infrastructure → SERP API
- Copy your API key and zone name

#### 5. Verify Installation

Test your configuration:
```bash
python config.py
```

Expected output:
```
✓ Configuration validated successfully
✓ SERP API configured for zone: your_zone_name
✓ Default search params: country=us, language=en
✓ Active signals: 4
```

If you see errors, check your `.env` file credentials.

---

## Quick Start

### Minimal Working Example

Create a file `test_basic.py`:

```python
from enrichment_engine import CustomEnrichmentEngine

# Initialize engine
engine = CustomEnrichmentEngine()

# Enrich a single lead
profile = engine.enrich_with_custom_signals(
    domain="acme.com",
    company_name="Acme Corporation"
)

# Display results
print(f"Score: {profile['custom_signals']['total_score']}/100")
print(f"Intent: {profile['custom_signals']['intent_level']}")
print(f"Recommendation: {profile['custom_signals']['recommendation']}")

# Show conversation starters
print("\nConversation Starters:")
for starter in profile['conversation_starters']:
    print(f"  • {starter}")
```

Run it:
```bash
python test_basic.py
```

### Expected Output

```
→ Tracking custom signals: Acme Corporation
  • Checking hiring signals...
    ✓ Signal detected (+30 points)
  • Checking pain point signals...
  • Checking tech stack signals...
    ✓ Signal detected (+25 points)
  • Checking strategic signals...

  ✓ Total signal score: 55/100 (Medium intent)

Score: 55/100
Intent: Medium
Recommendation: ⚡ Medium intent. 2 signal(s) detected. Schedule standard outreach with personalized messaging.

Conversation Starters:
  • Saw you're hiring for roles involving data engineer - are you expanding your team?
  • Noticed you're working with Snowflake - how's that migration going?
  • Interested in learning more about Acme Corporation's data strategy
```

### Customization Hints

**Change signal weights:** Edit `config.py` → `CUSTOM_SIGNALS` → adjust `weight` values

**Add keywords:** Edit `config.py` → add to `keywords` list for each signal

**Change thresholds:** Edit `config.py` → `INTENT_THRESHOLDS` → adjust score cutoffs

---

## Command-Line Interface

The enrichment engine includes a powerful CLI for easy command-line usage, automation, and batch processing.

### CLI Commands

| Command | Description |
|---------|-------------|
| `enrich` | Enrich a single lead |
| `batch` | Batch process leads from CSV |
| `monitor` | Set up automated monitoring |
| `preset` | Manage industry presets |

### Quick CLI Examples

**Enrich a single lead:**
```bash
./run_enrichment.sh enrich --domain stripe.com
```

**Batch process from CSV:**
```bash
./run_enrichment.sh batch --input leads.csv
```

**List available presets:**
```bash
./run_enrichment.sh preset --list
```

**Set up weekly monitoring:**
```bash
./schedule_monitoring.sh setup --leads-file leads.csv
```

---

### 1. Enrich Command

Enrich a single lead with custom buying signals.

**Basic Usage:**
```bash
./run_enrichment.sh enrich --domain DOMAIN [OPTIONS]
```

**Options:**
- `--domain` (required): Company domain (e.g., stripe.com)
- `--company`: Company name (optional, auto-derived if not provided)
- `--output`: Output format - `text` (default), `json`, or `csv`
- `--preset`: Industry preset to use (e.g., devtools, fintech, security)

**Examples:**

```bash
# Basic enrichment with text output
./run_enrichment.sh enrich --domain stripe.com

# With company name and JSON output
./run_enrichment.sh enrich --domain stripe.com --company Stripe --output json

# Using a specific industry preset
./run_enrichment.sh enrich --domain stripe.com --preset fintech

# CSV output for spreadsheet import
./run_enrichment.sh enrich --domain gusto.com --output csv
```

**Output Example (Text):**
```
============================================================
ENRICHMENT RESULTS
============================================================
Company: Stripe
Domain: stripe.com
Date: 2026-01-20T23:45:12.123456

Signal Score: 75/100
Intent Level: High

Detected Signals:
  ✓ Hiring Signals (Weight: 30)
      Evidence: 3 sources
  ✗ Pain Point Signals (Weight: 35)
  ✓ Tech Stack Signals (Weight: 25)
      Evidence: 2 sources
  ✓ Strategic Signals (Weight: 20)
      Evidence: 1 sources

Recommendation:
  🔥 High priority lead! Prioritize immediate outreach.

Conversation Starters:
  1. Saw you're hiring for roles involving data engineer
  2. Noticed you're working with Snowflake
  3. Just saw your post about payment infrastructure
```

---

### 2. Batch Command

Process multiple leads from a CSV file.

**Basic Usage:**
```bash
./run_enrichment.sh batch --input FILE [OPTIONS]
```

**Options:**
- `--input` (required): Input CSV file with `domain` column
- `--output-file`: Output filename (auto-generated if not provided)
- `--format`: Output format - `csv` (default) or `json`
- `--preset`: Industry preset to use

**CSV Format:**

Your input CSV should have these columns:
```csv
domain,company_name
stripe.com,Stripe
gusto.com,Gusto
datadog.com,Datadog
```

**Examples:**

```bash
# Basic batch processing
./run_enrichment.sh batch --input leads.csv

# With specific output file
./run_enrichment.sh batch --input leads.csv --output-file enriched_leads.csv

# JSON output
./run_enrichment.sh batch --input leads.csv --format json

# Using industry preset
./run_enrichment.sh batch --input leads.csv --preset devtools

# Full example with all options
./run_enrichment.sh batch \
  --input my_leads.csv \
  --output-file results_2026.json \
  --format json \
  --preset fintech
```

**Output Example:**
```
✓ Using preset: devtools

Enriching 5 leads...
------------------------------------------------------------
[1/5] stripe.com... 75/100 (High)
[2/5] gusto.com... 85/100 (High)
[3/5] datadog.com... 55/100 (Medium)
[4/5] snowflake.com... 65/100 (High)
[5/5] anthropic.com... 70/100 (High)

------------------------------------------------------------
✓ Enrichment complete: 5 leads
✓ Results saved to: enriched_20260120_234512.csv

============================================================
BATCH SUMMARY
============================================================
Total Leads: 5
  High Intent: 4
  Medium Intent: 1
  Low Intent: 0

Average Score: 70.0/100
```

---

### 3. Preset Command

Manage and use industry-specific signal presets.

**Basic Usage:**
```bash
./run_enrichment.sh preset [OPTIONS]
```

**Options:**
- `--list`: List all available presets
- `--show NAME`: Show detailed info about a preset
- `--use NAME`: Apply a preset (makes it default)

**Available Presets:**
- `devtools` - Developer Tools & API Platforms
- `hrtech` - HR Technology & Recruiting
- `security` - Cybersecurity & Compliance
- `data` - Data & Analytics Tools
- `fintech` - Financial Technology
- `saas` - SaaS Platforms
- `martech` - Marketing Technology
- `infrastructure` - Infrastructure & Cloud

**Examples:**

```bash
# List all presets
./run_enrichment.sh preset --list

# Show details of security preset
./run_enrichment.sh preset --show security

# Apply HR Tech preset
./run_enrichment.sh preset --use hrtech
```

**List Output Example:**
```
============================================================
AVAILABLE INDUSTRY PRESETS
============================================================

devtools
  Industry: Developer Tools & API Platforms
  Signals: 5
  Example: stripe.com, twilio.com

hrtech
  Industry: HR Technology & Recruiting
  Signals: 5
  Example: gusto.com, rippling.com

security
  Industry: Cybersecurity & Compliance
  Signals: 5
  Example: cloudflare.com, okta.com

...

------------------------------------------------------------
Usage: python cli.py preset --use <preset_name>
```

---

### 4. Monitor Command

Set up automated monitoring for leads with scheduled checks.

**Setup Monitoring:**
```bash
./schedule_monitoring.sh setup --leads-file FILE [OPTIONS]
```

**Options:**
- `--leads-file` (required): CSV file with leads to monitor
- `--schedule`: Frequency - `daily` or `weekly` (default: weekly)
- `--alert-threshold`: Score threshold for alerts (default: 60)
- `--time`: Time to run in HHMM format (default: 0900)

**Other Commands:**
```bash
# Check monitoring status
./schedule_monitoring.sh status

# Test monitoring without scheduling
./schedule_monitoring.sh test --leads-file leads.csv

# Remove monitoring
./schedule_monitoring.sh remove
```

**Examples:**

```bash
# Basic weekly monitoring
./schedule_monitoring.sh setup --leads-file leads.csv

# Daily monitoring with custom threshold
./schedule_monitoring.sh setup \
  --leads-file leads.csv \
  --schedule daily \
  --alert-threshold 70

# Custom time (2 PM daily)
./schedule_monitoring.sh setup \
  --leads-file leads.csv \
  --schedule daily \
  --time 1400

# Check current status
./schedule_monitoring.sh status

# Test before scheduling
./schedule_monitoring.sh test --leads-file leads.csv --alert-threshold 70
```

**Setup Output:**
```
============================================================
SETTING UP MONITORING
============================================================

✓ Monitoring set up successfully!

Configuration:
  Leads File: /full/path/to/leads.csv
  Schedule: Weekly on Monday at 09:00
  Alert Threshold: 60
  Log File: /full/path/to/monitoring.log

ℹ To view logs: tail -f /full/path/to/monitoring.log
ℹ To check status: ./schedule_monitoring.sh status
ℹ To remove: ./schedule_monitoring.sh remove
```

**Monitoring Output:**
```
============================================================
MONITORING RUN: 2026-01-20 09:00:00
============================================================
Monitoring 10 leads (threshold: 60)
Schedule: weekly
------------------------------------------------------------
🔔 ALERT: stripe.com - Score 75/100
   gusto.com - Score 45/100
🔔 ALERT: datadog.com - Score 65/100
   snowflake.com - Score 30/100

============================================================
⚠️  2 HIGH-INTENT ALERTS
============================================================

Stripe (stripe.com)
  Score: 75/100 (High intent)
  Action: 🔥 High priority lead! Prioritize immediate outreach.

Datadog (datadog.com)
  Score: 65/100 (High intent)
  Action: 🔥 High priority lead! Prioritize immediate outreach.

✓ Alerts saved to: alerts_20260120.json

Next weekly check scheduled
```

---

### CLI Best Practices

**1. Use Industry Presets**
```bash
# Start with a preset, then customize if needed
./run_enrichment.sh preset --use fintech
./run_enrichment.sh enrich --domain stripe.com
```

**2. Batch Processing with Checkpoints**
```bash
# Process large lists in batches
./run_enrichment.sh batch --input batch1.csv --output-file results1.csv
./run_enrichment.sh batch --input batch2.csv --output-file results2.csv
```

**3. Automate with Cron**
```bash
# Set up weekly monitoring for high-value leads
./schedule_monitoring.sh setup --leads-file high_value_leads.csv --alert-threshold 70
```

**4. Pipeline Integration**
```bash
# Use JSON output for pipeline processing
./run_enrichment.sh enrich --domain example.com --output json | jq '.custom_signals.total_score'

# Batch with JSON for further processing
./run_enrichment.sh batch --input leads.csv --format json > results.json
```

**5. Testing New Presets**
```bash
# Test a preset on a few leads first
./run_enrichment.sh preset --show security
./run_enrichment.sh enrich --domain test.com --preset security
```

---

### Troubleshooting CLI

**Script not executable:**
```bash
chmod +x run_enrichment.sh schedule_monitoring.sh
```

**Missing .env file:**
```bash
cp .env.example .env
# Edit .env and add your API credentials
```

**Virtual environment issues:**
```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**View monitoring logs:**
```bash
tail -f monitoring.log
```

**Test without making changes:**
```bash
./schedule_monitoring.sh test --leads-file leads.csv
```

---

## Configuration Guide

### How to Define Custom Signals

Signals are defined in `config.py` as dictionaries. Each signal has:

```python
'signal_name': {
    'enabled': True,              # Turn signal on/off
    'keywords': ['keyword1', ...], # Terms to search for
    'weight': 30,                  # Importance (0-100)
    'query_template': '{company_name} {keyword}'  # Search query format
}
```

### Signal Weight Guidelines

Weights determine how much each signal contributes to the total score. They should sum to **approximately 100**.

| Weight Range | Usage | Example |
|--------------|-------|---------|
| **30-40** | Critical buying signals | Recent security breach, active migration |
| **20-30** | Strong indicators | Relevant hiring, technology adoption |
| **15-20** | Supporting signals | Strategic mentions, industry trends |
| **10-15** | Context signals | General interest, exploration |

**Example weighting strategy:**
```python
CUSTOM_SIGNALS = {
    'critical_pain_point': {'weight': 35},  # Highest - clear need
    'active_hiring': {'weight': 30},        # High - growth indicator
    'tech_adoption': {'weight': 20},        # Medium - stack compatibility
    'strategic_mention': {'weight': 15}     # Lower - future opportunity
}
# Total: 100
```

### Query Template Examples

Templates control how search queries are constructed. Use placeholders:

**Available placeholders:**
- `{company_name}`: The company name
- `{domain}`: The company domain
- `{keyword}`: Each keyword from the signal's keyword list

**Template patterns:**

| Pattern | Example | Use Case |
|---------|---------|----------|
| `{company_name} {keyword}` | "Acme data breach" | General signal detection |
| `{company_name} hiring {keyword}` | "Acme hiring DevOps" | Job postings |
| `{company_name} uses {keyword}` | "Acme uses Kubernetes" | Technology adoption |
| `{keyword} at {company_name}` | "API issues at Acme" | Pain point discovery |
| `{company_name} migrating to {keyword}` | "Acme migrating to AWS" | Active transitions |

**Advanced example:**
```python
'migration_signals': {
    'enabled': True,
    'keywords': ['Salesforce', 'HubSpot', 'Marketo'],
    'weight': 35,
    # Catches: "switching from X", "moving away from X"
    'query_template': '{company_name} switching from {keyword}'
}
```

### Industry-Specific Tips

#### SaaS/B2B Software
- **Focus on:** Integration announcements, API launches, tech stack
- **High weight:** Platform migrations (30-35%)
- **Keywords:** "API launch", "new integration", "developer platform"

#### Developer Tools
- **Focus on:** Performance issues, framework adoption, infrastructure
- **High weight:** API performance problems (30-35%)
- **Keywords:** "API downtime", "slow response", "scaling issues"

#### HR Technology
- **Focus on:** Hiring surges, onboarding challenges, ATS problems
- **High weight:** Rapid growth signals (30-35%)
- **Keywords:** "hiring spree", "rapid expansion", "100+ employees"

#### Cybersecurity
- **Focus on:** Security incidents, compliance needs, audit mentions
- **High weight:** Recent breaches (35-40%)
- **Keywords:** "data breach", "security incident", "SOC 2 audit"

**Pro tip:** Test keywords before committing. Run `test_enrichment.py --single` with different configs to see what works.

---

## Usage Examples

### 1. Single Lead Enrichment

Basic enrichment for one company:

```python
from enrichment_engine import CustomEnrichmentEngine

engine = CustomEnrichmentEngine()

# Enrich a lead
result = engine.enrich_with_custom_signals(
    domain="stripe.com",
    company_name="Stripe"
)

# Access the data
print(f"Intent: {result['custom_signals']['intent_level']}")
print(f"Score: {result['custom_signals']['total_score']}/100")

# Check which signals fired
for signal_name, data in result['custom_signals']['detected_signals'].items():
    if data['detected']:
        print(f"✓ {signal_name}: {len(data['evidence'])} sources")
```

### 2. Batch Processing

Enrich multiple leads efficiently:

```python
import csv
from enrichment_engine import CustomEnrichmentEngine

# Read leads from CSV
leads = []
with open('leads.csv', 'r') as f:
    reader = csv.DictReader(f)
    leads = list(reader)

# Enrich all leads
engine = CustomEnrichmentEngine()
enriched = []

for lead in leads:
    result = engine.enrich_with_custom_signals(
        domain=lead['domain'],
        company_name=lead['company_name']
    )
    enriched.append(result)

# Filter for high-intent leads
high_intent = [
    lead for lead in enriched
    if lead['custom_signals']['intent_level'] == 'High'
]

print(f"Found {len(high_intent)} high-intent leads out of {len(leads)}")

# Export to JSON
import json
with open('high_intent_leads.json', 'w') as f:
    json.dump(high_intent, f, indent=2)
```

### 3. CRM Integration Pattern

Combine with existing CRM data:

```python
from enrichment_engine import CustomEnrichmentEngine
import salesforce_api  # Example: your CRM library

engine = CustomEnrichmentEngine()

# Fetch leads from Salesforce
sf_leads = salesforce_api.query("SELECT Name, Domain__c FROM Lead WHERE Status = 'Open'")

for lead in sf_leads:
    # Enrich with custom signals
    enriched = engine.enrich_with_custom_signals(
        domain=lead['Domain__c'],
        company_name=lead['Name']
    )

    # Update Salesforce with intent score
    salesforce_api.update('Lead', lead['Id'], {
        'Intent_Score__c': enriched['custom_signals']['total_score'],
        'Intent_Level__c': enriched['custom_signals']['intent_level'],
        'Last_Enriched__c': enriched['enrichment_date']
    })

    # If high intent, create task for sales rep
    if enriched['custom_signals']['intent_level'] == 'High':
        salesforce_api.create('Task', {
            'WhoId': lead['Id'],
            'Subject': 'High Intent Lead - Immediate Follow-up',
            'Description': enriched['custom_signals']['recommendation']
        })
```

### 4. Custom Output Formats

Export enriched data in various formats:

**JSON Export:**
```python
import json

enriched_leads = [...]  # Your enriched data

with open('leads.json', 'w') as f:
    json.dump(enriched_leads, f, indent=2)
```

**CSV Export:**
```python
import csv

with open('leads.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Company', 'Domain', 'Score', 'Intent', 'Recommendation'])

    for lead in enriched_leads:
        writer.writerow([
            lead['company_name'],
            lead['domain'],
            lead['custom_signals']['total_score'],
            lead['custom_signals']['intent_level'],
            lead['custom_signals']['recommendation']
        ])
```

**Markdown Report:**
```python
def export_markdown(enriched_leads, filename='report.md'):
    with open(filename, 'w') as f:
        f.write("# Lead Enrichment Report\n\n")

        for lead in enriched_leads:
            signals = lead['custom_signals']
            f.write(f"## {lead['company_name']}\n\n")
            f.write(f"- **Domain**: {lead['domain']}\n")
            f.write(f"- **Score**: {signals['total_score']}/100\n")
            f.write(f"- **Intent**: {signals['intent_level']}\n")
            f.write(f"- **Recommendation**: {signals['recommendation']}\n\n")

            f.write("**Conversation Starters:**\n")
            for starter in lead['conversation_starters']:
                f.write(f"- {starter}\n")
            f.write("\n---\n\n")
```

---

## API Reference

### CustomEnrichmentEngine

Main class for lead enrichment.

**Initialization:**
```python
engine = CustomEnrichmentEngine(signal_tracker=None)
```

Parameters:
- `signal_tracker` (SignalTracker, optional): Custom signal tracker instance

---

#### `enrich_with_custom_signals(domain, company_name=None, existing_data=None)`

Enriches a lead with custom buying signals.

**Parameters:**
- `domain` (str, required): Company domain (e.g., "acme.com")
- `company_name` (str, optional): Company name. Auto-derived from domain if not provided
- `existing_data` (dict, optional): Existing lead data to preserve

**Returns:**
```python
{
    'enrichment_date': '2026-01-20T23:15:42.123456',  # ISO timestamp
    'domain': 'acme.com',
    'company_name': 'Acme Corporation',
    'custom_signals': {
        'total_score': 75,                             # 0-100
        'intent_level': 'High',                        # High/Medium/Low
        'detected_signals': {                          # Signal breakdown
            'hiring_signals': {
                'detected': True,
                'weight': 30,
                'evidence': [...]
            },
            # ... other signals
        },
        'recommendation': 'High priority lead! ...'    # Action item
    },
    'conversation_starters': [                         # 3 personalized openers
        'Saw you\'re hiring for...',
        'Noticed you\'re working with...',
        'Read about your...'
    ],
    'standard_data': {}                                # Preserved existing data
}
```

**Example:**
```python
profile = engine.enrich_with_custom_signals(
    domain="anthropic.com",
    company_name="Anthropic",
    existing_data={"industry": "AI", "employees": 500}
)
```

---

### SignalTracker

Tracks buying signals using SERP data.

**Initialization:**
```python
from signal_tracker import SignalTracker
tracker = SignalTracker(serp_client=None)
```

---

#### `track_signals(domain, company_name=None)`

Tracks all enabled signals for a company.

**Parameters:**
- `domain` (str, required): Company domain
- `company_name` (str, optional): Company name

**Returns:**
```python
{
    'company_name': 'Acme Corporation',
    'domain': 'acme.com',
    'total_score': 55,
    'intent_level': 'Medium',
    'signals': {                                       # Detected signals
        'hiring_signals': {
            'detected': True,
            'weight': 30,
            'evidence': [
                {
                    'source': 'Page title',
                    'url': 'https://...',
                    'matched_keywords': ['data engineer'],
                    'snippet': 'First 150 chars...'
                }
            ]
        },
        # ... other signals
    },
    'recommendation': 'Medium intent. 2 signal(s) detected...'
}
```

---

### SerpClient

Client for Bright Data SERP API.

**Initialization:**
```python
from serp_client import SerpClient
client = SerpClient()
```

---

#### `query(keyword, gl='us', hl='en')`

Execute a search query.

**Parameters:**
- `keyword` (str, required): Search query
- `gl` (str, optional): Country code (default: 'us')
- `hl` (str, optional): Language code (default: 'en')

**Returns:** JSON response from SERP API or `{"results": []}` on error

---

#### `search_for_signals(query, result_count=3)`

Search and format results for signal detection.

**Parameters:**
- `query` (str, required): Search query
- `result_count` (int, optional): Max results to return (default: 3)

**Returns:**
```python
[
    {
        'title': 'Page title',
        'url': 'https://...',
        'description': 'Full description text',
        'snippet': 'First 150 chars...'
    },
    # ... more results
]
```

---

### Error Handling

All methods handle errors gracefully:

- **Invalid domains**: Returns score of 0, Low intent
- **Missing API credentials**: Raises `ValueError` with clear message
- **Network failures**: Logs error, returns empty results
- **Malformed responses**: Returns empty results, continues processing

**Example error handling:**
```python
try:
    result = engine.enrich_with_custom_signals("invalid.com")
    # Result will have score=0, intent=Low, but won't crash
except ValueError as e:
    print(f"Configuration error: {e}")
    # Handle missing credentials
```

---

## Troubleshooting

### Common Errors and Solutions

#### ❌ "SERP_API_KEY is required. Please set it in your .env file."

**Cause:** Missing or incorrect API credentials

**Solution:**
1. Verify `.env` file exists in project root
2. Check that `SERP_API_KEY` is set (no quotes needed)
3. Ensure no extra spaces: `SERP_API_KEY=abc123` not `SERP_API_KEY = abc123`
4. Restart Python session after editing `.env`

```bash
# Correct format
SERP_API_KEY=your_key_here
SERP_ZONE=your_zone_here
```

---

#### ❌ "SERP API request failed: 401 Unauthorized"

**Cause:** Invalid API key or zone name

**Solution:**
1. Log in to Bright Data dashboard
2. Verify API key is active and not expired
3. Check zone name matches exactly (case-sensitive)
4. Ensure API key has SERP API permissions

---

#### ❌ "SERP API request failed: 429 Too Many Requests"

**Cause:** Rate limiting (too many API calls)

**Solution:**
1. Add delays between requests:
   ```python
   import time
   for lead in leads:
       result = engine.enrich_with_custom_signals(lead['domain'])
       time.sleep(2)  # 2 second delay
   ```
2. Check your Bright Data plan limits
3. Implement exponential backoff for retries
4. Consider upgrading API plan for higher limits

---

#### ❌ All signals showing as "not detected" despite valid company

**Cause:** Keywords may not match search results, or results filtered out

**Solution:**
1. Test keywords manually on Google to verify they return results
2. Check query template formats - try simpler templates
3. Adjust description length filter in `serp_client.py` (60-600 chars)
4. Try more general keywords first, then refine
5. Increase `result_count` in signal detection:
   ```python
   results = self.serp.search_for_signals(query, result_count=5)  # Default: 3
   ```

---

#### ❌ "Signal weights sum to X, not 100"

**Cause:** Warning that weights don't total 100 (still functional)

**Solution:** Adjust weights in `config.py` to total 100:
```python
# Before (total: 90)
'signal_1': {'weight': 30},
'signal_2': {'weight': 30},
'signal_3': {'weight': 30}

# After (total: 100)
'signal_1': {'weight': 35},
'signal_2': {'weight': 35},
'signal_3': {'weight': 30}
```

---

### API Rate Limiting

**Bright Data SERP API limits vary by plan.** Check your dashboard for specifics.

**Best practices:**
```python
import time
from datetime import datetime

def enrich_with_rate_limit(domains, requests_per_minute=10):
    """Enrich leads with rate limiting"""
    engine = CustomEnrichmentEngine()
    delay = 60 / requests_per_minute

    results = []
    for i, domain in enumerate(domains):
        print(f"[{i+1}/{len(domains)}] Enriching {domain}...")
        result = engine.enrich_with_custom_signals(domain)
        results.append(result)

        # Wait between requests
        if i < len(domains) - 1:
            time.sleep(delay)

    return results
```

---

### Empty Results Handling

If consistently getting empty results:

**1. Verify API is working:**
```python
from serp_client import SerpClient

client = SerpClient()
results = client.query("test query")
print(results)  # Should return search results
```

**2. Test with well-known company:**
```python
result = engine.enrich_with_custom_signals("google.com", "Google")
# Google should trigger multiple signals
```

**3. Check logs for errors:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
# Re-run enrichment to see detailed logs
```

---

### Configuration Issues

**Signal not triggering:**
1. Verify signal is `enabled: True`
2. Check keywords are in the actual search results
3. Test query template manually on Google
4. Review logs for "Signal detected" messages

**Scores seem incorrect:**
1. Verify all weights sum to 100
2. Check which signals are firing with `print(result['custom_signals']['detected_signals'])`
3. Adjust weights based on your priorities

**Need help?** Run `python test_enrichment.py --errors` to test error handling.

---

## Production Deployment

### Scaling Considerations

**Batch Size:**
- Optimal: **10-50 leads per batch**
- Include 1-2 second delays between requests
- Use async processing for larger volumes

**Example batch processor:**
```python
def process_leads_in_batches(leads, batch_size=20):
    """Process leads in manageable batches"""
    import time
    from enrichment_engine import CustomEnrichmentEngine

    engine = CustomEnrichmentEngine()
    all_results = []

    for i in range(0, len(leads), batch_size):
        batch = leads[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}...")

        for lead in batch:
            result = engine.enrich_with_custom_signals(
                domain=lead['domain'],
                company_name=lead.get('name')
            )
            all_results.append(result)
            time.sleep(1.5)  # Rate limiting

        # Checkpoint: save progress after each batch
        with open(f'checkpoint_batch_{i//batch_size}.json', 'w') as f:
            json.dump(all_results, f)

    return all_results
```

---

### Cost Optimization

**Bright Data pricing:** Pay per SERP API request

**Optimization strategies:**

**1. Cache results:**
```python
import json
from datetime import datetime, timedelta

def get_cached_or_enrich(domain, cache_days=7):
    """Use cached results if recent, otherwise re-enrich"""
    cache_file = f"cache/{domain}.json"

    # Check cache
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached = json.load(f)
            enrichment_date = datetime.fromisoformat(cached['enrichment_date'])

            # Use cache if less than 7 days old
            if datetime.utcnow() - enrichment_date < timedelta(days=cache_days):
                print(f"Using cached data for {domain}")
                return cached

    # Enrich and cache
    result = engine.enrich_with_custom_signals(domain)
    with open(cache_file, 'w') as f:
        json.dump(result, f)

    return result
```

**2. Pre-filter leads:**
Only enrich leads that meet basic criteria:
```python
def should_enrich(lead):
    """Filter leads before expensive enrichment"""
    # Only enrich if domain is valid and employee count > 50
    return (
        lead.get('domain') and
        lead.get('employee_count', 0) > 50 and
        lead.get('industry') in ['Software', 'Technology']
    )

leads_to_enrich = [lead for lead in all_leads if should_enrich(lead)]
```

**3. Reduce result_count:**
Lower `result_count` for faster, cheaper queries:
```python
# In serp_client.py, search_for_signals() method
results = self.serp.search_for_signals(query, result_count=2)  # Default: 3
```

**4. Disable low-value signals:**
Turn off signals that rarely fire or provide little value:
```python
# In config.py
'low_value_signal': {
    'enabled': False,  # Disable to reduce API calls
    ...
}
```

---

### Integration Patterns

**Webhook Integration:**
```python
from flask import Flask, request, jsonify
from enrichment_engine import CustomEnrichmentEngine

app = Flask(__name__)
engine = CustomEnrichmentEngine()

@app.route('/enrich', methods=['POST'])
def enrich_lead():
    """Webhook endpoint for enrichment"""
    data = request.json
    result = engine.enrich_with_custom_signals(
        domain=data['domain'],
        company_name=data.get('company_name')
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000)
```

**Scheduled Batch Job:**
```python
# scheduled_enrichment.py
import schedule
import time

def daily_enrichment():
    """Run enrichment daily on new leads"""
    # Fetch new leads from CRM
    new_leads = fetch_new_leads_from_crm()

    # Enrich them
    engine = CustomEnrichmentEngine()
    for lead in new_leads:
        result = engine.enrich_with_custom_signals(lead['domain'])
        update_crm_with_results(lead['id'], result)

# Schedule job
schedule.every().day.at("02:00").do(daily_enrichment)

while True:
    schedule.run_pending()
    time.sleep(60)
```

**Cloud Function (AWS Lambda):**
```python
import json
from enrichment_engine import CustomEnrichmentEngine

def lambda_handler(event, context):
    """AWS Lambda function for enrichment"""
    engine = CustomEnrichmentEngine()

    domain = event['domain']
    company_name = event.get('company_name')

    result = engine.enrich_with_custom_signals(domain, company_name)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

---

### Monitoring and Logging

**Setup comprehensive logging:**
```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'enrichment_{datetime.now().date()}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Track metrics
class EnrichmentMetrics:
    def __init__(self):
        self.total_enriched = 0
        self.high_intent = 0
        self.api_errors = 0
        self.start_time = datetime.now()

    def record_enrichment(self, result):
        self.total_enriched += 1
        if result['custom_signals']['intent_level'] == 'High':
            self.high_intent += 1

    def record_error(self):
        self.api_errors += 1

    def report(self):
        duration = datetime.now() - self.start_time
        logger.info(f"""
        Enrichment Session Report:
        - Total Enriched: {self.total_enriched}
        - High Intent Found: {self.high_intent}
        - API Errors: {self.api_errors}
        - Duration: {duration}
        - Success Rate: {(1 - self.api_errors/self.total_enriched)*100:.1f}%
        """)
```

**Monitor API usage:**
```python
def monitor_api_usage():
    """Track API call volume"""
    import os
    from collections import Counter

    # Count API calls from logs
    with open('enrichment.log', 'r') as f:
        logs = f.readlines()
        api_calls = [line for line in logs if 'Querying SERP API' in line]

    print(f"Total API calls today: {len(api_calls)}")

    # Estimate cost (example: $0.01 per request)
    estimated_cost = len(api_calls) * 0.01
    print(f"Estimated cost: ${estimated_cost:.2f}")
```

---

## Project Structure

```
custom-enrichment-layer/
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── config.py                # Signal definitions and configuration
├── requirements.txt         # Python dependencies
├── serp_client.py          # Bright Data SERP API client
├── signal_tracker.py       # Signal detection logic
├── enrichment_engine.py    # Main enrichment orchestrator
├── test_enrichment.py      # Comprehensive test suite
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guidelines
│
├── example_configs/        # Industry-specific configurations
│   ├── README.md
│   ├── devtools_config.py
│   ├── hrtech_config.py
│   ├── security_config.py
│   └── saas_config.py
│
└── examples/               # Example outputs
    ├── example_output.txt
    ├── example_signals.json
    └── example_signals.csv
```

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Adding new signal types
- Creating industry configs
- Improving detection accuracy
- Optimizing performance

---

## Security Notes

- **Never commit `.env` files** to version control
- **Rotate API credentials** regularly (every 90 days recommended)
- **Use environment-specific credentials** for dev/staging/production
- **Monitor API usage** to prevent unexpected charges
- **Sanitize outputs** before logging or exporting

---

## Support and Resources

- **Bright Data Documentation:** https://docs.brightdata.com/
- **SERP API Guide:** https://docs.brightdata.com/serp-api
- **Issue Tracker:** (Add your GitHub issues link)
- **API Status:** Check Bright Data dashboard for service status

---

## License

Internal use only. All rights reserved.

---

**Built with ❤️ using Bright Data SERP API**
