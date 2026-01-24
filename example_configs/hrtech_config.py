"""
HR Technology Industry Signal Configuration

This configuration targets companies experiencing rapid growth or HR challenges.
Signals focus on hiring surges, manual processes, and recruiting technology gaps.

Use Case: Selling ATS, HRIS, onboarding platforms, or recruiting automation tools
"""

# Custom buying signals for HR Tech industry
CUSTOM_SIGNALS = {
    'rapid_growth': {
        'enabled': True,
        'keywords': [
            'hiring surge',
            'rapid hiring',
            'scaling team',
            'hiring spree',
            'expanding workforce'
        ],
        'weight': 30,  # Strong indicator of immediate HR needs
        'query_template': '{company_name} {keyword}'
    },

    'hr_challenges': {
        'enabled': True,
        'keywords': [
            'manual HR processes',
            'HR inefficiencies',
            'employee data management',
            'HR bottlenecks',
            'HR operations challenges'
        ],
        'weight': 35,  # Highest weight - clear pain points
        'query_template': '{company_name} {keyword}'
    },

    'onboarding_pain': {
        'enabled': True,
        'keywords': [
            'onboarding challenges',
            'new hire experience',
            'employee onboarding',
            'remote onboarding',
            'orientation issues'
        ],
        'weight': 20,  # Specific pain point for onboarding solutions
        'query_template': '{company_name} {keyword}'
    },

    'recruiting_tech': {
        'enabled': True,
        'keywords': [
            'ATS issues',
            'recruitment software',
            'applicant tracking',
            'recruiting platform',
            'hiring technology'
        ],
        'weight': 15,  # Shows they're already thinking about tech solutions
        'query_template': '{company_name} {keyword}'
    }
}

# Intent scoring thresholds
INTENT_THRESHOLDS = {
    'high': 60,    # Score >= 60: High intent, prioritize outreach
    'medium': 30,  # Score >= 30 and < 60: Medium intent, warm lead
    'low': 0       # Score < 30: Low intent, nurture or disqualify
}
