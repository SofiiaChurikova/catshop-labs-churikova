import pytest

import app as shop


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(shop, "COUNTER_FILE", tmp_path / "visits.txt")
    monkeypatch.setattr(shop, "DATABASE_URL", None)
    shop.app.config["TESTING"] = True
    return shop.app.test_client()
