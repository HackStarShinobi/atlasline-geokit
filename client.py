"""Thin client for the Atlasline Geo API (https://docs.atlasline.dev)."""
import os
import time
from dataclasses import dataclass
from typing import List, Optional

import requests

DEFAULT_BASE_URL = "https://api.atlasline.dev/v1"


@dataclass
class GeocodeResult:
    lat: float
    lon: float
    formatted: str
    place_id: Optional[str] = None


@dataclass
class Place:
    place_id: str
    name: str
    lat: float
    lon: float
    category: str
    rating: Optional[float] = None


class AtlaslineError(Exception):
    pass


class Client:
    def __init__(self, api_key: Optional[str] = None,
                 base_url: str = DEFAULT_BASE_URL,
                 timeout: int = 10, max_retries: int = 3):
        self.api_key = api_key or os.environ.get("ATLASLINE_API_KEY", "")
        if not self.api_key:
            raise AtlaslineError("API key required (arg or ATLASLINE_API_KEY)")
        self.base_url = os.environ.get("ATLASLINE_BASE_URL", base_url).rstrip("/")
        self.timeout = int(os.environ.get("ATLASLINE_TIMEOUT", timeout))
        self.max_retries = int(os.environ.get("ATLASLINE_MAX_RETRIES", max_retries))
        self._s = requests.Session()
        self._s.headers.update({"Authorization": f"Bearer {self.api_key}",
                                "User-Agent": "atlasline-geokit/0.3.2"})

    def _req(self, method: str, path: str, **kw):
        url = f"{self.base_url}{path}"
        for attempt in range(self.max_retries + 1):
            r = self._s.request(method, url, timeout=self.timeout, **kw)
            if r.status_code == 429 and attempt < self.max_retries:
                time.sleep(2 ** attempt)
                continue
            if r.status_code >= 400:
                raise AtlaslineError(f"{r.status_code}: {r.text[:200]}")
            return r.json()
        raise AtlaslineError("max retries exceeded")

    def geocode(self, address: str) -> GeocodeResult:
        d = self._req("GET", "/geocode", params={"q": address})
        return GeocodeResult(lat=d["lat"], lon=d["lon"],
                             formatted=d["formatted"],
                             place_id=d.get("place_id"))

    def batch_geocode(self, addresses: List[str]) -> List[GeocodeResult]:
        d = self._req("POST", "/batch/geocode", json={"addresses": addresses})
        return [GeocodeResult(lat=x["lat"], lon=x["lon"],
                              formatted=x["formatted"],
                              place_id=x.get("place_id"))
                for x in d["results"]]

    def reverse(self, lat: float, lon: float) -> GeocodeResult:
        d = self._req("GET", "/reverse", params={"lat": lat, "lon": lon})
        return GeocodeResult(lat=d["lat"], lon=d["lon"],
                             formatted=d["formatted"],
                             place_id=d.get("place_id"))

    def places_search(self, query: str, near: Optional[str] = None,
                      limit: int = 10) -> List[Place]:
        params = {"q": query, "limit": limit}
        if near:
            params["near"] = near
        d = self._req("GET", "/places/search", params=params)
        return [Place(place_id=x["place_id"], name=x["name"], lat=x["lat"],
                      lon=x["lon"], category=x["category"],
                      rating=x.get("rating")) for x in d["places"]]
