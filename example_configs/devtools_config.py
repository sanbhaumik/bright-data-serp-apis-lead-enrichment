"""
Developer Tools Industry Signal Configuration

This configuration targets companies building developer tools, APIs, or infrastructure.
Signals focus on technology adoption, performance concerns, and developer hiring.

Use Case: Selling developer infrastructure, monitoring tools, or API platforms
"""

# Custom buying signals for DevTools industry
CUSTOM_SIGNALS = {
    'framework_adoption': {
        'enabled': True,
        'keywords': [
            'Next.js',
            'React',
            'TypeScript',
            'Vue.js',
            'modern frontend'
        ],
        'weight': 25,  # Framework adoption shows they value modern tooling
        'query_template': '{company_name} using {keyword}'
    },

    'api_performance': {
        'enabled': True,
        'keywords': [
            'API scaling',
            'API performance issues',
            'slow API response',
            'rate limiting',
            'API downtime'
        ],
        'weight': 30,  # Strong pain point indicator - high priority
        'query_template': '{company_name} {keyword}'
    },

    'infrastructure_signals': {
        'enabled': True,
        'keywords': [
            'Kubernetes',
            'Docker',
            'microservices',
            'infrastructure migration',
            'cloud native'
        ],
        'weight': 20,  # Shows they're modernizing infrastructure
        'query_template': '{company_name} {keyword}'
    },

    'developer_hiring': {
        'enabled': True,
        'keywords': [
            'DevOps engineer',
            'Backend engineer',
            'Infrastructure engineer',
            'SRE',
            'Platform engineer'
        ],
        'weight': 25,  # Hiring indicates growth and need for tooling
        'query_template': '{company_name} hiring {keyword}'
    }
}

# Intent scoring thresholds
INTENT_THRESHOLDS = {
    'high': 60,    # Score >= 60: High intent, prioritize outreach
    'medium': 30,  # Score >= 30 and < 60: Medium intent, warm lead
    'low': 0       # Score < 30: Low intent, nurture or disqualify
}
