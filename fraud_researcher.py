#!/usr/bin/env python3
"""
Forbes 30 Under 30 Fraud Researcher
Utility functions for CSV management and progress tracking.
Actual searches performed via Playwright MCP tools.
"""

import csv
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
CSV_FILE = BASE_DIR / "30u30_all_years.csv"
PROGRESS_FILE = BASE_DIR / "progress" / "progress.json"
RESULTS_FILE = BASE_DIR / "progress" / "results.json"
METHODOLOGY_FILE = BASE_DIR / "search_methodology.md"

# Fraud indicator keywords
HIGH_CONFIDENCE = [
    "sentenced", "convicted", "guilty", "prison", "pleaded guilty",
    "federal prison", "years in prison", "months in prison"
]
MEDIUM_CONFIDENCE = [
    "indicted", "charged", "arrested", "SEC charges", "fraud allegations",
    "criminal charges", "wire fraud", "securities fraud", "bank fraud"
]


def load_csv():
    """Load the CSV file and return list of dicts."""
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_csv(rows, fieldnames=None):
    """Save rows back to CSV file."""
    if not fieldnames:
        fieldnames = ['year', 'name', 'age', 'title', 'company', 'category', 'description', 'fraud']
    with open(CSV_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_progress():
    """Load progress tracking file."""
    with open(PROGRESS_FILE, 'r') as f:
        return json.load(f)


def save_progress(progress):
    """Save progress tracking file."""
    progress['last_updated'] = datetime.now().isoformat()
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)


def load_results():
    """Load results file."""
    with open(RESULTS_FILE, 'r') as f:
        return json.load(f)


def save_results(results):
    """Save results file."""
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)


def update_fraud_status(row_index, fraud_description):
    """Update fraud column for a specific row."""
    rows = load_csv()
    if 0 <= row_index < len(rows):
        rows[row_index]['fraud'] = fraud_description
        save_csv(rows)
        return True
    return False


def add_fraud_case(name, year, company, fraud_description, source, query_used):
    """Record a fraud case in results.json."""
    results = load_results()
    results['fraud_cases'].append({
        'name': name,
        'year': year,
        'company': company,
        'fraud_description': fraud_description,
        'source': source,
        'query_used': query_used,
        'timestamp': datetime.now().isoformat()
    })
    save_results(results)


def add_uncertain_case(name, year, company, reason):
    """Record an uncertain case for manual review."""
    results = load_results()
    results['uncertain_cases'].append({
        'name': name,
        'year': year,
        'company': company,
        'reason': reason,
        'timestamp': datetime.now().isoformat()
    })
    save_results(results)


def find_person_row(name, year=None, company=None):
    """Find a person's row index in the CSV."""
    rows = load_csv()
    for i, row in enumerate(rows):
        if row['name'].lower() == name.lower():
            if year and str(row['year']) != str(year):
                continue
            if company and company.lower() not in row.get('company', '').lower():
                continue
            return i, row
    return None, None


def get_next_unprocessed(start_from=0):
    """Get the next person who hasn't been processed."""
    rows = load_csv()
    progress = load_progress()

    for i in range(start_from, len(rows)):
        if not rows[i].get('fraud'):  # Empty fraud field = not processed
            return i, rows[i]
    return None, None


def generate_search_queries(name, company):
    """Generate search queries for a person."""
    queries = [
        f'"{name}" "{company}" arrested',
        f'"{name}" "{company}" convicted fraud',
        f'"{name}" "{company}" sentenced prison',
        f'"{name}" "{company}" criminal charges',
        f'site:justice.gov "{name}"',
        f'site:sec.gov "{name}"',
    ]
    return queries


def analyze_text_for_fraud(text):
    """Analyze text for fraud indicators. Returns (confidence, keywords_found)."""
    text_lower = text.lower()

    high_found = [kw for kw in HIGH_CONFIDENCE if kw in text_lower]
    medium_found = [kw for kw in MEDIUM_CONFIDENCE if kw in text_lower]

    if high_found:
        return 'high', high_found
    elif medium_found:
        return 'medium', medium_found
    else:
        return 'none', []


def get_known_fraud_cases():
    """Return list of known fraud cases for validation."""
    return [
        {
            'name': 'Charlie Javice',
            'search_year': 2019,
            'company': 'Frank',
            'expected': 'Convicted wire/bank/securities fraud. Sentenced 85 months prison (2025)'
        },
        {
            'name': 'Sam Bankman-Fried',
            'search_year': 2021,
            'company': 'FTX',
            'expected': 'Convicted fraud/conspiracy. Sentenced 25 years prison (2024)'
        },
        {
            'name': 'Caroline Ellison',
            'search_year': 2022,
            'company': 'Alameda Research',
            'expected': 'Pleaded guilty to fraud. Sentenced 2 years prison (2024)'
        },
        {
            'name': 'Elizabeth Holmes',
            'search_year': None,  # May not be in dataset
            'company': 'Theranos',
            'expected': 'Convicted fraud. Sentenced 11+ years prison (2022)'
        },
    ]


def print_summary():
    """Print current processing summary."""
    progress = load_progress()
    results = load_results()

    print(f"\n=== Processing Summary ===")
    print(f"Total rows: {progress['total_rows']}")
    print(f"Processed: {progress['processed_count']}")
    print(f"Fraud found: {progress['fraud_found_count']}")
    print(f"Last updated: {progress['last_updated']}")
    print(f"\nFraud cases: {len(results['fraud_cases'])}")
    print(f"Uncertain cases: {len(results['uncertain_cases'])}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'summary':
            print_summary()

        elif cmd == 'known':
            print("\n=== Known Fraud Cases for Validation ===")
            for case in get_known_fraud_cases():
                idx, row = find_person_row(case['name'], case['search_year'], case['company'])
                status = f"Row {idx}" if idx is not None else "NOT FOUND in dataset"
                print(f"\n{case['name']} ({case['company']}, {case['search_year']})")
                print(f"  Status: {status}")
                print(f"  Expected: {case['expected']}")

        elif cmd == 'queries' and len(sys.argv) > 3:
            name = sys.argv[2]
            company = sys.argv[3]
            print(f"\n=== Search Queries for {name} ({company}) ===")
            for q in generate_search_queries(name, company):
                print(f"  {q}")

        elif cmd == 'find' and len(sys.argv) > 2:
            name = ' '.join(sys.argv[2:])
            idx, row = find_person_row(name)
            if row:
                print(f"\nFound at row {idx}:")
                for k, v in row.items():
                    print(f"  {k}: {v}")
            else:
                print(f"Not found: {name}")

        else:
            print("Usage:")
            print("  python fraud_researcher.py summary")
            print("  python fraud_researcher.py known")
            print("  python fraud_researcher.py queries <name> <company>")
            print("  python fraud_researcher.py find <name>")
    else:
        print_summary()
