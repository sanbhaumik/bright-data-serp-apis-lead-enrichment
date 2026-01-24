#!/bin/bash
#
# Lead Enrichment Engine - Easy Runner Script
#
# This script provides a convenient way to run the lead enrichment CLI
# with proper environment activation and error handling.
#
# Usage:
#   ./run_enrichment.sh enrich --domain stripe.com
#   ./run_enrichment.sh batch --input leads.csv
#   ./run_enrichment.sh preset --list
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to print colored messages
print_error() {
    echo -e "${RED}✗ Error: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found"
    echo ""
    echo "Please create .env file with your API credentials:"
    echo "  1. cp .env.example .env"
    echo "  2. Edit .env and add your SERP_API_KEY and SERP_ZONE"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Virtual environment not found. Creating..."
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import requests" 2>/dev/null; then
    print_info "Installing dependencies..."
    pip install -r requirements.txt
    print_success "Dependencies installed"
fi

# Run the CLI with all arguments
print_info "Running enrichment engine..."
echo ""

python cli.py "$@"
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

# Exit with CLI's exit code
exit $EXIT_CODE
