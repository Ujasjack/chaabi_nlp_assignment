import requests

# Replace this URL with the correct URL where your FastAPI app is running
api_url = "http://127.0.0.1:8000/ask"

# Example question to test the API
user_input = {"user_input": "give product description of garlic oil"}

try:
    # Send a POST request to the /ask endpoint
    response = requests.post(api_url, json=user_input)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the API response
        print("API Response:")
        print(response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")
