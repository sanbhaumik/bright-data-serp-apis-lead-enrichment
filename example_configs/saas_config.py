"""
SaaS Industry Signal Configuration

This configuration targets SaaS companies launching integrations, APIs, or experiencing platform challenges.
Signals focus on integration announcements, API development, migrations, and product issues.

Use Case: Selling integration platforms, API management, monitoring, or product analytics tools
"""

# Custom buying signals for SaaS industry
CUSTOM_SIGNALS = {
    'integration_announcements': {
        'enabled': True,
        'keywords': [
            'new integration',
            'integration launch',
            'third-party integrations',
            'app marketplace',
            'partner integrations'
        ],
        'weight': 25,  # Shows they're building out ecosystem
        'query_template': '{company_name} {keyword}'
    },

    'api_launches': {
        'enabled': True,
        'keywords': [
            'API launch',
            'public API',
            'REST API',
            'API documentation',
            'developer API'
        ],
        'weight': 25,  # API development indicates need for tooling
        'query_template': '{company_name} {keyword}'
    },

    'platform_migrations': {
        'enabled': True,
        'keywords': [
            'platform migration',
            'switching from',
            'migrating to',
            'replacing software',
            'transition to'
        ],
        'weight': 30,  # Active migration = highest buying intent
        'query_template': '{company_name} {keyword}'
    },

    'product_challenges': {
        'enabled': True,
        'keywords': [
            'product issues',
            'software bugs',
            'downtime',
            'performance problems',
            'user complaints'
        ],
        'weight': 20,  # Pain points create urgency
        'query_template': '{company_name} {keyword}'
    }
}

# Intent scoring thresholds
INTENT_THRESHOLDS = {
    'high': 60,    # Score >= 60: High intent, prioritize outreach
    'medium': 30,  # Score >= 30 and < 60: Medium intent, warm lead
    'low': 0       # Score < 30: Low intent, nurture or disqualify
}
