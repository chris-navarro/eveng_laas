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

# login authentication
login_url = 'http://192.168.0.15/api/auth/login'
creds = '{"username": "admin","password": "eve","html5": "-1"}'

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

print(cookies)

# adding a new user
user_data = {
                "username": "devuser",
                "name":"chris Navarro",
                "email":"cn02945@citi.com",
                "password":"eve",
                "role":"admin",
                "expiration":"-1",
                "pod":8,
                "pexpiration":"-1"
            }

user_data = json.dumps(user_data)

create_user_url = 'http://192.168.0.15/api/users'

create_user_api = requests.post(url=create_user_url, data=user_data, cookies=cookies, headers=headers)
user_api_response = create_user_api.json()

# if user_api_response['status'] == 'success':
#     print("New User has been created.")
# else:
#     print("Failed in creating new user.")
print(user_api_response)

# adding a new folder for the virtual lab
new_folder = {
                "path": "/",
                "name": "dev_folder"
            }
new_folder = json.dumps(new_folder)

create_folder_url = 'http://192.168.0.15/api/folders'

create_folder_api = requests.post(url=create_folder_url, data=new_folder, cookies=cookies, headers=headers)
folder_api_response = create_folder_api.json()

# if folder_api_response['status'] == 'success':
#     print("New Folder has been created.")
# else:
#     print("Failed in creating New Folder.")

print(folder_api_response)

# Adding a new virtual network topology
new_topology = {
                "path": "/dev_folder",
                "name": "sample_network",
                "version": "1",
                "author": "cn02945",
                "description": "A new demo lab",
                "body": "Lab usage and guide"
                }

new_topology = json.dumps(new_topology)

create_topology_url = 'http://192.168.0.15/api/labs'

create_topology_api = requests.post(url=create_topology_url, data=new_topology, cookies=cookies, headers=headers)
topology_api_response = create_topology_api.json()

# if topology_api_response['status'] == 'success':
#     print("New Topology has been created.")
# else:
#     print("Failed in creating New Topology.")
print(topology_api_response)

# Adding a Network Cloud
new_network_cloud = {
                "count": "1",
                "visibility": "1",
                "name": "Net0",
                "type": "pnet0",
                "left": "750",
                "top": "173",
                "postfix": 0
            }
new_network_cloud = json.dumps(new_network_cloud)
create_network_url = 'http://192.168.0.15/api/labs/dev_folder/sample_network.unl/networks'
create_network_api = requests.post(url=create_network_url, data=new_network_cloud, cookies=cookies, headers=headers)
network_api_response = create_network_api.json()
# net_id = network_api_response["data"]["id"]
# print(f"Total Created Network is: {net_id}")
print(network_api_response)


# def create_node_instance(total):

#     for i in range(1,total+1):
        # adding a new node
new_node = {
            "template": "vios",
            "type": "qemu",
            "count": "1",
            "image": "vios-159-m3",
            "name": "vIOS-Router",
            "icon": "Router.png",
            "uuid": "",
            "cpulimit": "undefined",
            "cpu": "1",
            "ram": "1024",
            "ethernet": "4",
            "qemu_version": "",
            "qemu_arch": "",
            "qemu_nic": "",
            "qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -nodefaults -rtc base=utc -cpu host",
            "ro_qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -nodefaults -rtc base=utc -cpu host",
            "config": "0",
            "delay": "0",
            "console": "telnet",
            "left": "734",
            "top": "500",
            "postfix": 0,
            }

new_node = json.dumps(new_node)

create_node_url = 'http://192.168.0.15/api/labs/dev_folder/sample_network.unl/nodes'

create_node_api = requests.post(url=create_node_url, data=new_node, cookies=cookies, headers=headers)
node_api_response = create_node_api.json()
# node_id = node_api_response["data"]["id"]
# print(f" New Created Node ID is: {node_id}")
print(node_api_response)

print("Connecting the interfaces to the network cloud")
create_intf_url = 'http://192.168.0.15/api/labs/dev_folder/sample_network.unl/nodes/1/interfaces'
intf_mapping = '{"0": "1"}'
intf_api = requests.put(url=create_intf_url, data=intf_mapping, cookies=cookies, headers=headers)
intf_api_response = intf_api.json()
print(intf_api_response)

print("Starting the Node...")
node_url = 'http://192.168.0.15/api/labs/dev_folder/sample_network.unl/nodes/1/start'
start_node_api = requests.get(url=node_url, cookies=cookies, headers=headers)
response = start_node_api.json()
print(response)

# total_node_instance = int(input("Enter the Total Node Instances Required: "))
# create_node_instance(total_node_instance)