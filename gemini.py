from google import genai
from google.genai import types

client = genai.Client()

grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Did the Forbes 30 under 30 winner {} be targeted by any lawsuit, suing, scandal, or controversy? Print the string \"N/A\" if not",
    config=config,
)

print(response.text)
