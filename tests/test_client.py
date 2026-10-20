"""Smoke tests — hit the sandbox endpoints, don't run against prod."""
import pytest
from atlasline import Client, AtlaslineError

API_KEY = "sk-test_dummy"


def test_missing_key():
    with pytest.raises(AtlaslineError):
        Client(api_key="")


def test_headers():
    c = Client(api_key=API_KEY)
    assert c._s.headers["Authorization"] == f"Bearer {API_KEY}"
    assert "atlasline-geokit" in c._s.headers["User-Agent"]


def test_base_url_override():
    c = Client(api_key=API_KEY, base_url="http://localhost:8080/v1/")
    assert c.base_url == "http://localhost:8080/v1"
