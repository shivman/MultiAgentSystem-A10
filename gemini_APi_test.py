import os
import requests

# Set your API key here
API_KEY = "AIzaSyABDclvruKv9LD35fv52SD-RC6wG61Of8Y"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Example prompt
prompt = "Write a short poem about AI and nature."

# Make request
response = requests.post(
    f"{BASE_URL}?key={API_KEY}",
    headers={"Content-Type": "application/json"},
    json={
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    },
)

if response.status_code == 200:
    result = response.json()
    print("Gemini Response:")
    print(result["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Error:", response.status_code, response.text)
