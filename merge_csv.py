#!/usr/bin/env python3
import csv
from collections import OrderedDict

csv_files = [
    ("30u30/2013/forbes_30u30_2013.csv", 2013),
    ("30u30/2014/people.csv", 2014),
    ("30u30/2015/people.csv", 2015),
    ("30u30/2016/people.csv", 2016),
    ("30u30/2017/all_honorees.csv", 2017),
    ("30u30/2018/all_honorees.csv", 2018),
    ("30u30/2019/all_honorees.csv", 2019),
    ("30u30/2020/all_honorees.csv", 2020),
    ("30u30/2021/all_honorees.csv", 2021),
    ("30u30/2022/all_honorees.csv", 2022),
    ("30u30/2023/all_honorees.csv", 2023),
    ("30u30/2024/all_honorees.csv", 2024),
    ("30u30/2025/forbes_30u30_2025.csv", 2025),
    ("30u30/2026/forbes_30u30_2026.csv", 2026),
]

all_rows = []
all_columns = set()

for file_path, year in csv_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Normalize column names to lowercase
            normalized_row = {k.lower().strip(): v for k, v in row.items()}
            normalized_row['year'] = str(year)
            all_rows.append(normalized_row)
            all_columns.update(normalized_row.keys())

# Order columns: year first, then common ones, then rest
preferred_order = ['year', 'name', 'age', 'title', 'company', 'category', 'description']
final_columns = [c for c in preferred_order if c in all_columns]
final_columns += sorted([c for c in all_columns if c not in final_columns])

# Write merged CSV
with open('30u30_all_years.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=final_columns)
    writer.writeheader()
    for row in all_rows:
        writer.writerow({col: row.get(col, '') for col in final_columns})

print(f"Merged {len(all_rows)} records into 30u30_all_years.csv")
print(f"Columns: {final_columns}")
