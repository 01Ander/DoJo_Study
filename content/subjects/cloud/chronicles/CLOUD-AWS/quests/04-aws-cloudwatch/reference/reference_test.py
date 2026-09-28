import pytest
import logging
from solution import lambda_handler

def test_lambda_handler_normal_status(caplog):
    """Validates that a stable dragon logs INFO correctly and returns 200 without raising exceptions."""
    caplog.set_level(logging.INFO)
    
    event = {"dragon_id": 10, "instability": 50}
    result = lambda_handler(event, {})
    
    assert result['statusCode'] == 200, "Must return 200 if instability is < 90"
    
    # Verify logs injected to CloudWatch
    messages = [record.message for record in caplog.records]
    assert "Processing report for dragon ID: 10" in messages
    assert "Normal status. Finishing." in messages

def test_lambda_handler_critical_status(caplog):
    """Validates that an unstable dragon logs ERROR with the exact phrase and returns 500."""
    caplog.set_level(logging.INFO)
    
    event = {"dragon_id": 99, "instability": 95}
    result = lambda_handler(event, {})
    
    assert result['statusCode'] == 500, "The catastrophic exception should be caught and return 500."
    
    error_messages = [record.message for record in caplog.records if record.levelname == 'ERROR']
    
    # The phrase must match identically for the Guild Metric Filter to trigger
    expected_phrase = "CRITICAL DANGER! Dragon 99 about to explode. Level: 95"
    assert expected_phrase in error_messages, f"Missing exact critical error log for CloudWatch. Expected: {expected_phrase}"
    
    # Validate that global try/except also logged the final failure
    assert any("Pipeline failure: Catastrophic instability" in m for m in error_messages), "Final exception was not logged."
