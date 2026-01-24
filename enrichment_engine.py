"""
Custom Enrichment Engine for Lead Generation
Combines signal tracking with profile enrichment and conversation starters
"""

from datetime import datetime
from signal_tracker import SignalTracker


class CustomEnrichmentEngine:
    """
    Main enrichment engine that orchestrates lead enrichment

    This engine:
    1. Tracks buying signals using SERP data
    2. Scores and classifies leads by intent
    3. Generates personalized conversation starters
    4. Combines custom signals with existing lead data
    """

    def __init__(self, signal_tracker=None):
        """
        Initialize enrichment engine with signal tracker

        Args:
            signal_tracker (SignalTracker, optional): Signal tracking instance.
                                                     Creates new instance if not provided.
        """
        self.tracker = signal_tracker or SignalTracker()

    def enrich_with_custom_signals(self, domain, company_name=None, existing_data=None):
        """
        Enrich lead profile with custom buying signals

        This is the main entry point for enrichment. It:
        - Tracks buying signals across multiple dimensions
        - Calculates intent score and classification
        - Generates personalized conversation starters
        - Combines everything into a comprehensive profile

        Args:
            domain (str): Company domain (e.g., "acme.com")
            company_name (str, optional): Company name. Derived from domain if not provided.
            existing_data (dict, optional): Existing lead data to preserve (e.g., from CRM)

        Returns:
            dict: Enriched profile containing:
                - enrichment_date (str): ISO timestamp of enrichment
                - domain (str): Company domain
                - company_name (str): Company name
                - custom_signals (dict): Signal tracking results
                  - total_score (int): Aggregated signal score
                  - intent_level (str): High/Medium/Low classification
                  - detected_signals (dict): Detailed signal data
                  - recommendation (str): Actionable next steps
                - conversation_starters (list): Personalized opening messages
                - standard_data (dict): Original lead data passed in

        Example:
            engine = CustomEnrichmentEngine()
            profile = engine.enrich_with_custom_signals(
                "acme.com",
                company_name="Acme Corp",
                existing_data={"industry": "SaaS", "employees": 500}
            )
        """
        # Get current timestamp for enrichment tracking
        enrichment_date = datetime.utcnow().isoformat()

        # Run signal tracking to detect buying signals
        signal_results = self.tracker.track_signals(domain, company_name)

        # Generate personalized conversation starters based on detected signals
        conversation_starters = self._generate_conversation_starters(signal_results)

        # Build enriched profile
        enriched_profile = {
            'enrichment_date': enrichment_date,
            'domain': signal_results['domain'],
            'company_name': signal_results['company_name'],
            'custom_signals': {
                'total_score': signal_results['total_score'],
                'intent_level': signal_results['intent_level'],
                'detected_signals': signal_results['signals'],
                'recommendation': signal_results['recommendation']
            },
            'conversation_starters': conversation_starters,
            'standard_data': existing_data or {}
        }

        return enriched_profile

    def _generate_conversation_starters(self, signal_results):
        """
        Generate personalized conversation starters based on detected signals

        Creates natural, relevant opening messages that reference specific
        signals detected during tracking. These can be used in cold emails,
        LinkedIn messages, or sales calls.

        Args:
            signal_results (dict): Results from track_signals() containing
                                  detected signals and evidence

        Returns:
            list: Up to 3 personalized conversation starters

        Example:
            starters = self._generate_conversation_starters(signal_results)
            # ["Saw you're hiring for Data Engineer roles - are you expanding your team?"]
        """
        starters = []
        signals = signal_results.get('signals', {})

        # Generate starter based on hiring signals
        if signals.get('hiring_signals', {}).get('detected'):
            evidence = signals['hiring_signals'].get('evidence', [])
            if evidence:
                # Extract keywords from first piece of evidence
                matched_keywords = evidence[0].get('matched_keywords', [])
                if matched_keywords:
                    keyword = matched_keywords[0]
                    starters.append(
                        f"Saw you're hiring for roles involving {keyword} - are you expanding your team?"
                    )

        # Generate starter based on tech stack signals
        if signals.get('tech_stack_signals', {}).get('detected'):
            evidence = signals['tech_stack_signals'].get('evidence', [])
            if evidence:
                matched_keywords = evidence[0].get('matched_keywords', [])
                if matched_keywords:
                    keyword = matched_keywords[0]
                    starters.append(
                        f"Noticed you're working with {keyword} - how's that migration going?"
                    )

        # Generate starter based on pain point signals
        if signals.get('pain_point_signals', {}).get('detected'):
            evidence = signals['pain_point_signals'].get('evidence', [])
            if evidence:
                matched_keywords = evidence[0].get('matched_keywords', [])
                if matched_keywords:
                    keyword = matched_keywords[0]
                    starters.append(
                        f"Read some feedback about {keyword} - is this still a challenge?"
                    )

        # Generate starter based on strategic signals
        if signals.get('strategic_signals', {}).get('detected'):
            evidence = signals['strategic_signals'].get('evidence', [])
            if evidence:
                source = evidence[0].get('source', 'your recent update')
                starters.append(
                    f"Just saw your post about {source} - how does this fit into your roadmap?"
                )

        # Handle case where no signals were detected
        if not starters:
            # Provide generic but professional fallback starters
            company_name = signal_results.get('company_name', 'your company')
            starters = [
                f"Interested in learning more about {company_name}'s data strategy",
                "Would love to connect and discuss potential collaboration opportunities",
                f"Noticed {company_name}'s growth - how are you handling data at scale?"
            ]

        # Return up to 3 starters
        return starters[:3]


