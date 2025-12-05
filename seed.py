import requests, random
from datetime import date, timedelta

BASE = "http://localhost:8000"

items = ["Rice", "Dal", "Sambar", "Curd", "Veg Curry"]

start = date.today() - timedelta(days=60)
for i in range(60):
    d = start + timedelta(days=i)
    for item in items:
        prepared = random.uniform(15, 40)
        consumed = prepared - random.uniform(1, 10)
        requests.post(f"{BASE}/add-entry", json={
            "date": d.isoformat(),
            "item_name": item,
            "prepared_qty": round(prepared, 2),
            "consumed_qty": round(consumed, 2)
        })
print("Seed completed!")
