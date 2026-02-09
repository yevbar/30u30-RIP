import csv
import subprocess
import urllib.parse

from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

empty_config = types.GenerateContentConfig(tools=[])


def run():
    with open('30u30_all_years.csv', mode='r', newline='', encoding='utf-8') as file, \
         open('30u30_final.csv', mode='w', newline='', encoding='utf-8') as out_file:
        csv_reader = csv.DictReader(file)

        fieldnames = csv_reader.fieldnames
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()

        rows = list(csv_reader)
        for i, row in enumerate(rows):
            if i % 10 == 0:
                print()
                print(f"{i} / {len(rows)}")
                print()

            if row["fraud"] != '':
                writer.writerow(row)
            else:
                identifier = (row["name"] + " from " + row["company"]) if len(row["company"]) > 0 else row["name"]
                query = f'Did the Forbes 30 under 30 winner {identifier} get targeted by any lawsuit, suing, scandal, or controversy? Return ONLY the string "N/A" if there is none'
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=query,
                        config=config,
                    )
                except:
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=query,
                        config=config,
                    )

                new_row = dict()
                if response.text is None:
                    print()
                    print("Got back a none!")
                    print()
                    new_row = {
                        **row,
                        "fraud": "N/A",
                    }
                elif "N/A" in response.text:
                    new_row = {
                        **row,
                        "fraud": "N/A"
                    }
                else:
                    confirm_response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents="Answer with either YES or NO - does the below text describe a true positive controversy? Answer no if it says there is no controvery\n\n" + response.text,
                        config=empty_config
                    )

                    if confirm_response is None:
                        print()
                        print("GOT BACK NONE FOR CONFIRM RESPONSE")
                        print()
                        new_row = {
                            **row,
                            "fraud": response.text
                        }
                    elif "no" in confirm_response.text.lower():
                        new_row = {
                            **row,
                            "fraud": "N/A"
                        }
                    else:
                        new_row = {
                            **row,
                            "fraud": response.text
                        }

                print("Name: " + row["name"])
                print("Fraud: " + new_row["fraud"])

                writer.writerow(new_row)

run()
