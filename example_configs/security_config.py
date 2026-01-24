"""
Cybersecurity Industry Signal Configuration

This configuration targets companies with security incidents, compliance needs, or security gaps.
Signals focus on breaches, compliance requirements, and security hiring.

Use Case: Selling security tools, compliance platforms, penetration testing, or security services
"""

# Custom buying signals for Cybersecurity industry
CUSTOM_SIGNALS = {
    'security_incidents': {
        'enabled': True,
        'keywords': [
            'security breach',
            'data breach',
            'security vulnerability',
            'cyberattack',
            'security incident'
        ],
        'weight': 35,  # Highest priority - immediate security need
        'query_template': '{company_name} {keyword}'
    },

    'compliance_needs': {
        'enabled': True,
        'keywords': [
            'SOC 2',
            'ISO 27001',
            'GDPR compliance',
            'HIPAA compliance',
            'compliance audit'
        ],
        'weight': 30,  # Strong signal - regulatory pressure drives decisions
        'query_template': '{company_name} {keyword}'
    },

    'vulnerability_mentions': {
        'enabled': True,
        'keywords': [
            'penetration testing',
            'vulnerability assessment',
            'security audit',
            'security review',
            'risk assessment'
        ],
        'weight': 20,  # Shows proactive security approach
        'query_template': '{company_name} {keyword}'
    },

    'security_hiring': {
        'enabled': True,
        'keywords': [
            'Security Engineer',
            'CISO',
            'Security Analyst',
            'Cybersecurity',
            'InfoSec'
        ],
        'weight': 15,  # Building security team indicates investment
        'query_template': '{company_name} hiring {keyword}'
    }
}

# Intent scoring thresholds
INTENT_THRESHOLDS = {
    'high': 60,    # Score >= 60: High intent, prioritize outreach
    'medium': 30,  # Score >= 30 and < 60: Medium intent, warm lead
    'low': 0       # Score < 30: Low intent, nurture or disqualify
}
