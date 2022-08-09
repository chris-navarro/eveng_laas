#! /usr/bin/python3

# Copyright (c) 2022, chris.navarro
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# Version 1.0, written 07-21-2022 by
# ejnavarro@gmail.com

import requests
import json
i#mport hidden

def del_instance(*args):

    # login authentication
    login_url = 'http://192.168.0.15/api/auth/login'

    creds = {"username": f"{user}","password": "eve","html5": "-1"}

    headers = {'Accept': 'application/json'}

    login = requests.post(url=login_url, data=creds)

    cookies = login.cookies

    print(cookies)
    

    for node_id in args:

        del_url = f'http://192.168.0.15/api/labs/{folder}/{topology}.unl/nodes/{node_id}'

        del_api = requests.delete(url=del_url, cookies=cookies, headers=headers)

        del_response = del_api.json()
        print(del_response)

        # if node_id != node_id:
        #     print(f"Failed to delete the Node ID/s {node_id}. Error code {'code'}")
        # elif del_response['code'] == 200:
        #     print(f"The Node ID/s {node_id} deleted successfully!")
        # else:
        #     print(f"Failed to delete the Node ID/s {node_id}. Error code {'code'}")
user = input("Enter the username: ")
folder = input("Enter the Folder name: ")
topology = input("Enter the Topology name: ")

del_node_instance = (input("Enter the Node ID Instance/s to be deleted (e.i. 1,2,3): ").split(','))

del_instance(*del_node_instance)