if __name__ == "__main__":
    """
    Test the enrichment engine with a sample company

    Run this script directly to test the full enrichment pipeline:
    python enrichment_engine.py
    """
    print("Testing Custom Enrichment Engine...")
    print("=" * 60)

    try:
        # Initialize engine
        engine = CustomEnrichmentEngine()

        # Test with sample data
        test_domain = "snowflake.com"
        test_company = "Snowflake"
        test_existing_data = {
            "industry": "Cloud Data Warehouse",
            "employees": 5000,
            "revenue": "$1B+"
        }

        print(f"\nEnriching profile for: {test_company} ({test_domain})")
        print("-" * 60)

        # Run enrichment
        profile = engine.enrich_with_custom_signals(
            domain=test_domain,
            company_name=test_company,
            existing_data=test_existing_data
        )

        # Display enriched profile
        print("\n" + "=" * 60)
        print("ENRICHED LEAD PROFILE")
        print("=" * 60)
        print(f"Company: {profile['company_name']}")
        print(f"Domain: {profile['domain']}")
        print(f"Enrichment Date: {profile['enrichment_date']}")

        print("\n" + "-" * 60)
        print("CUSTOM SIGNALS")
        print("-" * 60)
        signals = profile['custom_signals']
        print(f"Total Score: {signals['total_score']}/100")
        print(f"Intent Level: {signals['intent_level']}")
        print(f"\nRecommendation:")
        print(f"  {signals['recommendation']}")

        print("\n" + "-" * 60)
        print("DETECTED SIGNALS")
        print("-" * 60)
        for signal_type, data in signals['detected_signals'].items():
            status = "✓" if data['detected'] else "✗"
            signal_name = signal_type.replace('_', ' ').title()
            print(f"  {status} {signal_name} (Weight: {data['weight']})")

        print("\n" + "-" * 60)
        print("CONVERSATION STARTERS")
        print("-" * 60)
        for i, starter in enumerate(profile['conversation_starters'], 1):
            print(f"  {i}. {starter}")

        print("\n" + "-" * 60)
        print("STANDARD DATA")
        print("-" * 60)
        for key, value in profile['standard_data'].items():
            print(f"  {key}: {value}")

        print("\n" + "=" * 60)
        print("✓ Enrichment completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error during enrichment: {e}")
        print("  Please ensure your .env file is configured correctly")
