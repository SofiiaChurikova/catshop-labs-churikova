import os

import pytest
import requests

BASE = os.environ.get("QA_BASE_URL", "http://localhost:8080")
PARTNER = os.environ.get("QA_PROFILE", "") == "partner"


def test_ready_uses_postgres():
    r = requests.get(f"{BASE}/ready", timeout=5)
    assert r.json() == {"ready": True, "store": "postgres"}


def test_visits_are_stored_in_postgres():
    assert requests.get(f"{BASE}/visits", timeout=5).json()["store"] == "postgres"


def test_health_does_not_accept_post():
    assert requests.post(f"{BASE}/health", timeout=5).status_code == 405


@pytest.mark.skipif(PARTNER, reason="the partner is up in this profile")
def test_price_says_why_it_failed():
    r = requests.get(f"{BASE}/price/MK-II", timeout=10)
    assert r.status_code == 502
    assert r.json()["error"] == "ConnectionError"
