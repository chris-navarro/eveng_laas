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

def stop_nodes(*args):

    # login authentication
    login_url = 'http://192.168.0.15/api/auth/login'

    creds = hidden.secret
    headers = {'Accept': 'application/json'}
    login = requests.post(url=login_url, data=creds)
    cookies = login.cookies

    #print(cookies)
    for node_id in args:

        # Shutting Down the Nodes
        node_url = f"http://192.168.0.15/api/labs/{folder}/{topology}.unl/nodes/{node_id}/stop"
        stop_node_api = requests.get(url=node_url, cookies=cookies, headers=headers)
        response = stop_node_api.json()
        print(f"Shutting Down Node/s {node_id}.")
        #print(response)

folder = input("Enter the Virtual Lab Folder: ")
topology = input("Enter the Virtual Lab Topology: ")

stop_node_instance = (input("Enter the Node ID/s to be Shutdown(e.i. 1,2,3): ").split(","))
stop_nodes(*stop_node_instance)        