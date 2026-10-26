"""Validation suite for Quest 01-02: Resilient API Pagination & Rate Limiting.

Tests offset pagination, cursor pagination, rate limit backoff (HTTP 429),
deduplication, and infinite loop safeguards.
"""

from unittest.mock import patch
import pytest
import responses
import requests

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from api_paginator import (
    extract_paginated_offset,
    extract_paginated_cursor,
    RateLimitExceededError,
)

BASE_URL = "https://api.aerofleet.fake/v1"
TOKEN = "secret_flight_token_xyz"


# ==============================================================================
# OFFSET PAGINATION TESTS
# ==============================================================================

@responses.activate
def test_offset_pagination_multi_page_and_deduplication():
    """Validates multi-page offset extraction and defensive deduplication of duplicate IDs."""
    endpoint = f"{BASE_URL}/flights"

    # Page 1: 2 items (limit=2)
    responses.add(
        responses.GET,
        f"{endpoint}?page=1&limit=2",
        json={"data": [{"id": "FL-001", "callsign": "Aero1"}, {"id": "FL-002", "callsign": "Aero2"}]},
        status=200,
    )

    # Page 2: 2 items (one duplicate FL-002 due to page drift, one new FL-003)
    responses.add(
        responses.GET,
        f"{endpoint}?page=2&limit=2",
        json={"data": [{"id": "FL-002", "callsign": "Aero2"}, {"id": "FL-003", "callsign": "Aero3"}]},
        status=200,
    )

    # Page 3: 1 item (< limit=2, terminates pagination)
    responses.add(
        responses.GET,
        f"{endpoint}?page=3&limit=2",
        json={"data": [{"id": "FL-004", "callsign": "Aero4"}]},
        status=200,
    )

    results = extract_paginated_offset(endpoint, TOKEN, page_size=2, max_pages=10)

    assert results is not None, "extract_paginated_offset must return a list, got None"
    assert len(results) == 4, f"Expected 4 unique flights, got {len(results)}"
    ids = [item["id"] for item in results]
    assert ids == ["FL-001", "FL-002", "FL-003", "FL-004"]


@responses.activate
def test_offset_pagination_max_pages_safeguard():
    """Validates that extraction halts at max_pages even when more data is available."""
    endpoint = f"{BASE_URL}/flights"

    for p in range(1, 6):
        responses.add(
            responses.GET,
            f"{endpoint}?page={p}&limit=2",
            json={"data": [{"id": f"FL-{p}A"}, {"id": f"FL-{p}B"}]},
            status=200,
        )

    # Limit to 2 pages maximum
    results = extract_paginated_offset(endpoint, TOKEN, page_size=2, max_pages=2)

    assert results is not None
    assert len(results) == 4, f"Expected 4 records across 2 max pages, got {len(results)}"


# ==============================================================================
# CURSOR PAGINATION TESTS
# ==============================================================================

@responses.activate
def test_cursor_pagination_success():
    """Validates sequential cursor-based extraction until next_cursor is None."""
    endpoint = f"{BASE_URL}/telemetry"

    # Batch 1 (initial request, no cursor query param)
    responses.add(
        responses.GET,
        f"{endpoint}?limit=50",
        json={
            "items": [{"event_id": "EVT-100", "altitude": 32000}],
            "next_cursor": "cur_alpha",
        },
        status=200,
    )

    # Batch 2 (with cursor cur_alpha)
    responses.add(
        responses.GET,
        f"{endpoint}?limit=50&cursor=cur_alpha",
        json={
            "items": [{"event_id": "EVT-101", "altitude": 34000}],
            "next_cursor": "cur_beta",
        },
        status=200,
    )

    # Batch 3 (with cursor cur_beta, end of stream)
    responses.add(
        responses.GET,
        f"{endpoint}?limit=50&cursor=cur_beta",
        json={
            "items": [{"event_id": "EVT-102", "altitude": 36000}],
            "next_cursor": None,
        },
        status=200,
    )

    results = extract_paginated_cursor(endpoint, TOKEN, max_pages=10)

    assert results is not None, "extract_paginated_cursor must return a list, got None"
    assert len(results) == 3, f"Expected 3 events across cursor stream, got {len(results)}"
    event_ids = [e["event_id"] for e in results]
    assert event_ids == ["EVT-100", "EVT-101", "EVT-102"]


@responses.activate
@patch("time.sleep", return_value=None)
def test_cursor_pagination_rate_limit_retry_success(mock_sleep):
    """Validates that receiving HTTP 429 triggers a Retry-After wait and subsequent retry success."""
    endpoint = f"{BASE_URL}/telemetry"

    # Page 1 succeeds
    responses.add(
        responses.GET,
        f"{endpoint}?limit=50",
        json={"items": [{"event_id": "EVT-200"}], "next_cursor": "cur_retry_step"},
        status=200,
    )

    # Page 2 attempt 1: Rate limit 429
    responses.add(
        responses.GET,
        f"{endpoint}?limit=50&cursor=cur_retry_step",
        headers={"Retry-After": "2.5"},
        json={"error": "Too Many Requests"},
        status=429,
    )

    # Page 2 attempt 2 (retry): 200 OK with data and end
    responses.add(
        responses.GET,
        f"{endpoint}?limit=50&cursor=cur_retry_step",
        json={"items": [{"event_id": "EVT-201"}], "next_cursor": None},
        status=200,
    )

    results = extract_paginated_cursor(endpoint, TOKEN, max_retries=2)

    assert results is not None
    assert len(results) == 2, f"Expected 2 events recovered after rate limit retry, got {len(results)}"
    assert mock_sleep.called, "Expected time.sleep to be called when HTTP 429 was encountered"
    mock_sleep.assert_called_with(2.5)


@responses.activate
@patch("time.sleep", return_value=None)
def test_cursor_pagination_rate_limit_exceeded_error(mock_sleep):
    """Validates that exhausting max_retries on HTTP 429 raises RateLimitExceededError."""
    endpoint = f"{BASE_URL}/telemetry"

    # Repeatedly return 429
    for _ in range(4):
        responses.add(
            responses.GET,
            f"{endpoint}?limit=50",
            headers={"Retry-After": "1.0"},
            json={"error": "Rate limited"},
            status=429,
        )

    with pytest.raises(RateLimitExceededError):
        extract_paginated_cursor(endpoint, TOKEN, max_retries=2)
