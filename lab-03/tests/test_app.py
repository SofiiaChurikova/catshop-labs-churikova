import app as shop


def test_health_says_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "ok\n"


def test_visits_counts_up(client):
    assert client.get("/visits").get_json() == {"visits": 1, "store": "file"}
    assert client.get("/visits").get_json() == {"visits": 2, "store": "file"}


def test_visits_are_saved_in_the_counter_file(client):
    for _ in range(3):
        client.get("/visits")
    assert shop.COUNTER_FILE.read_text() == "3"


def test_visits_is_503_when_the_store_is_broken(client, monkeypatch, tmp_path):
    monkeypatch.setattr(shop, "COUNTER_FILE", tmp_path)
    r = client.get("/visits")
    assert r.status_code == 503
    assert r.get_json()["store"] == "file"


def test_ready_with_the_file_store(client):
    r = client.get("/ready")
    assert r.status_code == 200
    body = r.get_json()
    assert body["ready"] is True
    assert body["store"].startswith("file:")


def test_ready_is_503_when_the_database_is_down(client, monkeypatch):
    monkeypatch.setattr(shop, "DATABASE_URL", "postgresql://catshop:x@127.0.0.1:1/catshop")
    r = client.get("/ready")
    assert r.status_code == 503
    assert r.get_json()["ready"] is False
