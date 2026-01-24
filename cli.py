#!/usr/bin/env python3
"""
Command-Line Interface for Lead Enrichment Engine

This CLI provides easy access to all enrichment features from the command line.
Perfect for automation, batch processing, and quick lead enrichment.

Usage:
    python cli.py enrich --domain acme.com
    python cli.py batch --input leads.csv --output-file enriched.csv
    python cli.py preset --list
    python cli.py monitor --leads-file leads.csv --schedule weekly
"""

import argparse
import sys
import csv
import json
import os
from datetime import datetime
from enrichment_engine import CustomEnrichmentEngine
from presets.load_preset import PresetLoader, apply_preset
import config


class EnrichmentCLI:
    """Command-line interface for lead enrichment"""

    def __init__(self):
        self.engine = CustomEnrichmentEngine()
        self.preset_loader = PresetLoader()

    def enrich_command(self, args):
        """
        Enrich one or more leads

        Examples:
            python cli.py enrich --domain stripe.com
            python cli.py enrich --domain stripe.com --company Stripe
            python cli.py enrich --domain stripe.com --output json
            python cli.py enrich --domain stripe.com --preset fintech
        """
        # Load preset if specified
        if args.preset:
            try:
                apply_preset(args.preset)
                if args.output != 'json':
                    print(f"✓ Using preset: {args.preset}")
            except Exception as e:
                print(f"Error loading preset '{args.preset}': {e}", file=sys.stderr)
                sys.exit(1)

        # Enrich the lead
        try:
            result = self.engine.enrich_with_custom_signals(
                domain=args.domain,
                company_name=args.company
            )

            # Output based on format
            if args.output == 'json':
                print(json.dumps(result, indent=2))
            elif args.output == 'csv':
                self._output_csv_single(result)
            else:  # text (default)
                self._output_text(result)

        except Exception as e:
            print(f"Error enriching {args.domain}: {e}", file=sys.stderr)
            sys.exit(1)

    def batch_command(self, args):
        """
        Batch process leads from CSV file

        CSV file should have columns: domain, company_name (optional)

        Examples:
            python cli.py batch --input leads.csv
            python cli.py batch --input leads.csv --output-file enriched.json --format json
            python cli.py batch --input leads.csv --preset devtools
        """
        # Validate input file
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
            sys.exit(1)

        # Load preset if specified
        if args.preset:
            try:
                apply_preset(args.preset)
                print(f"✓ Using preset: {args.preset}")
            except Exception as e:
                print(f"Error loading preset '{args.preset}': {e}", file=sys.stderr)
                sys.exit(1)

        # Read leads from CSV
        leads = []
        try:
            with open(args.input, 'r') as f:
                reader = csv.DictReader(f)
                leads = list(reader)

            if not leads:
                print(f"Error: No leads found in {args.input}", file=sys.stderr)
                sys.exit(1)

            # Validate required columns
            if 'domain' not in leads[0]:
                print("Error: CSV must have 'domain' column", file=sys.stderr)
                sys.exit(1)

        except Exception as e:
            print(f"Error reading {args.input}: {e}", file=sys.stderr)
            sys.exit(1)

        # Enrich all leads
        print(f"\nEnriching {len(leads)} leads...")
        print("-" * 60)

        enriched_results = []
        for i, lead in enumerate(leads, 1):
            domain = lead['domain']
            company_name = lead.get('company_name', lead.get('name'))

            print(f"[{i}/{len(leads)}] {domain}...", end=' ', flush=True)

            try:
                result = self.engine.enrich_with_custom_signals(
                    domain=domain,
                    company_name=company_name
                )
                enriched_results.append(result)

                # Quick status
                score = result['custom_signals']['total_score']
                intent = result['custom_signals']['intent_level']
                print(f"{score}/100 ({intent})")

            except Exception as e:
                print(f"Error: {e}")
                # Add error result
                enriched_results.append({
                    'domain': domain,
                    'error': str(e)
                })

        # Output results
        print("\n" + "-" * 60)
        print(f"✓ Enrichment complete: {len(enriched_results)} leads")

        # Save to file
        output_file = args.output_file or f"enriched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"

        try:
            if args.format == 'json':
                with open(output_file, 'w') as f:
                    json.dump(enriched_results, f, indent=2)
            else:  # csv
                self._save_batch_csv(enriched_results, output_file)

            print(f"✓ Results saved to: {output_file}")

        except Exception as e:
            print(f"Error saving results: {e}", file=sys.stderr)
            sys.exit(1)

        # Print summary
        self._print_batch_summary(enriched_results)

    def monitor_command(self, args):
        """
        Monitor leads on a schedule

        This command enriches leads and sends alerts for high-intent signals.
        Designed to be run via cron for automated monitoring.

        Examples:
            python cli.py monitor --leads-file leads.csv
            python cli.py monitor --leads-file leads.csv --alert-threshold 70
        """
        # Validate input file
        if not os.path.exists(args.leads_file):
            print(f"Error: Leads file '{args.leads_file}' not found", file=sys.stderr)
            sys.exit(1)

        # Read leads
        try:
            with open(args.leads_file, 'r') as f:
                reader = csv.DictReader(f)
                leads = list(reader)
        except Exception as e:
            print(f"Error reading leads file: {e}", file=sys.stderr)
            sys.exit(1)

        # Enrich and check for alerts
        print(f"\n{'='*60}")
        print(f"MONITORING RUN: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        print(f"Monitoring {len(leads)} leads (threshold: {args.alert_threshold})")
        print(f"Schedule: {args.schedule}")
        print("-" * 60)

        alerts = []
        for lead in leads:
            domain = lead['domain']
            company_name = lead.get('company_name', lead.get('name'))

            try:
                result = self.engine.enrich_with_custom_signals(domain, company_name)
                score = result['custom_signals']['total_score']

                # Check if alert threshold exceeded
                if score >= args.alert_threshold:
                    alerts.append({
                        'domain': domain,
                        'company_name': result['company_name'],
                        'score': score,
                        'intent': result['custom_signals']['intent_level'],
                        'recommendation': result['custom_signals']['recommendation']
                    })
                    print(f"🔔 ALERT: {domain} - Score {score}/100")
                else:
                    print(f"   {domain} - Score {score}/100")

            except Exception as e:
                print(f"   Error monitoring {domain}: {e}")

        # Output alerts
        print("\n" + "=" * 60)
        if alerts:
            print(f"⚠️  {len(alerts)} HIGH-INTENT ALERTS")
            print("=" * 60)

            for alert in alerts:
                print(f"\n{alert['company_name']} ({alert['domain']})")
                print(f"  Score: {alert['score']}/100 ({alert['intent']} intent)")
                print(f"  Action: {alert['recommendation']}")

            # Save alerts to file
            alert_file = f"alerts_{datetime.now().strftime('%Y%m%d')}.json"
            with open(alert_file, 'w') as f:
                json.dump(alerts, f, indent=2)
            print(f"\n✓ Alerts saved to: {alert_file}")

        else:
            print("✓ No alerts - All leads below threshold")
            print("=" * 60)

        print(f"\nNext {args.schedule} check scheduled")

    def preset_command(self, args):
        """
        Manage industry presets

        Examples:
            python cli.py preset --list
            python cli.py preset --show devtools
            python cli.py preset --use hrtech
        """
        if args.list:
            # List all available presets
            presets = self.preset_loader.list_available_presets()

            print("\n" + "=" * 60)
            print("AVAILABLE INDUSTRY PRESETS")
            print("=" * 60)

            for preset_name in presets:
                try:
                    info = self.preset_loader.get_preset_info(preset_name)
                    print(f"\n{preset_name}")
                    print(f"  Industry: {info['industry']}")
                    print(f"  Signals: {info['signal_count']}")
                    print(f"  Example: {', '.join(info['example_companies'][:2])}")
                except Exception as e:
                    print(f"\n{preset_name}: Error - {e}")

            print("\n" + "-" * 60)
            print("Usage: python cli.py preset --use <preset_name>")
            print("       python cli.py enrich --domain example.com --preset <preset_name>")

        elif args.show:
            # Show details of specific preset
            try:
                preset = self.preset_loader.load_preset(args.show)

                print("\n" + "=" * 60)
                print(f"PRESET: {preset['industry']}")
                print("=" * 60)
                print(f"\nDescription:")
                print(f"  {preset['description']}")

                print(f"\nSignals ({len(preset['signals'])}):")
                for signal_name, signal_data in preset['signals'].items():
                    print(f"\n  {signal_name} ({signal_data['weight']}%)")
                    print(f"    Keywords: {', '.join(signal_data['keywords'][:3])}...")
                    print(f"    Template: {signal_data['query_template']}")

                print(f"\nExample Companies:")
                for company in preset['example_companies']:
                    print(f"  • {company}")

                print(f"\nUse Case:")
                print(f"  {preset['typical_use_case']}")

            except Exception as e:
                print(f"Error loading preset '{args.show}': {e}", file=sys.stderr)
                sys.exit(1)

        elif args.use:
            # Apply preset
            try:
                preset = apply_preset(args.use)
                print(f"\n✓ Applied preset: {preset['industry']}")
                print(f"  Signals loaded: {len(preset['signals'])}")
                print("\nYou can now run enrichment commands with this preset:")
                print(f"  python cli.py enrich --domain example.com")
            except Exception as e:
                print(f"Error applying preset '{args.use}': {e}", file=sys.stderr)
                sys.exit(1)

        else:
            print("Error: Use --list, --show <name>, or --use <name>", file=sys.stderr)
            sys.exit(1)

    def _output_text(self, result):
        """Output enrichment result in text format"""
        print("\n" + "=" * 60)
        print("ENRICHMENT RESULTS")
        print("=" * 60)
        print(f"Company: {result['company_name']}")
        print(f"Domain: {result['domain']}")
        print(f"Date: {result['enrichment_date']}")

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

    def _output_csv_single(self, result):
        """Output single enrichment result in CSV format"""
        import sys
        writer = csv.writer(sys.stdout)

        # Header
        writer.writerow([
            'Company', 'Domain', 'Score', 'Intent', 'Hiring Signals',
            'Pain Points', 'Tech Stack', 'Strategic', 'Recommendation'
        ])

        # Data
        signals = result['custom_signals']['detected_signals']
        writer.writerow([
            result['company_name'],
            result['domain'],
            result['custom_signals']['total_score'],
            result['custom_signals']['intent_level'],
            '✓' if signals.get('hiring_signals', {}).get('detected') else '✗',
            '✓' if signals.get('pain_point_signals', {}).get('detected') else '✗',
            '✓' if signals.get('tech_stack_signals', {}).get('detected') else '✗',
            '✓' if signals.get('strategic_signals', {}).get('detected') else '✗',
            result['custom_signals']['recommendation']
        ])

    def _save_batch_csv(self, results, filename):
        """Save batch results to CSV file"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Company', 'Domain', 'Score', 'Intent',
                'Recommendation', 'Enrichment Date'
            ])

            # Data rows
            for result in results:
                if 'error' in result:
                    # Error row
                    writer.writerow([
                        result.get('company_name', ''),
                        result['domain'],
                        'ERROR',
                        '',
                        result['error'],
                        datetime.now().isoformat()
                    ])
                else:
                    writer.writerow([
                        result['company_name'],
                        result['domain'],
                        result['custom_signals']['total_score'],
                        result['custom_signals']['intent_level'],
                        result['custom_signals']['recommendation'],
                        result['enrichment_date']
                    ])

    def _print_batch_summary(self, results):
        """Print summary statistics for batch enrichment"""
        # Count by intent level
        high = sum(1 for r in results if r.get('custom_signals', {}).get('intent_level') == 'High')
        medium = sum(1 for r in results if r.get('custom_signals', {}).get('intent_level') == 'Medium')
        low = sum(1 for r in results if r.get('custom_signals', {}).get('intent_level') == 'Low')
        errors = sum(1 for r in results if 'error' in r)

        # Calculate average score
        scores = [r['custom_signals']['total_score'] for r in results if 'custom_signals' in r]
        avg_score = sum(scores) / len(scores) if scores else 0

        print("\n" + "=" * 60)
        print("BATCH SUMMARY")
        print("=" * 60)
        print(f"Total Leads: {len(results)}")
        print(f"  High Intent: {high}")
        print(f"  Medium Intent: {medium}")
        print(f"  Low Intent: {low}")
        if errors:
            print(f"  Errors: {errors}")
        print(f"\nAverage Score: {avg_score:.1f}/100")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Lead Enrichment Engine CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Enrich a single lead
  python cli.py enrich --domain stripe.com --company Stripe

  # Enrich with specific preset
  python cli.py enrich --domain stripe.com --preset fintech --output json

  # Batch process leads from CSV
  python cli.py batch --input leads.csv --output-file enriched.csv

  # Batch with preset
  python cli.py batch --input leads.csv --preset devtools --format json

  # List available presets
  python cli.py preset --list

  # Show preset details
  python cli.py preset --show security

  # Monitor leads for alerts
  python cli.py monitor --leads-file monitor.csv --alert-threshold 70

For more information, see README.md
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Enrich command
    enrich_parser = subparsers.add_parser('enrich', help='Enrich one lead')
    enrich_parser.add_argument('--domain', required=True, help='Company domain (e.g., stripe.com)')
    enrich_parser.add_argument('--company', help='Company name (optional)')
    enrich_parser.add_argument('--output', choices=['text', 'json', 'csv'], default='text',
                              help='Output format (default: text)')
    enrich_parser.add_argument('--preset', help='Industry preset to use (e.g., devtools, fintech)')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process leads from CSV')
    batch_parser.add_argument('--input', required=True, help='Input CSV file with domains')
    batch_parser.add_argument('--output-file', help='Output filename (auto-generated if not provided)')
    batch_parser.add_argument('--format', choices=['json', 'csv'], default='csv',
                            help='Output format (default: csv)')
    batch_parser.add_argument('--preset', help='Industry preset to use')

    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor leads on schedule')
    monitor_parser.add_argument('--leads-file', required=True, help='CSV file with leads to monitor')
    monitor_parser.add_argument('--schedule', choices=['daily', 'weekly'], default='weekly',
                               help='Monitoring schedule (default: weekly)')
    monitor_parser.add_argument('--alert-threshold', type=int, default=60,
                               help='Signal score threshold for alerts (default: 60)')

    # Preset command
    preset_parser = subparsers.add_parser('preset', help='Manage industry presets')
    preset_group = preset_parser.add_mutually_exclusive_group(required=True)
    preset_group.add_argument('--list', action='store_true', help='List available presets')
    preset_group.add_argument('--show', metavar='NAME', help='Show preset details')
    preset_group.add_argument('--use', metavar='NAME', help='Apply preset')

    # Parse arguments
    args = parser.parse_args()

    # Show help if no command provided
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Validate config before running
    try:
        config.validate_config()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}", file=sys.stderr)
        print("\nPlease ensure your .env file is set up correctly:", file=sys.stderr)
        print("  1. Copy .env.example to .env", file=sys.stderr)
        print("  2. Add your SERP_API_KEY and SERP_ZONE", file=sys.stderr)
        print("  3. Run the command again\n", file=sys.stderr)
        sys.exit(1)

    # Run command
    cli = EnrichmentCLI()

    try:
        if args.command == 'enrich':
            cli.enrich_command(args)
        elif args.command == 'batch':
            cli.batch_command(args)
        elif args.command == 'monitor':
            cli.monitor_command(args)
        elif args.command == 'preset':
            cli.preset_command(args)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
