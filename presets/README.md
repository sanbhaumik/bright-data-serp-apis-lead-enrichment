# Industry Signal Presets

Ready-to-use signal configurations optimized for 8 major industries. Load a preset and start enriching leads in minutes—no configuration needed.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Available Presets](#available-presets)
- [Usage Examples](#usage-examples)
- [Customizing Presets](#customizing-presets)
- [Creating Custom Presets](#creating-custom-presets)

---

## Quick Start

### Load and Use a Preset

```python
from presets.load_preset import apply_preset
from enrichment_engine import CustomEnrichmentEngine

# Apply DevTools preset
apply_preset('devtools')

# Start enriching
engine = CustomEnrichmentEngine()
result = engine.enrich_with_custom_signals('stripe.com', 'Stripe')

print(f"Score: {result['custom_signals']['total_score']}/100")
print(f"Intent: {result['custom_signals']['intent_level']}")
```

### List Available Presets

```python
from presets.load_preset import PresetLoader

loader = PresetLoader()
presets = loader.list_available_presets()
print(presets)
# ['data', 'devtools', 'fintech', 'hrtech', 'infrastructure', 'martech', 'saas', 'security']
```

---

## Available Presets

### 1. Developer Tools (`devtools.json`)

**Industry:** Developer Tools & API Platforms

**Best For:** API management, monitoring tools, infrastructure platforms, developer tools

**Signals Tracked:**
- **API Performance Issues (30%)**: Downtime, slow responses, rate limiting
- **Framework Adoption (20%)**: Next.js, React, TypeScript, GraphQL
- **Infrastructure Challenges (25%)**: Scaling issues, Kubernetes, microservices
- **Developer Hiring (20%)**: DevOps, Backend, SRE roles
- **API Launches (15%)**: Public API announcements, developer platforms

**Example Companies:** Stripe, Twilio, Plaid, Segment

**Use When:** Targeting companies with API/infrastructure challenges or launching developer platforms

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('devtools')
```

---

### 2. HR Technology (`hrtech.json`)

**Industry:** HR Technology & Recruiting

**Best For:** ATS platforms, HRIS, onboarding tools, recruiting automation

**Signals Tracked:**
- **Rapid Growth (30%)**: Hiring surges, team scaling, workforce expansion
- **HR Process Challenges (25%)**: Manual processes, inefficiencies
- **Onboarding Issues (20%)**: New hire experience, remote onboarding
- **ATS/Recruiting Problems (15%)**: Applicant tracking issues, candidate experience
- **Remote Work Transition (10%)**: Distributed teams, hybrid workforce

**Example Companies:** Gusto, Rippling, Greenhouse, Workday

**Use When:** Targeting high-growth companies or those with HR pain points

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('hrtech')
```

---

### 3. Cybersecurity (`security.json`)

**Industry:** Cybersecurity & Compliance

**Best For:** Security tools, compliance platforms, pentesting services, security consulting

**Signals Tracked:**
- **Security Incidents (35%)**: Breaches, vulnerabilities, cyberattacks
- **Compliance Requirements (30%)**: SOC 2, ISO 27001, GDPR, HIPAA
- **Vulnerability Assessments (20%)**: Pentesting, security audits
- **Security Hiring (10%)**: CISO, Security Engineers, Analysts
- **Regulatory Pressure (5%)**: Data protection, privacy requirements

**Example Companies:** Cloudflare, Okta, CrowdStrike, Palo Alto Networks

**Use When:** Targeting companies post-breach or seeking compliance certifications

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('security')
```

---

### 4. Data & Analytics (`data.json`)

**Industry:** Data & Analytics Tools

**Best For:** Data warehouses, ETL tools, BI platforms, data observability

**Signals Tracked:**
- **Data Quality Issues (35%)**: Accuracy problems, inconsistencies, reliability
- **Data Engineering Hiring (25%)**: Data engineers, Analytics engineers, ML engineers
- **Modern Data Stack (20%)**: Snowflake, Databricks, dbt adoption
- **Reporting Challenges (15%)**: Slow reporting, manual processes, data silos
- **Data Transformation (5%)**: Data strategy, analytics transformation

**Example Companies:** Snowflake, Databricks, Fivetran, Looker

**Use When:** Targeting companies with data quality or reporting challenges

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('data')
```

---

### 5. Financial Technology (`fintech.json`)

**Industry:** Financial Technology

**Best For:** Payment processors, fraud detection, KYC/AML tools, financial infrastructure

**Signals Tracked:**
- **Payment Processing Issues (30%)**: Payment failures, transaction delays
- **Regulatory Compliance (25%)**: KYC, AML, PSD2, banking compliance
- **Fraud & Security (25%)**: Fraud detection, transaction security, chargebacks
- **International Expansion (15%)**: Cross-border payments, multi-currency
- **FinTech Hiring (5%)**: Risk Analysts, Compliance Officers, Payment Engineers

**Example Companies:** Stripe, Square, Plaid, Adyen

**Use When:** Targeting companies with payment, compliance, or fraud concerns

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('fintech')
```

---

### 6. SaaS Platforms (`saas.json`)

**Industry:** SaaS Platforms

**Best For:** Integration platforms, API tools, customer data platforms, product analytics

**Signals Tracked:**
- **Platform Migrations (30%)**: Switching software, replacing systems
- **Integration Launches (25%)**: New integrations, app marketplace
- **Scalability Challenges (25%)**: Performance problems, downtime
- **Product Expansion (15%)**: New product launches, feature announcements
- **Customer Experience Issues (5%)**: User complaints, churn

**Example Companies:** Slack, Notion, Airtable, Monday.com

**Use When:** Targeting SaaS companies building ecosystems or experiencing scaling issues

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('saas')
```

---

### 7. Marketing Technology (`martech.json`)

**Industry:** Marketing Technology

**Best For:** Marketing analytics, attribution tools, automation platforms

**Signals Tracked:**
- **Attribution Challenges (30%)**: ROI tracking, multi-touch attribution
- **Marketing Automation (25%)**: Email automation, campaign automation
- **Campaign Performance (25%)**: Low conversion rates, ad spend optimization
- **Marketing Hiring (15%)**: Growth Marketing, Demand Generation roles
- **MarTech Stack (5%)**: HubSpot, Marketo, martech consolidation

**Example Companies:** HubSpot, Marketo, Segment, Braze

**Use When:** Targeting companies with attribution or campaign performance issues

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('martech')
```

---

### 8. Infrastructure & Cloud (`infrastructure.json`)

**Industry:** Infrastructure & Cloud

**Best For:** Cloud platforms, infrastructure monitoring, CDN, DevOps tools

**Signals Tracked:**
- **Cloud Migration (30%)**: Moving to AWS/Azure/GCP, cloud-first strategy
- **Infrastructure Incidents (30%)**: Downtime, outages, service disruptions
- **Scaling Challenges (20%)**: Performance bottlenecks, load balancing
- **Infrastructure Modernization (15%)**: Kubernetes, containerization, serverless
- **Infrastructure Hiring (5%)**: SRE, Cloud Architects, Platform Engineers

**Example Companies:** Cloudflare, Datadog, New Relic, PagerDuty

**Use When:** Targeting companies migrating to cloud or experiencing infrastructure issues

**Quick Start:**
```python
from presets.load_preset import apply_preset
apply_preset('infrastructure')
```

---

## Usage Examples

### Example 1: Basic Preset Usage

```python
from presets.load_preset import apply_preset
from enrichment_engine import CustomEnrichmentEngine

# Apply HR Tech preset
apply_preset('hrtech')

# Enrich leads
engine = CustomEnrichmentEngine()

companies = [
    ('gusto.com', 'Gusto'),
    ('rippling.com', 'Rippling'),
    ('bamboohr.com', 'BambooHR')
]

for domain, name in companies:
    result = engine.enrich_with_custom_signals(domain, name)
    print(f"{name}: {result['custom_signals']['intent_level']} intent")
```

**Output:**
```
✓ Applied preset: HR Technology & Recruiting
  Signals loaded: 5

Gusto: High intent
Rippling: High intent
BambooHR: Medium intent
```

---

### Example 2: Compare Multiple Presets

```python
from presets.load_preset import PresetLoader

loader = PresetLoader()

# Get info for multiple presets
for preset_name in ['devtools', 'security', 'data']:
    info = loader.get_preset_info(preset_name)
    print(f"\n{info['industry']}")
    print(f"  Signals: {info['signal_count']}")
    print(f"  Use Case: {info['typical_use_case'][:80]}...")
```

---

### Example 3: Inspect Preset Before Using

```python
from presets.load_preset import load_preset
import json

# Load preset without applying
preset = load_preset('fintech')

print(f"Industry: {preset['industry']}")
print(f"Description: {preset['description']}\n")

print("Signals:")
for signal_name, signal_data in preset['signals'].items():
    print(f"  • {signal_name}: {signal_data['weight']}%")
    print(f"    Keywords: {', '.join(signal_data['keywords'][:3])}...")
```

**Output:**
```
Industry: Financial Technology
Description: Tracks signals for companies dealing with payment processing...

Signals:
  • payment_processing_issues: 30%
    Keywords: payment processing issues, payment failures, transaction delays...
  • regulatory_compliance: 25%
    Keywords: KYC compliance, AML requirements, PSD2...
```

---

### Example 4: Switch Between Presets

```python
from presets.load_preset import apply_preset
from enrichment_engine import CustomEnrichmentEngine

engine = CustomEnrichmentEngine()

# Test with DevTools preset
apply_preset('devtools')
result1 = engine.enrich_with_custom_signals('stripe.com', 'Stripe')
print(f"DevTools preset score: {result1['custom_signals']['total_score']}")

# Switch to FinTech preset
apply_preset('fintech')
result2 = engine.enrich_with_custom_signals('stripe.com', 'Stripe')
print(f"FinTech preset score: {result2['custom_signals']['total_score']}")

# Different presets = different scores for the same company
```

---

### Example 5: Batch Processing with Preset

```python
import csv
from presets.load_preset import apply_preset
from enrichment_engine import CustomEnrichmentEngine

# Apply preset
apply_preset('security')

# Load leads from CSV
leads = []
with open('security_leads.csv', 'r') as f:
    reader = csv.DictReader(f)
    leads = list(reader)

# Enrich all leads
engine = CustomEnrichmentEngine()
high_intent_leads = []

for lead in leads:
    result = engine.enrich_with_custom_signals(lead['domain'], lead['name'])

    if result['custom_signals']['intent_level'] == 'High':
        high_intent_leads.append(result)

print(f"Found {len(high_intent_leads)} high-intent security leads")

# Export high-intent leads
with open('high_intent_security_leads.json', 'w') as f:
    json.dump(high_intent_leads, f, indent=2)
```

---

## Customizing Presets

### Method 1: Modify JSON Directly

Edit the preset JSON file:

```json
{
  "industry": "Your Custom Industry",
  "signals": {
    "your_signal": {
      "enabled": true,
      "keywords": ["keyword1", "keyword2"],
      "weight": 30,
      "query_template": "{company_name} {keyword}"
    }
  }
}
```

### Method 2: Modify After Loading

```python
from presets.load_preset import load_preset, apply_preset
import config

# Load base preset
preset = load_preset('devtools')

# Customize it
preset['signals']['custom_signal'] = {
    'enabled': True,
    'keywords': ['your', 'custom', 'keywords'],
    'weight': 10,
    'query_template': '{company_name} {keyword}'
}

# Apply modified preset
config.CUSTOM_SIGNALS = preset['signals']
```

### Method 3: Combine Multiple Presets

```python
from presets.load_preset import load_preset
import config

# Load two presets
devtools = load_preset('devtools')
security = load_preset('security')

# Combine signals (with adjusted weights)
combined_signals = {}

# Add devtools signals at 50% weight
for name, signal in devtools['signals'].items():
    signal['weight'] = signal['weight'] // 2
    combined_signals[f'devtools_{name}'] = signal

# Add security signals at 50% weight
for name, signal in security['signals'].items():
    signal['weight'] = signal['weight'] // 2
    combined_signals[f'security_{name}'] = signal

# Apply combined preset
config.CUSTOM_SIGNALS = combined_signals
```

---

## Creating Custom Presets

### Step 1: Create JSON File

Create `presets/your_industry.json`:

```json
{
  "industry": "Your Industry Name",
  "description": "What this preset tracks and who it's for",
  "signals": {
    "signal_category_1": {
      "enabled": true,
      "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
      ],
      "weight": 35,
      "query_template": "{company_name} {keyword}"
    },
    "signal_category_2": {
      "enabled": true,
      "keywords": ["..."],
      "weight": 30,
      "query_template": "{company_name} {keyword}"
    }
  },
  "example_companies": [
    "company1.com",
    "company2.com"
  ],
  "typical_use_case": "Brief description of when to use this preset"
}
```

### Step 2: Test Your Preset

```python
from presets.load_preset import apply_preset
from enrichment_engine import CustomEnrichmentEngine

# Apply your custom preset
apply_preset('your_industry')

# Test with sample companies
engine = CustomEnrichmentEngine()
result = engine.enrich_with_custom_signals('test.com', 'Test Company')

print(f"Score: {result['custom_signals']['total_score']}/100")
```

### Step 3: Validate Weights

Ensure signal weights sum to 100:

```python
from presets.load_preset import load_preset

preset = load_preset('your_industry')
total_weight = sum(s['weight'] for s in preset['signals'].values())
print(f"Total weight: {total_weight}")  # Should be 100
```

---

## Best Practices

### Choosing the Right Preset

| Your Product | Recommended Preset | Why |
|--------------|-------------------|-----|
| API Gateway | `devtools` | Tracks API performance issues |
| ATS Platform | `hrtech` | Detects hiring surges |
| Security Scanner | `security` | Finds breach victims |
| Data Warehouse | `data` | Identifies data quality issues |
| Payment Gateway | `fintech` | Tracks payment problems |
| iPaaS | `saas` | Detects integration needs |
| Attribution Tool | `martech` | Finds attribution challenges |
| Monitoring Tool | `infrastructure` | Spots downtime incidents |

### When to Customize

- **Different ICP**: Adjust keywords to match your ideal customer profile
- **Niche Market**: Modify signals for specific sub-industries
- **Regional Focus**: Change query templates for non-English markets
- **Competitive Positioning**: Add signals tracking competitor mentions

### Performance Tips

1. **Start with a preset**: Don't build from scratch
2. **Test keywords**: Verify they return relevant results
3. **Adjust weights**: Based on your conversion data
4. **Monitor results**: Track which signals correlate with closed deals
5. **Iterate**: Refine keywords and weights over time

---

## Troubleshooting

### Preset Not Found

```python
# Error: FileNotFoundError: Preset 'mypreset' not found

# Solution: Check spelling and available presets
from presets.load_preset import PresetLoader
loader = PresetLoader()
print(loader.list_available_presets())
```

### Weights Don't Sum to 100

```python
# Warning: Signal weights sum to 95, not 100

# Solution: Adjust weights in JSON file
# Or ignore - it still works, just with proportional scoring
```

### No Signals Detected

```python
# All signals showing as "not detected"

# Possible causes:
# 1. Keywords don't match search results
# 2. Company doesn't have public mentions
# 3. Query template needs adjustment

# Solution: Test keywords manually on Google first
```

---

## Support

- **Main Documentation**: See parent [README.md](../README.md)
- **Examples**: Check [examples/](../examples/) folder
- **Testing**: Run `python load_preset.py` to test presets

---

## Contributing

Have a preset for a new industry? See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Creating new presets
- Improving existing ones
- Sharing with the community

---

**Built for 8 major industries. Load, enrich, close deals.**
