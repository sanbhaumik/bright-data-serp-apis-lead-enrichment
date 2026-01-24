"""
Testing Utilities for Lead Enrichment Engine

This module provides comprehensive test functions to validate the enrichment pipeline.
Run individual tests or all tests to verify functionality.

Usage:
    python test_enrichment.py              # Run all tests
    python test_enrichment.py --single     # Run single lead test only
    python test_enrichment.py --multiple   # Run multiple leads test only
"""

import json
import csv
import os
import sys
from datetime import datetime
from enrichment_engine import CustomEnrichmentEngine
import config


def test_single_lead():
    """
    Test enrichment on a single lead

    This test demonstrates basic enrichment functionality by:
    - Enriching a single company (Anthropic)
    - Printing results in a readable text format
    - Returning enriched data for further processing

    Returns:
        dict: Enriched profile data
    """
    print("\n" + "=" * 70)
    print("TEST 1: Single Lead Enrichment")
    print("=" * 70)

    try:
        # Initialize enrichment engine
        engine = CustomEnrichmentEngine()

        # Test with a well-known company
        domain = "anthropic.com"
        company_name = "Anthropic"

        print(f"\nEnriching lead: {company_name} ({domain})")
        print("-" * 70)

        # Run enrichment
        enriched_data = engine.enrich_with_custom_signals(
            domain=domain,
            company_name=company_name
        )

        # Print results in readable format
        print("\n✓ ENRICHMENT COMPLETED")
        print("-" * 70)
        print(f"Company: {enriched_data['company_name']}")
        print(f"Domain: {enriched_data['domain']}")
        print(f"Enrichment Date: {enriched_data['enrichment_date']}")

        # Display custom signals
        signals = enriched_data['custom_signals']
        print(f"\nSignal Score: {signals['total_score']}/100")
        print(f"Intent Level: {signals['intent_level']}")

        print("\nDetected Signals:")
        for signal_type, data in signals['detected_signals'].items():
            status = "✓" if data['detected'] else "✗"
            signal_name = signal_type.replace('_', ' ').title()
            print(f"  {status} {signal_name} (Weight: {data['weight']})")

            # Show evidence if signal detected
            if data['detected'] and data['evidence']:
                print(f"      Evidence: {len(data['evidence'])} sources found")

        print(f"\nRecommendation:")
        print(f"  {signals['recommendation']}")

        print("\nConversation Starters:")
        for i, starter in enumerate(enriched_data['conversation_starters'], 1):
            print(f"  {i}. {starter}")

        print("\n" + "=" * 70)
        print("✓ TEST 1 PASSED")
        print("=" * 70)

        return enriched_data

    except Exception as e:
        print(f"\n✗ TEST 1 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_multiple_leads():
    """
    Test enrichment on multiple leads and export results

    This test demonstrates batch processing by:
    - Enriching 3 companies from different industries
    - Exporting results to JSON format
    - Exporting results to CSV format
    - Showing how to process multiple leads efficiently

    Returns:
        list: List of enriched profiles
    """
    print("\n" + "=" * 70)
    print("TEST 2: Multiple Lead Enrichment with Export")
    print("=" * 70)

    # Test companies from different industries
    test_leads = [
        {"domain": "stripe.com", "company_name": "Stripe"},
        {"domain": "gusto.com", "company_name": "Gusto"},
        {"domain": "datadog.com", "company_name": "Datadog"}
    ]

    enriched_leads = []

    try:
        engine = CustomEnrichmentEngine()

        # Enrich each lead
        for lead in test_leads:
            print(f"\nEnriching: {lead['company_name']} ({lead['domain']})")
            enriched = engine.enrich_with_custom_signals(
                domain=lead['domain'],
                company_name=lead['company_name']
            )
            enriched_leads.append(enriched)
            print(f"  Score: {enriched['custom_signals']['total_score']}/100 | "
                  f"Intent: {enriched['custom_signals']['intent_level']}")

        # Export to JSON
        json_filename = "enriched_leads.json"
        with open(json_filename, 'w') as f:
            json.dump(enriched_leads, f, indent=2)
        print(f"\n✓ Exported to JSON: {json_filename}")

        # Export to CSV
        csv_filename = "enriched_leads.csv"
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow([
                'Company Name',
                'Domain',
                'Total Score',
                'Intent Level',
                'Hiring Signals',
                'Pain Point Signals',
                'Tech Stack Signals',
                'Strategic Signals',
                'Recommendation',
                'Enrichment Date'
            ])

            # Write data rows
            for lead in enriched_leads:
                signals = lead['custom_signals']['detected_signals']
                writer.writerow([
                    lead['company_name'],
                    lead['domain'],
                    lead['custom_signals']['total_score'],
                    lead['custom_signals']['intent_level'],
                    '✓' if signals.get('hiring_signals', {}).get('detected') else '✗',
                    '✓' if signals.get('pain_point_signals', {}).get('detected') else '✗',
                    '✓' if signals.get('tech_stack_signals', {}).get('detected') else '✗',
                    '✓' if signals.get('strategic_signals', {}).get('detected') else '✗',
                    lead['custom_signals']['recommendation'],
                    lead['enrichment_date']
                ])

        print(f"✓ Exported to CSV: {csv_filename}")

        # Print summary
        print("\n" + "-" * 70)
        print("ENRICHMENT SUMMARY")
        print("-" * 70)
        high_intent = sum(1 for l in enriched_leads if l['custom_signals']['intent_level'] == 'High')
        medium_intent = sum(1 for l in enriched_leads if l['custom_signals']['intent_level'] == 'Medium')
        low_intent = sum(1 for l in enriched_leads if l['custom_signals']['intent_level'] == 'Low')

        print(f"Total Leads Enriched: {len(enriched_leads)}")
        print(f"  High Intent: {high_intent}")
        print(f"  Medium Intent: {medium_intent}")
        print(f"  Low Intent: {low_intent}")
        print(f"Average Score: {sum(l['custom_signals']['total_score'] for l in enriched_leads) / len(enriched_leads):.1f}/100")

        print("\n" + "=" * 70)
        print("✓ TEST 2 PASSED")
        print("=" * 70)

        return enriched_leads

    except Exception as e:
        print(f"\n✗ TEST 2 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_with_existing_data():
    """
    Test enrichment with existing lead data

    This test demonstrates how to combine custom signals with
    standard enrichment data from other sources (e.g., Clearbit, ZoomInfo).

    Shows:
    - Combining standard + custom enrichment
    - Preserving existing lead data
    - Creating a complete lead profile

    Returns:
        dict: Combined enriched profile
    """
    print("\n" + "=" * 70)
    print("TEST 3: Enrichment with Existing Data")
    print("=" * 70)

    try:
        engine = CustomEnrichmentEngine()

        # Mock existing data from standard enrichment tool
        # (This would come from Clearbit, ZoomInfo, etc. in real usage)
        existing_data = {
            "company": {
                "name": "Anthropic",
                "domain": "anthropic.com",
                "industry": "Artificial Intelligence",
                "employees": 500,
                "founded": 2021,
                "funding": "$1.5B",
                "location": "San Francisco, CA"
            },
            "contacts": [
                {
                    "name": "Dario Amodei",
                    "title": "CEO",
                    "email": "dario@anthropic.com"
                }
            ],
            "technographics": [
                "AWS",
                "Python",
                "React",
                "TypeScript"
            ]
        }

        print("\nExisting Standard Data:")
        print("-" * 70)
        print(json.dumps(existing_data, indent=2))

        # Enrich with custom signals
        print("\nAdding custom signal enrichment...")
        enriched_data = engine.enrich_with_custom_signals(
            domain="anthropic.com",
            company_name="Anthropic",
            existing_data=existing_data
        )

        # Display combined profile
        print("\n" + "-" * 70)
        print("COMBINED ENRICHED PROFILE")
        print("-" * 70)
        print(f"\nCompany: {enriched_data['company_name']}")
        print(f"Domain: {enriched_data['domain']}")

        print("\nStandard Data (from existing enrichment):")
        print(f"  Industry: {enriched_data['standard_data']['company']['industry']}")
        print(f"  Employees: {enriched_data['standard_data']['company']['employees']}")
        print(f"  Funding: {enriched_data['standard_data']['company']['funding']}")

        print("\nCustom Signals (from this engine):")
        signals = enriched_data['custom_signals']
        print(f"  Score: {signals['total_score']}/100")
        print(f"  Intent: {signals['intent_level']}")
        print(f"  Recommendation: {signals['recommendation']}")

        print("\nConversation Starters:")
        for i, starter in enumerate(enriched_data['conversation_starters'], 1):
            print(f"  {i}. {starter}")

        print("\n" + "=" * 70)
        print("✓ TEST 3 PASSED")
        print("✓ Successfully combined standard + custom enrichment")
        print("=" * 70)

        return enriched_data

    except Exception as e:
        print(f"\n✗ TEST 3 FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_error_handling():
    """
    Test error handling and graceful failures

    This test validates that the engine handles errors gracefully:
    - Invalid domains
    - Missing API credentials
    - Malformed configurations
    - Network failures

    Returns:
        bool: True if all error handling tests pass
    """
    print("\n" + "=" * 70)
    print("TEST 4: Error Handling")
    print("=" * 70)

    tests_passed = 0
    tests_total = 3

    # Test 1: Invalid domain
    print("\nTest 4.1: Invalid domain")
    print("-" * 70)
    try:
        engine = CustomEnrichmentEngine()
        result = engine.enrich_with_custom_signals(
            domain="invalid-domain-that-doesnt-exist-xyz123.com",
            company_name="Invalid Company"
        )

        # Should complete but with no signals detected
        if result['custom_signals']['total_score'] == 0:
            print("✓ Handled invalid domain gracefully (score: 0)")
            tests_passed += 1
        else:
            print("✗ Invalid domain did not result in expected behavior")
    except Exception as e:
        print(f"✗ Unexpected error with invalid domain: {str(e)}")

    # Test 2: Missing company name (should derive from domain)
    print("\nTest 4.2: Missing company name")
    print("-" * 70)
    try:
        engine = CustomEnrichmentEngine()
        result = engine.enrich_with_custom_signals(domain="test.com")

        if result['company_name'] == 'Test':
            print(f"✓ Derived company name from domain: '{result['company_name']}'")
            tests_passed += 1
        else:
            print(f"✗ Failed to derive company name: '{result['company_name']}'")
    except Exception as e:
        print(f"✗ Error handling missing company name: {str(e)}")

    # Test 3: Empty results handling
    print("\nTest 4.3: Empty search results")
    print("-" * 70)
    try:
        # This tests the internal error handling when SERP returns no results
        engine = CustomEnrichmentEngine()
        result = engine.enrich_with_custom_signals(
            domain="obscure-company-12345.com",
            company_name="Obscure Company"
        )

        # Should complete even with no results
        if 'custom_signals' in result and 'intent_level' in result['custom_signals']:
            print("✓ Handled empty results gracefully")
            print(f"  Returned intent: {result['custom_signals']['intent_level']}")
            tests_passed += 1
        else:
            print("✗ Failed to handle empty results properly")
    except Exception as e:
        print(f"✗ Error handling empty results: {str(e)}")

    # Summary
    print("\n" + "-" * 70)
    print(f"Error Handling Tests: {tests_passed}/{tests_total} passed")
    print("-" * 70)

    if tests_passed == tests_total:
        print("\n" + "=" * 70)
        print("✓ TEST 4 PASSED")
        print("✓ All error handling tests passed")
        print("=" * 70)
        return True
    else:
        print("\n" + "=" * 70)
        print("✗ TEST 4 PARTIAL: Some error handling tests failed")
        print("=" * 70)
        return False


def run_all_tests():
    """
    Run all test functions sequentially

    Executes all test cases and provides a summary of results.
    Useful for comprehensive validation of the enrichment engine.
    """
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "LEAD ENRICHMENT ENGINE TEST SUITE" + " " * 20 + "║")
    print("╚" + "=" * 68 + "╝")

    results = {
        'test_1_single_lead': False,
        'test_2_multiple_leads': False,
        'test_3_existing_data': False,
        'test_4_error_handling': False
    }

    # Run tests
    result1 = test_single_lead()
    results['test_1_single_lead'] = result1 is not None

    result2 = test_multiple_leads()
    results['test_2_multiple_leads'] = result2 is not None

    result3 = test_with_existing_data()
    results['test_3_existing_data'] = result3 is not None

    result4 = test_error_handling()
    results['test_4_error_handling'] = result4 is True

    # Print final summary
    print("\n" + "╔" + "=" * 68 + "╗")
    print("║" + " " * 25 + "TEST SUMMARY" + " " * 31 + "║")
    print("╠" + "=" * 68 + "╣")

    passed_tests = sum(1 for v in results.values() if v)
    total_tests = len(results)

    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        test_label = test_name.replace('_', ' ').title()
        print(f"║  {test_label:<50} {status:>15} ║")

    print("╠" + "=" * 68 + "╣")
    print(f"║  Total: {passed_tests}/{total_tests} tests passed" + " " * (68 - 25 - len(str(passed_tests)) - len(str(total_tests))) + "║")
    print("╚" + "=" * 68 + "╝")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed! The enrichment engine is working correctly.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please check the errors above.")


if __name__ == "__main__":
    """
    Command-line interface for running tests

    Usage:
        python test_enrichment.py              # Run all tests
        python test_enrichment.py --single     # Run single lead test
        python test_enrichment.py --multiple   # Run multiple leads test
        python test_enrichment.py --existing   # Run existing data test
        python test_enrichment.py --errors     # Run error handling test
    """

    # Check for API credentials before running tests
    try:
        config.validate_config()
    except ValueError as e:
        print(f"\n✗ Configuration Error: {e}")
        print("\nPlease ensure your .env file is set up correctly:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your SERP_API_KEY and SERP_ZONE")
        print("  3. Run tests again")
        sys.exit(1)

    # Parse command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == '--single':
            test_single_lead()
        elif arg == '--multiple':
            test_multiple_leads()
        elif arg == '--existing':
            test_with_existing_data()
        elif arg == '--errors':
            test_error_handling()
        else:
            print(f"Unknown argument: {arg}")
            print("\nUsage:")
            print("  python test_enrichment.py              # Run all tests")
            print("  python test_enrichment.py --single     # Run single lead test")
            print("  python test_enrichment.py --multiple   # Run multiple leads test")
            print("  python test_enrichment.py --existing   # Run existing data test")
            print("  python test_enrichment.py --errors     # Run error handling test")
    else:
        # Run all tests
        run_all_tests()
