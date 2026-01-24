"""
Signal Tracker for Lead Enrichment Engine
Detects buying signals by analyzing search results for specific keywords
"""

from serp_client import SerpClient
from config import CUSTOM_SIGNALS, INTENT_THRESHOLDS


class SignalTracker:
    """
    Tracks buying signals for companies using SERP data

    This class orchestrates signal detection by:
    1. Querying SERP API for signal-specific keywords
    2. Analyzing results for presence of keywords
    3. Scoring signals based on configured weights
    4. Determining overall intent level
    """

    def __init__(self, serp_client=None):
        """
        Initialize signal tracker with SERP client and configuration

        Args:
            serp_client (SerpClient, optional): SERP API client instance.
                                               Creates new instance if not provided.
        """
        self.serp = serp_client or SerpClient()
        self.signals_config = CUSTOM_SIGNALS
        self.thresholds = INTENT_THRESHOLDS

    def track_signals(self, domain, company_name=None):
        """
        Track all enabled signals for a company

        This method orchestrates the entire signal detection process:
        - Queries SERP API for each signal type
        - Analyzes results for keyword matches
        - Calculates overall intent score
        - Returns comprehensive signal report

        Args:
            domain (str): Company domain (e.g., "acme.com")
            company_name (str, optional): Company name. Derived from domain if not provided.

        Returns:
            dict: Signal tracking report containing:
                - company_name (str): Company name
                - domain (str): Company domain
                - total_score (int): Aggregated signal score (0-100)
                - intent_level (str): High/Medium/Low intent classification
                - signals (dict): Detailed signal detection results
                - recommendation (str): Actionable next steps

        Example:
            tracker = SignalTracker()
            result = tracker.track_signals("acme.com", "Acme Corporation")
        """
        # Derive company name from domain if not provided
        if not company_name:
            # Remove common TLDs and convert to title case
            # e.g., "acme.com" -> "Acme", "bright-data.io" -> "Bright Data"
            company_name = domain.replace('.com', '').replace('.io', '').replace('.net', '')
            company_name = company_name.replace('-', ' ').replace('_', ' ').title()

        print(f"\n→ Tracking custom signals: {company_name}")

        # Initialize tracking variables
        total_score = 0
        detected_signals = {}

        # Iterate through each signal type (hiring, pain_point, tech_stack, strategic)
        for signal_type, signal_config in self.signals_config.items():
            # Skip disabled signals
            if not signal_config.get('enabled', False):
                continue

            print(f"  • Checking {signal_type.replace('_', ' ')}...")

            # Track signal detection results for this signal type
            signal_results = {
                'detected': False,
                'weight': signal_config['weight'],
                'evidence': []
            }

            # Search for each keyword in this signal category
            keywords = signal_config['keywords']
            query_template = signal_config['query_template']

            # We'll check multiple keywords and aggregate evidence
            all_evidence = []
            signal_detected = False

            for keyword in keywords:
                # Build search query using template
                # e.g., "{company_name} hiring {keyword}" -> "Acme hiring data engineer"
                query = query_template.format(
                    company_name=company_name,
                    domain=domain,
                    keyword=keyword
                )

                # Get search results from SERP API
                results = self.serp.search_for_signals(query, result_count=3)

                # Analyze if this keyword appears in results
                detected, evidence = self._analyze_signal(results, [keyword])

                if detected:
                    signal_detected = True
                    all_evidence.extend(evidence)

            # Update signal results if any keyword was detected
            if signal_detected:
                signal_results['detected'] = True
                signal_results['evidence'] = all_evidence
                total_score += signal_config['weight']
                print(f"    ✓ Signal detected (+{signal_config['weight']} points)")

            # Store results for this signal type
            detected_signals[signal_type] = signal_results

        # Calculate overall intent level based on total score
        intent_level = self._calculate_intent(total_score)

        # Print summary
        print(f"\n  ✓ Total signal score: {total_score}/100 ({intent_level} intent)")

        # Get actionable recommendation
        recommendation = self._get_recommendation(intent_level, detected_signals)

        # Return comprehensive signal report
        return {
            'company_name': company_name,
            'domain': domain,
            'total_score': total_score,
            'intent_level': intent_level,
            'signals': detected_signals,
            'recommendation': recommendation
        }

    def _analyze_signal(self, results, keywords):
        """
        Analyze search results to detect signal keywords

        Performs case-insensitive matching of keywords in both
        titles and descriptions of search results.

        Args:
            results (list): List of search result dicts from SERP API
            keywords (list): Keywords to search for in results

        Returns:
            tuple: (signal_detected: bool, evidence: list)
                - signal_detected: True if any keyword found in results
                - evidence: List of dicts with detection details

        Example:
            detected, evidence = self._analyze_signal(results, ["data engineer", "ML"])
        """
        evidence = []
        signal_detected = False

        # Handle empty results gracefully
        if not results:
            return False, []

        # Check each search result
        for result in results:
            title = result.get('title', '').lower()
            description = result.get('description', '').lower()

            # Check if any keyword appears in title or description
            matched_keywords = []
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in title or keyword_lower in description:
                    matched_keywords.append(keyword)
                    signal_detected = True

            # If keywords found, record evidence
            if matched_keywords:
                evidence.append({
                    'source': result.get('title', 'Unknown'),
                    'url': result.get('url', ''),
                    'matched_keywords': matched_keywords,
                    'snippet': result.get('snippet', '')
                })

        return signal_detected, evidence

    def _calculate_intent(self, score):
        """
        Calculate intent level based on total signal score

        Converts numerical score to categorical intent level
        using thresholds from config.

        Args:
            score (int): Total signal score (0-100)

        Returns:
            str: Intent level ("High", "Medium", or "Low")

        Example:
            intent = self._calculate_intent(65)  # Returns "High"
        """
        if score >= self.thresholds['high']:
            return "High"
        elif score >= self.thresholds['medium']:
            return "Medium"
        else:
            return "Low"

    def _get_recommendation(self, intent_level, signals):
        """
        Generate actionable recommendations based on intent level

        Provides specific next steps for sales/marketing teams
        based on detected signals and intent level.

        Args:
            intent_level (str): "High", "Medium", or "Low"
            signals (dict): Detected signals with evidence

        Returns:
            str: Recommendation text with specific actions

        Example:
            rec = self._get_recommendation("High", signals_dict)
        """
        if intent_level == "High":
            # Identify strongest signals to lead with in outreach
            top_signals = [
                signal_type.replace('_', ' ').title()
                for signal_type, data in signals.items()
                if data['detected']
            ]

            if top_signals:
                return (f"🔥 High priority lead! "
                       f"Prioritize immediate outreach. "
                       f"Lead with: {', '.join(top_signals[:2])}. "
                       f"Strong buying signals detected.")
            else:
                return "🔥 High priority lead! Prioritize immediate outreach."

        elif intent_level == "Medium":
            # Standard outreach approach
            detected_count = sum(1 for s in signals.values() if s['detected'])
            return (f"⚡ Medium intent. "
                   f"{detected_count} signal(s) detected. "
                   f"Schedule standard outreach with personalized messaging.")

        else:
            # Nurture or disqualify
            return (f"📊 Low intent. "
                   f"Add to nurture campaign or revisit in 30-60 days. "
                   f"Consider lightweight touchpoints.")


