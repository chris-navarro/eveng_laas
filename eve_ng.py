#! /usr/bin/python3

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

# login authentication
login_url = 'http://192.168.0.15/api/auth/login'

creds = hidden.secret

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

#print(cookies)

# adding a new folder for the virtual lab
def create_folder():
    global folder
    folder = input("Enter Folder Name: ")

    new_folder = {
                    "path": "/",
                    "name": f"{folder}"
                }
    new_folder = json.dumps(new_folder)

    create_folder_url = 'http://192.168.0.15/api/folders'

    create_folder_api = requests.post(url=create_folder_url, data=new_folder, cookies=cookies, headers=headers)
    folder_api_response = create_folder_api.json()

    if folder_api_response['status'] == 'success':
        print("New Folder has been created.")
    else:
        print("Failed in creating New Folder.")

    #print(folder_api_response)
create_folder()

# Adding a new virtual network topology
def create_topology():
    global topology
    topology = input("Enter Topology Name: ")

    new_topology = {
                    "path": f"/{folder}",
                    "name": f"{topology}",
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
        print("New Topology has been created.")
    else:
        print("Failed in creating New Topology.")
    #print(topology_api_response)
create_topology()

# Adding a network
def create_network_cloud():
    global cloud_name
    global network_id
    #for i in range(0,id+1):
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
    create_network_url = f'http://192.168.0.15/api/labs/{folder}/{topology}.unl/networks'
    create_network_api = requests.post(url=create_network_url, data=new_network_cloud, cookies=cookies, headers=headers)
    network_api_response = create_network_api.json()
    #print(network_api_response)
    net_id = network_api_response["data"]["id"]
    print(f" Successfully Created Network Cloud ID: {net_id}")

network_id = int(input("Enter the Network Cloud ID (e.i. 1,2,3...9): "))
cloud_name = network_id - 1
create_network_cloud()

def create_node_instance(total):

    for i in range(1, total+1):
        # adding a new node
        global node_id
        new_node = {
                        "template": "veos",
                        "type": "qemu",
                        "count": "1",
                        "image": "veos-4.27.0F",
                        "name": f"rnrelab-lea{i}-vEOS",
                        "icon": "AristaSW.png",
                        "uuid": "",
                        "cpulimit": "undefined",
                        "cpu": "1",
                        "ram": "2048",
                        "ethernet": "9",
                        "qemu_version": "",
                        "qemu_arch": "",
                        "qemu_nic": "",
                        "qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -display none -no-user-config -rtc base=utc -boot order=d",
                        "ro_qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -display none -no-user-config -rtc base=utc -boot order=d",
                        "config": "0",
                        "delay": "0",
                        "console": "telnet",
                        "left": int("100") + i * 250,
                        "top": "500",
                        "postfix": 1,
                    }

        new_node = json.dumps(new_node)

        create_node_url = f'http://192.168.0.15/api/labs/{folder}/{topology}.unl/nodes'

        create_node_api = requests.post(url=create_node_url, data=new_node, cookies=cookies, headers=headers)
        node_api_response = create_node_api.json()
        node_id = node_api_response["data"]["id"]
        print(f" New Created Node ID: {node_id}")
        # print(node_api_response)

        print("Connecting the interface/s to the Network Cloud")
        create_intf_url = f'http://192.168.0.15/api/labs/{folder}/{topology}.unl/nodes/{node_id}/interfaces'

        if cloud_name == 0:
            intf_cloud_net_id = network_id
        else:
             intf_cloud_net_id = network_id - 1

        # intf_mapping_ios =
        # intf_mapping_nxos =
        intf_mapping_eos = {"1": f"{intf_cloud_net_id}"}
        intf_mapping_eos = json.dumps(intf_mapping_eos)
        # print(intf_mapping_eos)
        intf_api = requests.put(url=create_intf_url, data=intf_mapping_eos, cookies=cookies, headers=headers)
        intf_api_response = intf_api.json()
        #print(intf_api_response)

        # Adding an interswitch Connection 
        # Adding a network bridge for interswitch connection

        new_bridge = {
                    "visibility": 0
                 }
        new_bridge = json.dumps(new_bridge)

        new_net_count = node_id + 1
        # print(new_net_count)
        p2p_net_url = f'http://192.168.0.15/api/labs/{folder}/{topology}.unl/networks/{new_net_count}'
        p2p_net_api = requests.put(url=p2p_net_url, data=new_bridge, cookies=cookies, headers=headers)
        p2pnet_api_res = p2p_net_api.json()
        print(p2pnet_api_res)

        intersw_node_url = f'http://192.168.0.15/api/labs/{folder}/{topology}.unl/nodes/{node_id}/interfaces'
        # print(intersw_node1_url)

        # Increment the assigned interface connecting the Cloud Network for Interswitch Connection
        if intf_cloud_net_id == 1:
            intersw_id = intf_cloud_net_id + 1
        else:
            Print("Interface not found!")

        intfsw_node_mapping_eos = {"2":int(f"{intersw_id}")}
        # print(intfsw_node_mapping_eos)
        intfsw_node_mapping_eos = json.dumps(intfsw_node_mapping_eos)
        create_intfsw_api = requests.put(url=intersw_node_url, data=intfsw_node_mapping_eos, cookies=cookies, headers=headers)
        intfsw_api_response = create_intfsw_api.json()
        print(f"Interswitch port/s for node{node_id}: Ethernet{intersw_id}") 
        
         #Starting the Node/s
        node_url = f'http://192.168.0.15/api/labs/{folder}/{topology}.unl/nodes/{node_id}/start'
        start_node_api = requests.get(url=node_url, cookies=cookies, headers=headers)
        response = start_node_api.json()
        print(f"Node ID {node_id} Started.")
        # print(response)

total_node_instance = int(input("Enter the Total Node Instances Required: "))
create_node_instance(total_node_instance)


    