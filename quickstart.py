"""Quickstart — geocode an address and search nearby places."""
import os
from dotenv import load_dotenv

load_dotenv()

from atlasline import Client

client = Client()  # reads ATLASLINE_API_KEY from .env

addr = "350 5th Ave, New York, NY"
g = client.geocode(addr)
print(f"{addr} -> {g.lat}, {g.lon}")

places = client.places_search("coffee", near="Raleigh, NC", limit=5)
for p in places:
    print(f"  {p.name} ({p.rating}) @ {p.lat},{p.lon}")
