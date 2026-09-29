import pytest
import logging
from my_solution import lambda_handler

def test_lambda_handler_normal_status(caplog):
    """Validates that a stable dragon logs INFO correctly and returns 200."""
    caplog.set_level(logging.INFO)
    event = {"dragon_id": 10, "instability": 50}

    # EXERCISE: Call lambda_handler(event, {}) and assert:
    # 1. statusCode is 200
    # 2. caplog records contain "Processing report for dragon ID: 10"
    # 3. caplog records contain "Normal status. Finishing."
    # Your code here:
    pass


def test_lambda_handler_critical_status(caplog):
    """Validates that an unstable dragon logs ERROR with the exact phrase and returns 500."""
    caplog.set_level(logging.INFO)
    event = {"dragon_id": 99, "instability": 95}

    # EXERCISE: Call lambda_handler(event, {}) and assert:
    # 1. statusCode is 500
    # 2. caplog ERROR logs contain:
    #    "CRITICAL DANGER! Dragon 99 about to explode. Level: 95"
    # 3. caplog ERROR logs contain "Pipeline failure: Catastrophic instability"
    # Your code here:
    pass

