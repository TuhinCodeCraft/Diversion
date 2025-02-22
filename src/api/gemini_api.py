import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_response_from_gemini(prompt):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        # Pass the API key as a query parameter
        url_with_key = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        response = requests.post(url_with_key, json=payload, headers=headers)

        # Print the full JSON response to see its structure
        print("Raw Response:", response.json())

        if response.status_code == 200:
            # Check the entire response structure
            json_data = response.json()
            return json_data  # Return the whole response for now
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process the request."

# Example usage
prompt = "Explain how AI works"
response = get_response_from_gemini(prompt)
print("Gemini Response:", response)