if __name__ == "__main__":
    """
    Test the signal tracker with a sample company

    Run this script directly to test signal tracking:
    python signal_tracker.py
    """
    print("Testing Signal Tracker...")
    print("=" * 60)

    try:
        # Initialize tracker
        tracker = SignalTracker()

        # Test with a sample domain
        # In real usage, you'd pass actual company domains
        test_domain = "snowflake.com"
        test_company = "Snowflake"

        print(f"\nTracking signals for: {test_company} ({test_domain})")

        # Run signal tracking
        result = tracker.track_signals(test_domain, test_company)

        # Display results
        print("\n" + "=" * 60)
        print("SIGNAL TRACKING REPORT")
        print("=" * 60)
        print(f"Company: {result['company_name']}")
        print(f"Domain: {result['domain']}")
        print(f"Total Score: {result['total_score']}/100")
        print(f"Intent Level: {result['intent_level']}")
        print(f"\nRecommendation:")
        print(f"  {result['recommendation']}")

        print("\n" + "-" * 60)
        print("Detected Signals:")
        print("-" * 60)
        for signal_type, data in result['signals'].items():
            status = "✓ Detected" if data['detected'] else "✗ Not detected"
            print(f"  {signal_type.replace('_', ' ').title()}: {status}")
            if data['detected'] and data['evidence']:
                print(f"    Evidence count: {len(data['evidence'])} sources")

    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        print("  Please ensure your .env file is configured correctly")
