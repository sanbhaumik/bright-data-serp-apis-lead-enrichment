#!/bin/bash
#
# Lead Enrichment Monitoring Scheduler
#
# This script helps you set up automated monitoring of leads using cron.
# It can create daily or weekly monitoring jobs that check for high-intent signals.
#
# Usage:
#   ./schedule_monitoring.sh setup --leads-file leads.csv --schedule weekly
#   ./schedule_monitoring.sh remove
#   ./schedule_monitoring.sh status
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_error() { echo -e "${RED}✗ $1${NC}" >&2; }
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }

print_header() {
    echo ""
    echo -e "${BLUE}$1${NC}"
    echo "$(printf '=%.0s' {1..60})"
}

show_help() {
    cat << EOF
Lead Enrichment Monitoring Scheduler

USAGE:
    ./schedule_monitoring.sh COMMAND [OPTIONS]

COMMANDS:
    setup       Set up monitoring cron job
    remove      Remove monitoring cron job
    status      Check monitoring status
    test        Test monitoring without scheduling

SETUP OPTIONS:
    --leads-file FILE       CSV file with leads to monitor (required)
    --schedule FREQ         Frequency: daily or weekly (default: weekly)
    --alert-threshold N     Alert threshold score (default: 60)
    --time HHMM            Time to run (default: 0900 for 9:00 AM)

EXAMPLES:
    # Set up weekly monitoring at 9 AM
    ./schedule_monitoring.sh setup --leads-file leads.csv

    # Set up daily monitoring with custom threshold
    ./schedule_monitoring.sh setup --leads-file leads.csv --schedule daily --alert-threshold 70

    # Check current monitoring status
    ./schedule_monitoring.sh status

    # Remove monitoring
    ./schedule_monitoring.sh remove

    # Test monitoring without scheduling
    ./schedule_monitoring.sh test --leads-file leads.csv

EOF
}

setup_monitoring() {
    local LEADS_FILE=""
    local SCHEDULE="weekly"
    local THRESHOLD=60
    local TIME="0900"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --leads-file)
                LEADS_FILE="$2"
                shift 2
                ;;
            --schedule)
                SCHEDULE="$2"
                shift 2
                ;;
            --alert-threshold)
                THRESHOLD="$2"
                shift 2
                ;;
            --time)
                TIME="$2"
                shift 2
                ;;
            *)
                print_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done

    # Validate leads file
    if [ -z "$LEADS_FILE" ]; then
        print_error "Missing required option: --leads-file"
        echo "Usage: ./schedule_monitoring.sh setup --leads-file FILE"
        exit 1
    fi

    if [ ! -f "$LEADS_FILE" ]; then
        print_error "Leads file not found: $LEADS_FILE"
        exit 1
    fi

    # Validate schedule
    if [[ "$SCHEDULE" != "daily" && "$SCHEDULE" != "weekly" ]]; then
        print_error "Schedule must be 'daily' or 'weekly'"
        exit 1
    fi

    # Convert time to cron format
    HOUR="${TIME:0:2}"
    MINUTE="${TIME:2:2}"

    print_header "SETTING UP MONITORING"

    # Create absolute paths
    ABS_LEADS_FILE="$(cd "$(dirname "$LEADS_FILE")" && pwd)/$(basename "$LEADS_FILE")"
    ABS_SCRIPT_DIR="$SCRIPT_DIR"

    # Build cron command
    CRON_CMD="cd $ABS_SCRIPT_DIR && ./run_enrichment.sh monitor --leads-file $ABS_LEADS_FILE --schedule $SCHEDULE --alert-threshold $THRESHOLD >> $ABS_SCRIPT_DIR/monitoring.log 2>&1"

    # Build cron schedule
    if [ "$SCHEDULE" = "daily" ]; then
        CRON_SCHEDULE="$MINUTE $HOUR * * *"
        DESCRIPTION="Daily at ${HOUR}:${MINUTE}"
    else
        # Weekly on Monday
        CRON_SCHEDULE="$MINUTE $HOUR * * 1"
        DESCRIPTION="Weekly on Monday at ${HOUR}:${MINUTE}"
    fi

    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "lead_enrichment_monitor"; then
        print_warning "Monitoring cron job already exists. Removing old job..."
        crontab -l 2>/dev/null | grep -v "lead_enrichment_monitor" | crontab -
    fi

    # Add new cron job
    (crontab -l 2>/dev/null; echo "# Lead Enrichment Monitoring - lead_enrichment_monitor"; echo "$CRON_SCHEDULE $CRON_CMD") | crontab -

    print_success "Monitoring set up successfully!"
    echo ""
    echo "Configuration:"
    echo "  Leads File: $ABS_LEADS_FILE"
    echo "  Schedule: $DESCRIPTION"
    echo "  Alert Threshold: $THRESHOLD"
    echo "  Log File: $ABS_SCRIPT_DIR/monitoring.log"
    echo ""
    print_info "To view logs: tail -f $ABS_SCRIPT_DIR/monitoring.log"
    print_info "To check status: ./schedule_monitoring.sh status"
    print_info "To remove: ./schedule_monitoring.sh remove"
}

remove_monitoring() {
    print_header "REMOVING MONITORING"

    if ! crontab -l 2>/dev/null | grep -q "lead_enrichment_monitor"; then
        print_warning "No monitoring cron job found"
        exit 0
    fi

    # Remove cron job
    crontab -l 2>/dev/null | grep -v "lead_enrichment_monitor" | grep -v "Lead Enrichment Monitoring" | crontab -

    print_success "Monitoring removed successfully!"
}

check_status() {
    print_header "MONITORING STATUS"

    if crontab -l 2>/dev/null | grep -q "lead_enrichment_monitor"; then
        print_success "Monitoring is ACTIVE"
        echo ""
        echo "Cron job:"
        crontab -l 2>/dev/null | grep -A1 "Lead Enrichment Monitoring" | tail -1
        echo ""

        # Check for log file
        if [ -f "$SCRIPT_DIR/monitoring.log" ]; then
            echo "Recent activity:"
            echo "----------------------------------------"
            tail -20 "$SCRIPT_DIR/monitoring.log" | grep -E "(MONITORING RUN|ALERT|Error)" || echo "No recent activity"
            echo ""
            print_info "Full log: $SCRIPT_DIR/monitoring.log"
        else
            print_info "No log file yet. Monitoring hasn't run."
        fi
    else
        print_warning "Monitoring is NOT active"
        echo ""
        echo "To set up monitoring:"
        echo "  ./schedule_monitoring.sh setup --leads-file leads.csv"
    fi
}

test_monitoring() {
    local LEADS_FILE=""
    local THRESHOLD=60

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --leads-file)
                LEADS_FILE="$2"
                shift 2
                ;;
            --alert-threshold)
                THRESHOLD="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$LEADS_FILE" ]; then
        print_error "Missing required option: --leads-file"
        exit 1
    fi

    print_header "TESTING MONITORING"
    echo ""

    # Run monitoring once
    cd "$SCRIPT_DIR"
    ./run_enrichment.sh monitor --leads-file "$LEADS_FILE" --schedule weekly --alert-threshold "$THRESHOLD"

    echo ""
    print_success "Test complete"
}

# Main command router
COMMAND="${1:-}"

case "$COMMAND" in
    setup)
        shift
        setup_monitoring "$@"
        ;;
    remove)
        remove_monitoring
        ;;
    status)
        check_status
        ;;
    test)
        shift
        test_monitoring "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
