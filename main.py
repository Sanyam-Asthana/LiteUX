import json
import requests
import os
from colorama import Fore
API_KEY = os.getenv("API_KEY")

def generate_text_from_gemini(prompt: str, model_name: str = "gemini-2.5-pro") -> str:

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if result.get("candidates") and len(result["candidates"]) > 0 and \
           result["candidates"][0].get("content") and \``
           result["candidates"][0]["content"].get("parts") and \
           len(result["candidates"][0]["content"]["parts"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("Error: Unexpected response structure or no content found.")
            print(f"Full response: {result}")
            return "Error: Could not generate text."

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return f"Error: Failed to connect to Gemini API. {e}"
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return f"Error: Invalid JSON response from API. {e}"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

def generate_structured_response_from_gemini(
    prompt: str,
    response_schema: dict,
    model_name: str = "gemini-2.5-pro"
) -> dict:
    """
    Generates a structured response using the Gemini API with a specified JSON schema.

    Args:
        prompt (str): The text prompt to send to the model.
        response_schema (dict): A dictionary defining the JSON schema for the desired response.
        model_name (str): The name of the Gemini model to use (default: "gemini-2.0-flash").

    Returns:
        dict: The parsed JSON response from the AI, or an empty dictionary on error.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()

        if result.get("candidates") and len(result["candidates"]) > 0 and \
           result["candidates"][0].get("content") and \
           result["candidates"][0]["content"].get("parts") and \
           len(result["candidates"][0]["content"]["parts"]) > 0:
            json_string = result["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(json_string)
        else:
            print("Error: Unexpected response structure or no content found for structured response.")
            print(f"Full response: {result}")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response for structured data: {e}")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred during structured response generation: {e}")
        return {}

if __name__ == "__main__":
    print(f"{Fore.BLUE}Write your prompt:")
    text_prompt = """
    You are an expert UI/UX Designer and a full-stack web-developer


Analyze the following prompt about an interactive UI/UX design idea and create the design using only HTML canvas. All the elements mentioned in the design idea should be SVGs which are a part of the HTML Canvas. All the elements such as buttons, text-boxes etc. should be interact-able! Try to make give the design a modern look. No actual HTML code may be written except the canvas and its elements. Remember to only respond with the HTML code and nothing else. \n
    """ + input()
    print(f"{Fore.RED}Your prompt has been sent, please wait for the response...")
    ai_response = generate_text_from_gemini(text_prompt)
    print(f"{Fore.BLUE}AI Response:\n {Fore.BLACK}{ai_response}\n")
    print(f"{Fore.BLUE}Save this to a file? (Y/N)")
    c = input().lower()
    if c=="y":
        x = input("Enter filename: ")
        with open(x, "w") as f:
            s = ai_response.split("\n")
            for i in range(len(s)):
                s[i] = s[i] + "\n"
            f.writelines(s[1:-2])

