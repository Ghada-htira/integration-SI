# scripts/generate_html.py
from pymongo import MongoClient
import os

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
DB = os.getenv('MONGO_DB', 'testdb')
COL = os.getenv('MONGO_COLLECTION', 'restaurants')
OUT_PATH = os.getenv('OUT_PATH', '../nginx-site/site/index.html')

client = MongoClient(MONGO_URI)
db = client[DB]
collection = db[COL]

docs = list(collection.find())

html = "<!doctype html>\n<html><head><meta charset='utf-8'><title>Restaurants</title></head><body>\n"
html += "<h1>Restaurants — collection</h1>\n"
html += "<ul>\n"
for d in docs:
    name = d.get('name','-')
    address = d.get('address', {})
    street = address.get('street', '')
    building = address.get('building', '')
    zipcode = address.get('zipcode', '')
    addr = f"{building} {street} {zipcode}"
    html += f"<li><strong>{name}</strong> — {addr}</li>\n"
html += "</ul>\n"
html += "</body></html>"

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Wrote {len(docs)} docs to {OUT_PATH}")
