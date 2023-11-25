import requests
from requests.auth import HTTPBasicAuth

# The provided URL
url = "http://5.182.26.180:55565/telegram/hs/hl/gd"

# The GET parameters to send with the request
params = {
    'type': 'phone',
    'chat_id': 901569590,
    'phone_number': '+998933411945'
}

# Headers to send with the request
headers = {
    'Authorization': 'Basic SElMT0w6MHV0MGZiMHVuRA==',
    'User-Agent': 'PostmanRuntime/7.35.0',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

try:
    # Perform the GET request with the specified headers and Basic Authentication
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful
    if response.ok:
        # Attempt to print the JSON if the content type is correct
        if 'application/json' in response.headers.get('Content-Type', ''):
            print(response.json())
            result = response.text
        else:
            result = f"Response is not in JSON format: {response.text}"
    else:
        # Handle request error
        result = f"Request failed with status code {response.status_code}: {response.reason}"

except requests.exceptions.RequestException as e:
    # A serious problem happened, like an SSLError or InvalidURL
    result = f"Request failed: {e}"

print(result)