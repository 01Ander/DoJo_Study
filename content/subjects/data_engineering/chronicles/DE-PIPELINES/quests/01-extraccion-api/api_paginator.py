"""Module: api_paginator

Provides resilient REST API extraction mechanisms with offset and cursor pagination,
rate limit handling (HTTP 429), backoff retry logic, and loop safeguards.
"""

from typing import Any
import time
import requests


class RateLimitExceededError(Exception):
    """Raised when HTTP 429 retries are exhausted."""
    pass


def extract_paginated_offset(
    api_url: str,
    token: str,
    page_size: int = 20,
    max_pages: int = 50,
) -> list[dict[str, Any]]:
    """Extracts records using page/limit pagination with deduplication and loop guards.

    Args:
        api_url: Base endpoint URL.
        token: Bearer authentication token.
        page_size: Expected number of items per page.
        max_pages: Safeguard maximum number of pages to fetch.

    Returns:
        List of unique extracted dictionary records.
    """
    # TODO: Implement offset pagination with Bearer auth, query params, deduplication, and termination rules.
    headers = {"Authorization": f"Bearer {token}"}
    results = []
    seen_ids = set()
    page = 1

    while page <= max_pages:
        params = {"page": page, "limit": page_size}
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        batch = response.json().get("data", [])

        if not batch:
            break

        for item in batch:
            item_id = item.get("id")
            if item_id and item_id not in seen_ids:
                seen_ids.add(item_id)
                results.append(item)

        if len(batch) < page_size:
            break

        page += 1

    return results


def extract_paginated_cursor(
    api_url: str,
    token: str,
    max_pages: int = 50,
    max_retries: int = 3,
) -> list[dict[str, Any]]:
    """Extracts records using opaque cursor tokens, handling HTTP 429 rate limits with backoff.

    Args:
        api_url: Base endpoint URL.
        token: Bearer authentication token.
        max_pages: Safeguard maximum number of pages to fetch.
        max_retries: Maximum number of retries upon receiving HTTP 429.

    Returns:
        List of all extracted items across all fetched pages.

    Raises:
        RateLimitExceededError: If max_retries is exceeded when receiving HTTP 429.
    """
    # TODO: Implement cursor pagination with Retry-After backoff and rate limit exception handling.
    headers = {"Authorization": f"Bearer {token}"}
    all_items = []
    next_cursor = None
    pages = 0

    while pages < max_pages:
        params = {"limit": 50}
        if next_cursor:
            params["cursor"] = next_cursor

        retries = 0
        while retries <= max_retries:
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            if response.status_code == 429:
                wait_time = float(response.headers.get("Retry-After", 1.0))
                time.sleep(wait_time)
                retries += 1
                continue
            response.raise_for_status()
            break
        else:
            raise RateLimitExceededError("Rate limit exceeded")

        payload = response.json()
        all_items.extend(payload.get("items", []))
        pages += 1

        next_cursor = payload.get("next_cursor")
        if not next_cursor:
            break

    return all_items
