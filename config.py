"""
Configuration file for Lead Enrichment Engine
Manages API credentials, signal definitions, and scoring thresholds
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bright Data SERP API Configuration
SERP_API_KEY = os.getenv('SERP_API_KEY')
SERP_ZONE = os.getenv('SERP_ZONE')
DEFAULT_COUNTRY = os.getenv('DEFAULT_COUNTRY', 'us')
DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')

# Custom buying signals configuration
# Each signal tracks specific indicators that suggest a company is ready to buy
CUSTOM_SIGNALS = {
    'hiring_signals': {
        'enabled': True,
        'keywords': [
            'data engineer',
            'machine learning engineer',
            'Snowflake',
            'dbt'
        ],
        'weight': 25,  # Importance of this signal in overall scoring (out of 100)
        'query_template': '{company_name} hiring {keyword}'
    },

    'pain_point_signals': {
        'enabled': True,
        'keywords': [
            'manual data processes',
            'data quality issues',
            'slow reporting'
        ],
        'weight': 35,  # Highest weight - strongest indicator of need
        'query_template': '{company_name} {keyword}'
    },

    'tech_stack_signals': {
        'enabled': True,
        'keywords': [
            'Snowflake',
            'Databricks',
            'modern data stack'
        ],
        'weight': 25,  # Indicates they value modern technology
        'query_template': '{company_name} uses {keyword}'
    },

    'strategic_signals': {
        'enabled': True,
        'keywords': [
            'data strategy',
            'analytics transformation'
        ],
        'weight': 15,  # Shows high-level commitment to data initiatives
        'query_template': '{company_name} {keyword}'
    }
}

# Intent scoring thresholds
# Determines how we classify leads based on their total signal score
INTENT_THRESHOLDS = {
    'high': 60,    # Score >= 60: High intent, prioritize outreach
    'medium': 30,  # Score >= 30 and < 60: Medium intent, warm lead
    'low': 0       # Score < 30: Low intent, nurture or disqualify
}

# Validate required configuration
def validate_config():
    """
    Validates that all required configuration variables are set
    Raises ValueError if any required config is missing
    """
    if not SERP_API_KEY:
        raise ValueError("SERP_API_KEY is required. Please set it in your .env file.")
    if not SERP_ZONE:
        raise ValueError("SERP_ZONE is required. Please set it in your .env file.")

    # Validate signal weights sum to 100 (optional check for consistency)
    total_weight = sum(signal['weight'] for signal in CUSTOM_SIGNALS.values() if signal['enabled'])
    if total_weight != 100:
        print(f"Warning: Signal weights sum to {total_weight}, not 100. Adjust weights for accurate scoring.")

if __name__ == '__main__':
    # Quick config validation test
    try:
        validate_config()
        print("✓ Configuration validated successfully")
        print(f"✓ SERP API configured for zone: {SERP_ZONE}")
        print(f"✓ Default search params: country={DEFAULT_COUNTRY}, language={DEFAULT_LANGUAGE}")
        print(f"✓ Active signals: {len([s for s in CUSTOM_SIGNALS.values() if s['enabled']])}")
    except ValueError as e:
        print(f"✗ Configuration error: {e}")
