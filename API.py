import json
import requests

# Your API endpoint URL
api_url = 'http://5.182.26.180:55565/telegram/hs/hl/gd'

phone_number = "+998933333349"  # message.contact.phone_number
chat_id = '901569590'  # message.from_user.id
payload = {
    "type": "phone",
    "chat_id": chat_id,
    "phone_number": phone_number
}
payload_json = json.dumps(payload)

try:
    response = requests.get(api_url, data=payload_json, headers={'Authorization':'Basic SElMT0w6MHV0MGZiMHVuRA==', 'Postman-Token':'<calculated when request is sent>','Host':'<calculated when request is sent>','User-Agent': 'PostmanRuntime/7.35.0', 'Accept':'*/*', 'Accept-Encoding':'gzip, deflate, br', 'Connection':'keep-alive'}, timeout=30)

    if response.status_code == 200:
        # Print the response content (if you expect a response)
        print("Response:", response.json())
    else:
        # If the request was unsuccessful, print the status code and reason
        print("Request unsuccessful - Status code:", response.status_code)
        print("Reason:", response.reason)

except requests.exceptions.RequestException as e:
    print("Request Exception:", e)
    print("Failed to connect to the API. Check the URL or network connection.")
