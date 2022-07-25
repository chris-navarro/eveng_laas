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
import hidden
# from eve_ng import create_node_instance

def start_node(*args):

    # login authentication
    login_url = 'http://192.168.0.15/api/auth/login'

    creds = hidden.secret
    headers = {'Accept': 'application/json'}
    login = requests.post(url=login_url, data=creds)
    cookies = login.cookies
    #print(cookies)

    for node_id in args:

        # Starting the Nodes
        node_url = f"http://192.168.0.15/api/labs/{folder}/{topology}.unl/nodes/{node_id}/start"
        start_node_api = requests.get(url=node_url, cookies=cookies, headers=headers)
        response = start_node_api.json()
        print(f"Starting Node/s {node_id}.")
        #print(response)

# Starting the Nodes
folder = input("Enter the Virtual Lab Folder: ")
topology = input("Enter the Virtual Lab Topology: ")
start_node_instance = (input("Enter the Node ID/s to be started (e.i. 1,2,3): ").split(","))
start_node(*start_node_instance)

   