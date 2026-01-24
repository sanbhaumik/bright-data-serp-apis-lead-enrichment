# Contributing to Custom Lead Enrichment Engine

Thank you for your interest in contributing! This guide will help you extend and improve the lead enrichment engine.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Ways to Contribute](#ways-to-contribute)
- [Adding New Signal Types](#adding-new-signal-types)
- [Creating Industry Configurations](#creating-industry-configurations)
- [Improving Detection Accuracy](#improving-detection-accuracy)
- [Performance Optimization](#performance-optimization)
- [Testing Guidelines](#testing-guidelines)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Development environment set up**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Valid Bright Data API credentials** in `.env`

3. **Tested the existing code**
   ```bash
   python test_enrichment.py
   ```

### Development Workflow

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Document your changes
5. Submit your contribution

---

## Ways to Contribute

### 🎯 High-Value Contributions

1. **New Signal Types**: Add detection for new buying signals
2. **Industry Configs**: Create configurations for new industries
3. **Accuracy Improvements**: Better keyword matching and filtering
4. **Performance Optimizations**: Reduce API calls or processing time
5. **Documentation**: Improve guides, add examples, fix errors

### 🐛 Bug Reports

Found a bug? Please include:
- Python version
- Operating system
- Error message and full traceback
- Steps to reproduce
- Expected vs actual behavior

### 💡 Feature Requests

Have an idea? Describe:
- The problem it solves
- Proposed implementation
- Example use case
- Alternative solutions considered

---

## Adding New Signal Types

### Step 1: Define the Signal

Add your signal to `config.py`:

```python
CUSTOM_SIGNALS = {
    # ... existing signals ...

    'your_new_signal': {
        'enabled': True,
        'keywords': [
            'keyword1',
            'keyword2',
            'keyword3'
        ],
        'weight': 20,  # Adjust based on importance
        'query_template': '{company_name} {keyword}'
    }
}
```

### Step 2: Test Keyword Effectiveness

Before committing, verify keywords return useful results:

```python
# test_new_signal.py
from serp_client import SerpClient

client = SerpClient()

# Test each keyword
test_companies = ["Google", "Microsoft", "Stripe"]
keywords = ["your", "test", "keywords"]

for company in test_companies:
    for keyword in keywords:
        query = f"{company} {keyword}"
        results = client.search_for_signals(query, result_count=5)

        print(f"\n{query}:")
        print(f"  Found {len(results)} results")

        if results:
            print(f"  Sample: {results[0]['title']}")
```

### Step 3: Adjust Signal Weight

Guidelines for weight assignment:

| Signal Type | Weight Range | Example |
|-------------|--------------|---------|
| **Critical pain point** | 30-40 | Recent breach, system failure |
| **Strong buying indicator** | 20-30 | Active hiring, migration |
| **Supporting evidence** | 15-20 | Tech mentions, strategy posts |
| **Context signal** | 10-15 | General interest, exploration |

**Weight balancing rule:** Total weight of all enabled signals should equal 100.

### Step 4: Update Conversation Starters

Edit `enrichment_engine.py` → `_generate_conversation_starters()`:

```python
# Add your signal
if signals.get('your_new_signal', {}).get('detected'):
    evidence = signals['your_new_signal'].get('evidence', [])
    if evidence:
        matched_keywords = evidence[0].get('matched_keywords', [])
        if matched_keywords:
            keyword = matched_keywords[0]
            starters.append(
                f"Noticed your mention of {keyword} - [personalized question]?"
            )
```

### Step 5: Test Your Signal

Run tests with your new signal:

```bash
python test_enrichment.py --single
```

Check that:
- Signal is detected when appropriate
- Weight is applied correctly
- Conversation starters are generated
- Total score makes sense

### Example: Adding "Funding Signals"

```python
# In config.py
'funding_signals': {
    'enabled': True,
    'keywords': [
        'Series A funding',
        'Series B funding',
        'raised $',
        'venture capital',
        'funding round'
    ],
    'weight': 25,  # High weight - funding = growth = needs
    'query_template': '{company_name} {keyword}'
}

# In enrichment_engine.py → _generate_conversation_starters()
if signals.get('funding_signals', {}).get('detected'):
    evidence = signals['funding_signals'].get('evidence', [])
    if evidence:
        starters.append(
            "Congratulations on the recent funding - what are your growth priorities?"
        )
```

---

## Creating Industry Configurations

### Step 1: Research the Industry

Understand:
- Common pain points
- Key decision triggers
- Technology stack
- Hiring patterns
- Industry terminology

### Step 2: Design Signal Categories

Choose 4-5 signals that indicate buying intent:

**Example: E-commerce Industry**
1. **Growth Signals** (30%): Traffic surge, SKU expansion
2. **Technical Challenges** (35%): Checkout issues, slow site
3. **Platform Signals** (20%): Shopify/Magento mentions
4. **Scaling Indicators** (15%): Warehouse expansion, fulfillment

### Step 3: Create Config File

Create `example_configs/your_industry_config.py`:

```python
"""
[Industry Name] Signal Configuration

This configuration targets companies in [industry description].
Signals focus on [key indicators].

Use Case: Selling [your product type]
"""

CUSTOM_SIGNALS = {
    'signal_category_1': {
        'enabled': True,
        'keywords': [
            # 5-7 highly relevant keywords
            'keyword1',
            'keyword2',
            'keyword3'
        ],
        'weight': 30,  # Highest weight for strongest signal
        'query_template': '{company_name} {keyword}'
    },

    'signal_category_2': {
        'enabled': True,
        'keywords': [
            # 5-7 keywords
        ],
        'weight': 25,
        'query_template': '{company_name} {keyword}'
    },

    # 2-3 more signals...
}

INTENT_THRESHOLDS = {
    'high': 60,
    'medium': 30,
    'low': 0
}
```

### Step 4: Document Your Config

Add to `example_configs/README.md`:

```markdown
### X. [Industry Name] (`your_industry_config.py`)

**Best for:** Companies selling [product type]

**Signals:**
- Signal 1 (weight%): Description
- Signal 2 (weight%): Description
- Signal 3 (weight%): Description
- Signal 4 (weight%): Description

**Use when targeting:** [Target company characteristics]
```

### Step 5: Test with Real Companies

```python
# test_industry_config.py
from example_configs import your_industry_config
from enrichment_engine import CustomEnrichmentEngine
import config

# Override default config
config.CUSTOM_SIGNALS = your_industry_config.CUSTOM_SIGNALS
config.INTENT_THRESHOLDS = your_industry_config.INTENT_THRESHOLDS

# Test with 5-10 companies in the target industry
test_companies = [
    ("company1.com", "Company 1"),
    ("company2.com", "Company 2"),
    # ... more
]

engine = CustomEnrichmentEngine()
for domain, name in test_companies:
    result = engine.enrich_with_custom_signals(domain, name)
    print(f"{name}: {result['custom_signals']['total_score']}/100")
```

**What to look for:**
- Do the keywords trigger on relevant companies?
- Are scores distributed well (not all high or all low)?
- Are false positives rare?
- Do conversation starters make sense?

---

## Improving Detection Accuracy

### Keyword Selection Best Practices

**✅ Good Keywords:**
- Specific and actionable: "hiring data engineer"
- Industry-standard terms: "SOC 2 compliance"
- Clear buying signals: "migrating from Salesforce"
- Quantifiable: "data quality issues"

**❌ Avoid:**
- Too generic: "data", "software"
- Ambiguous: "good", "fast", "better"
- Negative-only: "bad", "worst" (context matters)
- Brand names without context: "Apple", "Amazon"

### Query Template Optimization

**Test different templates:**

```python
# Generic (baseline)
'{company_name} {keyword}'

# Hiring-focused
'{company_name} hiring {keyword}'

# Problem-focused
'{company_name} challenges with {keyword}'

# Technology-focused
'{company_name} uses {keyword}'
'{company_name} migrating to {keyword}'

# Timeline-focused
'{company_name} {keyword} 2025'
'{company_name} recent {keyword}'
```

**A/B test templates:**

```python
def test_query_templates(company, keyword):
    """Compare different query templates"""
    templates = [
        '{company_name} {keyword}',
        '{company_name} hiring {keyword}',
        '{keyword} at {company_name}'
    ]

    client = SerpClient()
    for template in templates:
        query = template.format(company_name=company, keyword=keyword)
        results = client.search_for_signals(query)
        print(f"\nTemplate: {template}")
        print(f"  Results: {len(results)}")
        if results:
            print(f"  Sample: {results[0]['title'][:80]}...")
```

### Filter Tuning

Adjust result filtering in `serp_client.py`:

```python
# Current filter: 60-600 characters
if 60 <= len(description) <= 600:
    # Process result

# Test different ranges:
# Stricter: 100-400 (fewer but higher quality)
# Looser: 40-800 (more results, potentially noisier)
```

### Evidence Quality

Improve evidence collection in `signal_tracker.py`:

```python
def _analyze_signal(self, results, keywords):
    """Enhanced analysis with quality scoring"""
    evidence = []

    for result in results:
        title = result.get('title', '').lower()
        description = result.get('description', '').lower()

        matched_keywords = []
        match_score = 0

        for keyword in keywords:
            keyword_lower = keyword.lower()

            # Title matches are more valuable
            if keyword_lower in title:
                matched_keywords.append(keyword)
                match_score += 2  # Higher weight for title

            elif keyword_lower in description:
                matched_keywords.append(keyword)
                match_score += 1  # Lower weight for description

        if matched_keywords:
            evidence.append({
                'source': result.get('title', 'Unknown'),
                'url': result.get('url', ''),
                'matched_keywords': list(set(matched_keywords)),
                'snippet': result.get('snippet', ''),
                'match_score': match_score  # Add scoring
            })

    # Sort by quality
    evidence.sort(key=lambda x: x.get('match_score', 0), reverse=True)

    return len(evidence) > 0, evidence
```

---

## Performance Optimization

### Reduce API Calls

**1. Cache frequently enriched domains:**

```python
# Add to serp_client.py
import functools
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=100)
def cached_query(keyword, gl, hl):
    """Cache SERP results for repeated queries"""
    return self.query(keyword, gl, hl)
```

**2. Batch similar queries:**

```python
def batch_signal_detection(self, domains):
    """Process multiple domains efficiently"""
    # Group by similar signals to reuse results
    results = {}
    for domain in domains:
        # Implement batching logic
        pass
```

**3. Parallel processing:**

```python
from concurrent.futures import ThreadPoolExecutor

def enrich_parallel(domains, max_workers=5):
    """Enrich multiple leads in parallel"""
    engine = CustomEnrichmentEngine()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                engine.enrich_with_custom_signals, domain
            ): domain for domain in domains
        }

        results = []
        for future in futures:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error enriching {futures[future]}: {e}")

    return results
```

### Optimize Keyword Matching

Use more efficient string matching:

```python
import re

def fast_keyword_match(text, keywords):
    """Faster keyword matching with regex"""
    # Compile pattern once
    pattern = re.compile(
        '|'.join(re.escape(kw) for kw in keywords),
        re.IGNORECASE
    )

    matches = pattern.findall(text)
    return list(set(matches))
```

---

## Testing Guidelines

### Writing Tests

All new features should include tests:

```python
# test_new_feature.py
def test_new_signal_detection():
    """Test new signal detects correctly"""
    from enrichment_engine import CustomEnrichmentEngine

    engine = CustomEnrichmentEngine()

    # Test with known company
    result = engine.enrich_with_custom_signals(
        "stripe.com",
        "Stripe"
    )

    # Verify signal is present in results
    assert 'your_new_signal' in result['custom_signals']['detected_signals']

    # Test signal fires when expected
    signal_data = result['custom_signals']['detected_signals']['your_new_signal']
    assert signal_data['weight'] == 20  # Expected weight

    print("✓ New signal test passed")
```

### Test Coverage

Ensure tests cover:
- ✅ Signal detection (true positives)
- ✅ Signal absence (true negatives)
- ✅ Edge cases (empty results, malformed data)
- ✅ Error handling (API failures, timeouts)
- ✅ Score calculations
- ✅ Conversation starter generation

### Running Tests

```bash
# Run all tests
python test_enrichment.py

# Run specific test
python test_enrichment.py --single

# Run with verbose logging
python -v test_enrichment.py
```

---

## Code Style

### Python Style Guidelines

Follow PEP 8 with these specifics:

**Naming:**
```python
# Functions and variables: snake_case
def enrich_lead(domain):
    company_name = "Acme"

# Classes: PascalCase
class CustomEnrichmentEngine:
    pass

# Constants: UPPER_CASE
INTENT_THRESHOLDS = {'high': 60}
```

**Docstrings:**
```python
def track_signals(self, domain, company_name=None):
    """
    Track all enabled signals for a company

    This method orchestrates signal detection by querying the SERP API
    and analyzing results for keyword matches.

    Args:
        domain (str): Company domain (e.g., "acme.com")
        company_name (str, optional): Company name. Derived if not provided.

    Returns:
        dict: Signal tracking results with scores and evidence

    Example:
        tracker = SignalTracker()
        result = tracker.track_signals("acme.com", "Acme Corp")
    """
    # Implementation...
```

**Comments:**
```python
# Explain WHY, not WHAT
# Good: Check cache to reduce API costs
# Bad: Get cached result

# Document complex logic
# Use multi-line comments for algorithms
```

**Imports:**
```python
# Standard library first
import os
import json
from datetime import datetime

# Third-party packages
import requests
from dotenv import load_dotenv

# Local modules
from serp_client import SerpClient
import config
```

---

## Submitting Changes

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass: `python test_enrichment.py`
- [ ] New features have tests
- [ ] Documentation updated
- [ ] No hardcoded credentials or secrets
- [ ] Commit messages are descriptive

### Commit Message Format

```
[type]: Brief description (50 chars max)

Longer explanation if needed (72 chars per line).
Include context, motivation, and impact.

- Bullet points for multiple changes
- Reference issues if applicable
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `perf`: Performance improvement
- `test`: Test additions or changes
- `refactor`: Code restructuring without feature changes

**Examples:**
```
feat: Add funding signals detection

Added new signal type to detect recent funding rounds.
Helps identify companies with budget for new purchases.

- Added funding_signals to config
- Updated conversation starter generation
- Added test coverage
```

```
fix: Handle empty SERP results gracefully

Previously crashed when SERP API returned no results.
Now returns score of 0 with Low intent.

Fixes issue where invalid domains caused exceptions.
```

---

## Questions or Need Help?

- **Documentation**: Check the [main README](README.md)
- **Examples**: See `examples/` and `example_configs/`
- **Testing**: Run `python test_enrichment.py --errors`

---

## Recognition

Contributors who make significant improvements will be recognized in the project documentation.

Thank you for helping improve the Custom Lead Enrichment Engine!
