"""
Test enrichment engine with mock SERP data (no API calls needed)
Run this to test the logic without valid API credentials
"""

from enrichment_engine import CustomEnrichmentEngine
from signal_tracker import SignalTracker
from serp_client import SerpClient


class MockSerpClient:
    """Mock SERP client that returns test data"""

    def query(self, keyword, gl='us', hl='en'):
        """Return mock search results"""
        return {
            "results": [
                {
                    "title": "Snowflake is hiring Data Engineers",
                    "url": "https://careers.snowflake.com/jobs/data-engineer",
                    "description": "Join our growing team as a Data Engineer. We're looking for talented individuals with experience in Snowflake, dbt, and modern data stack technologies. This is an exciting opportunity to work on cutting-edge data infrastructure."
                },
                {
                    "title": "Customer Review: Data Quality Issues at Scale",
                    "url": "https://g2.com/products/snowflake/reviews",
                    "description": "While Snowflake is powerful, we've experienced some data quality issues when scaling to large datasets. Manual data processes are still required for certain workflows, which slows down our reporting capabilities."
                },
                {
                    "title": "Snowflake Blog: Our Data Strategy for 2026",
                    "url": "https://snowflake.com/blog/data-strategy-2026",
                    "description": "We're investing heavily in analytics transformation and modern data stack technologies. Our goal is to become the leading cloud data platform by focusing on data strategy and customer success."
                }
            ]
        }

    def search_for_signals(self, query, result_count=3):
        """Return formatted mock results"""
        data = self.query(query)
        results = []

        for result in data.get('results', [])[:result_count]:
            description = result.get('description', '')

            if 60 <= len(description) <= 600:
                results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'description': description,
                    'snippet': description[:150] + "..." if len(description) > 150 else description
                })

        return results


def test_enrichment():
    """Test enrichment with mock data"""
    print("=" * 70)
    print("TESTING ENRICHMENT ENGINE WITH MOCK DATA")
    print("=" * 70)
    print("\nThis test uses mock SERP responses to verify the enrichment logic")
    print("without requiring valid API credentials.\n")

    # Create mock SERP client
    mock_serp = MockSerpClient()

    # Create signal tracker with mock client
    tracker = SignalTracker(serp_client=mock_serp)

    # Create enrichment engine with mock tracker
    engine = CustomEnrichmentEngine(signal_tracker=tracker)

    # Test enrichment
    print("Testing enrichment for: Snowflake")
    print("-" * 70)

    result = engine.enrich_with_custom_signals(
        domain="snowflake.com",
        company_name="Snowflake"
    )

    # Display results
    print("\n" + "=" * 70)
    print("ENRICHMENT RESULTS")
    print("=" * 70)
    print(f"Company: {result['company_name']}")
    print(f"Domain: {result['domain']}")
    print(f"Enrichment Date: {result['enrichment_date']}")

    signals = result['custom_signals']
    print(f"\nSignal Score: {signals['total_score']}/100")
    print(f"Intent Level: {signals['intent_level']}")

    print("\nDetected Signals:")
    for signal_type, data in signals['detected_signals'].items():
        status = "✓" if data['detected'] else "✗"
        signal_name = signal_type.replace('_', ' ').title()
        print(f"  {status} {signal_name} (Weight: {data['weight']})")
        if data['detected'] and data['evidence']:
            print(f"      Evidence: {len(data['evidence'])} sources")

    print(f"\nRecommendation:")
    print(f"  {signals['recommendation']}")

    print("\nConversation Starters:")
    for i, starter in enumerate(result['conversation_starters'], 1):
        print(f"  {i}. {starter}")

    print("\n" + "=" * 70)
    print("✓ TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nNext step: Get valid Bright Data API credentials to test with real data")
    print("Visit: https://brightdata.com/cp → SERP API")
    print()


if __name__ == "__main__":
    test_enrichment()
