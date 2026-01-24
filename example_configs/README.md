# Industry-Specific Signal Configurations

This folder contains pre-built signal configurations optimized for different industries. Use these as templates or drop-in replacements for the default `config.py`.

## Available Configurations

### 1. Developer Tools (`devtools_config.py`)

**Best for:** Companies selling developer infrastructure, APIs, monitoring tools, or cloud platforms

**Signals:**
- Framework Adoption (25%): Next.js, React, TypeScript, Vue.js
- API Performance (30%): Scaling issues, slow responses, downtime
- Infrastructure Signals (20%): Kubernetes, Docker, microservices
- Developer Hiring (25%): DevOps, Backend, SRE roles

**Use when targeting:** Engineering-heavy companies, API-first businesses, infrastructure platforms

---

### 2. HR Technology (`hrtech_config.py`)

**Best for:** Companies selling ATS, HRIS, onboarding platforms, or recruiting automation

**Signals:**
- Rapid Growth (30%): Hiring surges, team scaling
- HR Challenges (35%): Manual processes, inefficiencies
- Onboarding Pain (20%): New hire experience issues
- Recruiting Tech (15%): ATS problems, software gaps

**Use when targeting:** High-growth companies, companies with 100+ employees, remote-first teams

---

### 3. Cybersecurity (`security_config.py`)

**Best for:** Companies selling security tools, compliance platforms, pentesting, or security services

**Signals:**
- Security Incidents (35%): Breaches, vulnerabilities, attacks
- Compliance Needs (30%): SOC 2, ISO 27001, GDPR
- Vulnerability Mentions (20%): Pentesting, audits, assessments
- Security Hiring (15%): CISO, Security Engineer roles

**Use when targeting:** Recently breached companies, SaaS platforms seeking certification, regulated industries

---

### 4. SaaS (`saas_config.py`)

**Best for:** Companies selling integration platforms, API management, monitoring, or analytics tools

**Signals:**
- Integration Announcements (25%): New integrations, marketplaces
- API Launches (25%): Public APIs, developer programs
- Platform Migrations (30%): Switching software, replacements
- Product Challenges (20%): Bugs, downtime, complaints

**Use when targeting:** SaaS companies building ecosystems, companies launching APIs, platforms with integrations

---

## How to Use These Configurations

### Method 1: Replace Default Config (Simplest)

Replace the signals in your main `config.py`:

```python
# In config.py, replace the CUSTOM_SIGNALS section with:
from example_configs.devtools_config import CUSTOM_SIGNALS

# Rest of config.py remains the same
```

### Method 2: Use Directly in Your Code

Import and use the industry-specific config in your enrichment script:

```python
from example_configs import devtools_config
from signal_tracker import SignalTracker
from serp_client import SerpClient

# Initialize tracker with custom config
serp_client = SerpClient()
tracker = SignalTracker(serp_client)

# Replace the signals configuration
tracker.signals_config = devtools_config.CUSTOM_SIGNALS
tracker.thresholds = devtools_config.INTENT_THRESHOLDS

# Use as normal
result = tracker.track_signals("acme.com", "Acme Corp")
```

### Method 3: Create Custom Config Based on Examples

Copy an example config and customize it:

```bash
cp example_configs/devtools_config.py my_custom_config.py
```

Then edit `my_custom_config.py` with your specific keywords and weights.

---

## Customization Tips

### Adjusting Weights

Weights determine how much each signal contributes to the total score. They should sum to 100:

```python
'signal_name': {
    'weight': 30,  # This signal is worth 30% of total score
    ...
}
```

**Higher weights (30-40%):** Critical pain points or strong buying signals
**Medium weights (20-25%):** Important indicators
**Lower weights (10-15%):** Supporting signals

### Adding Keywords

Add more keywords to increase detection accuracy:

```python
'keywords': [
    'data engineer',
    'machine learning engineer',
    'MLOps engineer',  # Add more specific variants
    'AI engineer'
]
```

### Customizing Query Templates

Templates determine how search queries are constructed:

```python
# Default: Company-centric
'query_template': '{company_name} {keyword}'

# Alternative: Industry-wide
'query_template': '{keyword} challenges {company_name}'

# Hiring-specific
'query_template': '{company_name} hiring {keyword}'

# Technology-specific
'query_template': '{company_name} uses {keyword}'
```

---

## Testing Your Configuration

After customizing a config, test it:

```python
# test_config.py
from my_custom_config import CUSTOM_SIGNALS, INTENT_THRESHOLDS

# Verify weights sum to 100
total_weight = sum(s['weight'] for s in CUSTOM_SIGNALS.values() if s['enabled'])
print(f"Total weight: {total_weight}")  # Should be ~100

# Test with real company
from enrichment_engine import CustomEnrichmentEngine
engine = CustomEnrichmentEngine()

# Update config before running
import config
config.CUSTOM_SIGNALS = CUSTOM_SIGNALS
config.INTENT_THRESHOLDS = INTENT_THRESHOLDS

result = engine.enrich_with_custom_signals("testcompany.com")
print(result)
```

---

## Best Practices

1. **Start with existing configs**: Use the closest industry match and customize from there
2. **Test keywords**: Not all keywords will have good SERP data - test and iterate
3. **Weight by importance**: Put highest weights on strongest buying signals
4. **Keep it focused**: 4-5 signals is optimal - more than 6 can dilute results
5. **Update regularly**: Refresh keywords quarterly based on market trends

---

## Need Help?

- Check the main `config.py` for structure reference
- Run `python config.py` to validate your configuration
- Test with `python enrichment_engine.py` to see full pipeline

---

## Contributing

Created a great config for your industry? Consider adding it to this folder! Follow the same structure:
- 4-5 signals
- Weights sum to ~100
- Clear, descriptive comments
- Industry-specific keywords
