import csv
import json
import sys

csv.field_size_limit(sys.maxsize)

rows = []
with open("30u30_final.csv", "r", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cleaned = {}
        for k, v in row.items():
            cleaned[k.strip()] = v.strip().replace("\r", "")
        rows.append(cleaned)

with open("file.json", "w") as f:
    json.dump(rows, f)

print(f"Wrote {len(rows)} records to file.json")
