"""
SERP API Client for Lead Enrichment Engine
Handles communication with Bright Data SERP API to retrieve search results
"""

import logging
import requests
from urllib.parse import quote_plus
from requests.exceptions import RequestException
import config

# Configure logging for API interactions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SerpClient:
    """
    Client for interacting with Bright Data SERP API

    This client handles search queries and result processing for signal detection.
    It manages authentication, request formatting, and error handling.
    """

    def __init__(self):
        """
        Initialize SERP API client with credentials from config

        Validates that required configuration is present before creating client
        """
        config.validate_config()
        self.api_key = config.SERP_API_KEY
        self.zone = config.SERP_ZONE
        self.base_url = "https://api.brightdata.com/request"
        self.default_country = config.DEFAULT_COUNTRY
        self.default_language = config.DEFAULT_LANGUAGE

        logger.info(f"SerpClient initialized for zone: {self.zone}")

    def query(self, keyword, gl=None, hl=None):
        """
        Execute a search query through Bright Data SERP API

        Args:
            keyword (str): Search query/keyword to look up
            gl (str, optional): Country code for search localization (e.g., 'us', 'uk')
            hl (str, optional): Language code for search results (e.g., 'en', 'es')

        Returns:
            dict: JSON response from SERP API containing search results
                  Returns {"results": []} on failure to maintain consistent interface

        Example:
            results = client.query("data engineer hiring", gl="us", hl="en")
        """
        # Use defaults if not specified
        gl = gl or self.default_country
        hl = hl or self.default_language

        # URL encode the search keyword to handle special characters
        encoded_keyword = quote_plus(keyword)
        search_url = f"https://www.google.com/search?q={encoded_keyword}&gl={gl}&hl={hl}"

        # Prepare request headers with authentication
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Build request payload for Bright Data API
        payload = {
            "zone": self.zone,
            "url": search_url,
            "format": "json"
        }

        try:
            logger.info(f"Querying SERP API: '{keyword}' (gl={gl}, hl={hl})")

            # Make POST request with 30 second timeout
            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            # Raise exception for bad status codes (4xx, 5xx)
            response.raise_for_status()

            # Parse and return JSON response
            result = response.json()
            logger.info(f"Successfully retrieved results for: '{keyword}'")
            return result

        except RequestException as e:
            # Log the error but don't crash - return empty results
            logger.error(f"SERP API request failed for '{keyword}': {str(e)}")
            return {"results": []}

        except Exception as e:
            # Catch any other unexpected errors (JSON parsing, etc.)
            logger.error(f"Unexpected error processing SERP response for '{keyword}': {str(e)}")
            return {"results": []}

    def search_for_signals(self, query, result_count=3):
        """
        Search for buying signals and return formatted results

        This method queries the SERP API and filters/formats results specifically
        for signal detection. It removes very short or very long descriptions that
        are less likely to contain useful signal information.

        Args:
            query (str): Search query to execute
            result_count (int, optional): Maximum number of results to return. Defaults to 3.

        Returns:
            list: List of dictionaries containing:
                - title (str): Page title
                - url (str): Page URL
                - description (str): Full description text
                - snippet (str): First 150 characters of description

        Example:
            signals = client.search_for_signals("Acme Corp data quality issues", result_count=5)
            for signal in signals:
                print(f"{signal['title']}: {signal['snippet']}")
        """
        # Execute the search query
        response = self.query(query)

        # Handle empty or malformed responses gracefully
        if not response or "results" not in response:
            logger.warning(f"No results found for query: '{query}'")
            return []

        results = response.get("results", [])
        if not results:
            logger.warning(f"Empty results list for query: '{query}'")
            return []

        formatted_results = []

        for result in results:
            # Safely extract fields with defaults for missing data
            title = result.get("title", "")
            url = result.get("url", "")
            description = result.get("description", "")

            # Filter: Only include results with meaningful descriptions
            # Too short (< 60 chars): likely not enough context
            # Too long (> 600 chars): likely spam or irrelevant
            if 60 <= len(description) <= 600:
                # Create snippet: first 150 characters with ellipsis
                snippet = description[:150] + "..." if len(description) > 150 else description

                formatted_results.append({
                    "title": title,
                    "url": url,
                    "description": description,
                    "snippet": snippet
                })

            # Stop once we've collected enough results
            if len(formatted_results) >= result_count:
                break

        logger.info(f"Formatted {len(formatted_results)} results from query: '{query}'")
        return formatted_results


if __name__ == "__main__":
    """
    Test the SERP client with a sample query

    Run this script directly to test the API connection:
    python serp_client.py
    """
    print("Testing SERP API Client...")
    print("-" * 50)

    try:
        # Initialize client
        client = SerpClient()
        print(f"✓ Client initialized successfully")
        print(f"  Zone: {client.zone}")
        print(f"  Defaults: gl={client.default_country}, hl={client.default_language}")
        print()

        # Test search for signals
        test_query = "Snowflake data warehouse hiring"
        print(f"Testing query: '{test_query}'")
        print()

        results = client.search_for_signals(test_query, result_count=3)

        if results:
            print(f"✓ Found {len(results)} results:")
            print()
            for i, result in enumerate(results, 1):
                print(f"{i}. {result['title']}")
                print(f"   URL: {result['url']}")
                print(f"   Snippet: {result['snippet']}")
                print()
        else:
            print("✗ No results returned (check your API credentials)")

    except ValueError as e:
        print(f"✗ Configuration error: {e}")
        print("  Please ensure your .env file is set up correctly")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
