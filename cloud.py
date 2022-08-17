import requests
import json
import hidden
import folder
import lab

# login authentication
login_url = 'http://192.168.0.15/api/auth/login'

creds = hidden.secret
# print(creds)

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

#Adding a network
def create_network_cloud():
    global cloud_name
    global network_id
    new_network_cloud = {
                    "count": "1",
                    "visibility": "1",
                    "name": f"Net-{cloud_name}",
                    "type": f"pnet{cloud_name}",
                    "left": "750",
                    "top": "173",
                    "postfix": 0
                }
    new_network_cloud = json.dumps(new_network_cloud)
    create_network_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/networks'
    create_network_api = requests.post(url=create_network_url, data=new_network_cloud, cookies=cookies, headers=headers)
    network_api_response = create_network_api.json()
    # print(network_api_response)
    net_id = network_api_response["data"]["id"]
    print(f" Successfully Created Network Cloud ID: {net_id}")

network_id = int(input("Enter the Network cloud ID (e.i. 1,2,3...9): "))
cloud_name = network_id - 1
create_network_cloud()