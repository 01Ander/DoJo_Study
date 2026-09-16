from prefect import flow, task

@task(retries=2)
def extract_resources():
    return [{"ingredient": "Cosmic Dust"}]

@task
def load_to_vault(data):
    return True

@flow(name="Alchemical_Logistics_Pipeline")
def orchestrate_day():
    data = extract_resources()
    load_to_vault(data)

# SOLUTION TESTS
'''
import pytest

def test_extract_resources_is_task_with_retries():
    assert hasattr(extract_resources, 'retries'), "Missing or incorrect @task decorator"
    assert extract_resources.retries == 2, "Task must have 2 retries"

def test_load_to_vault_is_task():
    assert hasattr(load_to_vault, 'name'), "Missing @task decorator"

def test_orchestrate_day_is_flow():
    assert hasattr(orchestrate_day, 'name'), "Missing @flow decorator"
    assert orchestrate_day.name == "Alchemical_Logistics_Pipeline", "Incorrect flow name"
'''
