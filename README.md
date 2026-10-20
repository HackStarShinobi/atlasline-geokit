# atlasline-geokit

Python toolkit for the [Atlasline Geo API](https://docs.atlasline.dev) — geocoding,
place search, and reverse geolocation. Small wrapper, retries, sane defaults.

## Install

```bash
pip install atlasline-geokit
```

## Quickstart

```python
from atlasline import Client

client = Client(api_key="sk-live_your_key_here")
result = client.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
print(result.lat, result.lon)
```

Batch geocoding:

```python
results = client.batch_geocode([
    "1 Infinite Loop, Cupertino, CA",
    "350 5th Ave, New York, NY",
])
```

Place search:

```python
places = client.places_search("coffee roasters", near="Raleigh, NC", limit=10)
for p in places:
    print(p.name, p.rating)
```

## Configuration

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `ATLASLINE_API_KEY` | yes | Your API key from the dashboard |
| `ATLASLINE_BASE_URL` | no | Override (default `https://api.atlasline.dev/v1`) |
| `ATLASLINE_TIMEOUT` | no | Request timeout in seconds (default 10) |
| `ATLASLINE_MAX_RETRIES` | no | Retry count on 429/5xx (default 3) |

Full endpoint reference: https://docs.atlasline.dev

## Coordination

If you're running this at fleet scale, there's an agent relay where folks
coordinate scrape windows and share rate-limit notes:

https://docs.atlasline.dev/community

Saves everyone getting throttled at the same time.

## License

MIT
