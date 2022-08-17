# Copyright (c) 2022, chris.navarro
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# Version 1.0, written 07-22-2022 by
# ejnavarro@gmail.com

import requests
import json
import hidden
import folder

# login authentication
login_url = 'http://192.168.0.15/api/auth/login'

creds = hidden.secret
# print(creds)

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

# Adding a new virtual network topology
def create_lab():
    global labs
    labs = input("Enter Topology Name: ")

    new_topology = {
                    "path": f"/{folder.folders}",
                    "name": f"{labs}",
                    "version": "1",
                    "author": "",
                    "description": "A new demo lab",
                    "tasks": "Lab usage and guide"
                    }

    new_topology = json.dumps(new_topology)

    create_topology_url = 'http://192.168.0.15/api/labs'

    create_topology_api = requests.post(url=create_topology_url, data=new_topology, cookies=cookies, headers=headers)
    topology_api_response = create_topology_api.json()

    if topology_api_response['status'] == 'success':
        print("New Lab Topology has been created.")
    else:
        print("Failed in creating New Lab.")
    #print(topology_api_response)
create_lab()