import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure the `src` module path is available for test imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import app as src_app

@pytest.fixture(scope="session")
def app_module():
    return src_app

@pytest.fixture(scope="session")
def client(app_module):
    return TestClient(app_module.app)

@pytest.fixture(autouse=True)
def reset_activities(app_module):
    initial_state = copy.deepcopy(app_module.activities)
    app_module.activities = initial_state
    yield
    app_module.activities = copy.deepcopy(initial_state)
