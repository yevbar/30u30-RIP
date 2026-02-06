import csv
import subprocess
import urllib.parse


def run():
    with open('30u30_all_years.csv', mode='r', newline='', encoding='utf-8') as file, \
         open('30u30_final.csv', mode='w', newline='', encoding='utf-8') as out_file:
        csv_reader = csv.DictReader(file)

        fieldnames = csv_reader.fieldnames
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(csv_reader):
            if row["fraud"] != '':
                writer.writerow(row)
            else:
                query = f'"{row["name"]}" "{row["company"]}" lawsuit sued controversy scandal'
                safe_string = urllib.parse.quote_plus(query)
                subprocess.run(["open", f"https://www.google.com/search?q={safe_string}"])
                fraud = input(f'''[{row["name"]}] Enter reason for fraud (N/A): ''')
                if len(fraud) == 0:
                    fraud = "N/A"

                new_row = {
                    **row,
                    "fraud": fraud,
                }
                writer.writerow(new_row)

run()
