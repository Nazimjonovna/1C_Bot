import requests

def check_python_access(server_url):
    try:
        response = requests.get(server_url, auth=(login, password), timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to access Python on the server. Status code: {response.status_code}"
    except requests.RequestException as e:
        return f"An error occurred: {str(e)}"

# Replace 'http://server_ip_or_domain/test_script.py' with the actual URL where the script is hosted
server_url = 'http://5.182.26.180:55565/telegram/hs/hl/gd'
login = 'HILOL'
password = '0ut0fb0unD'

result = check_python_access(server_url)
print(result)





# import requests
#
# def is_authenticated(address, port, login, password):
#     try:
#         api_url = f"http://{address}:{port}/telegram/hs/hl/gd"
#         response = requests.get(api_url, auth=(login, password), timeout=30)
#
#         if response.status_code == 200:
#             return True
#         else:
#             return False
#
#     except requests.RequestException as e:
#         print("Request Exception:", e)
#         return False
#
# address = '5.182.26.180'
# port = 55565
# login = 'HILOL'
# password = '0ut0fb0unD'
#
# if is_authenticated(address, port, login, password):
#     print("Authenticated successfully")
# else:
#     print("Authentication failed or endpoint is not reachable")
