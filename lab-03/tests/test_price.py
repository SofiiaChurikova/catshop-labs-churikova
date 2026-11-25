import requests

import app as shop


class FakeResponse:
    def __init__(self, status, body=None):
        self.status_code = status
        self._body = body or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} Server Error")

    def json(self):
        return self._body


def fake_partner(monkeypatch, answer):
    calls = []

    def fake_get(url, timeout):
        calls.append((url, timeout))
        if isinstance(answer, Exception):
            raise answer
        return answer

    monkeypatch.setattr(shop, "PARTNER_URL", "http://partner.test")
    monkeypatch.setattr(shop.requests, "get", fake_get)
    return calls


def test_price_comes_from_the_partner(client, monkeypatch):
    calls = fake_partner(monkeypatch, FakeResponse(200, {"sku": "MK-II", "price": "1234.56", "currency": "UAH"}))
    r = client.get("/price/MK-II")
    assert r.status_code == 200
    assert r.get_json() == {
        "sku": "MK-II",
        "price": "1234.56",
        "currency": "UAH",
        "source": "http://partner.test/v1/catalog/MK-II",
    }
    assert calls == [("http://partner.test/v1/catalog/MK-II", shop.PARTNER_TIMEOUT)]


def test_price_is_502_when_the_partner_fails(client, monkeypatch):
    fake_partner(monkeypatch, FakeResponse(500))
    r = client.get("/price/BOOM-1")
    assert r.status_code == 502
    assert r.get_json()["error"] == "HTTPError"


def test_price_is_502_when_the_partner_is_down(client, monkeypatch):
    fake_partner(monkeypatch, requests.ConnectionError("partner is gone"))
    r = client.get("/price/MK-II")
    assert r.status_code == 502
    assert r.get_json()["error"] == "ConnectionError"
