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
import folder
import lab
import cloud

# login authentication
login_url = 'http://192.168.0.15/api/auth/login'

creds = hidden.secret
# print(creds)

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

# print(cookies)

def create_node_instance(total):

    for i in range(1, total+1):
        # adding a new node
        global node_id
        if hidden.platform == "eos":
            eos = {
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

            eos = json.dumps(eos)

            create_node_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/nodes'
            create_node_api = requests.post(url=create_node_url, data=eos, cookies=cookies, headers=headers)
            node_api_response = create_node_api.json()
            node_id = node_api_response["data"]["id"]
            #print(node_api_response)
            print(f"New Created Node ID: {node_id}")
            print("Connecting the interface/s to the Network Cloud")

            create_intf_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/nodes/{node_id}/interfaces'

            # interface mapping
            if cloud.cloud_name == 0:
                intf_cloud_net_id = cloud.network_id
            else:
                intf_cloud_net_id = cloud.network_id - 1

            intf_mapping_eos = {"1": f"{intf_cloud_net_id}"}
            intf_mapping_eos = json.dumps(intf_mapping_eos)
            # print(intf_mapping_eos)
            intf_api = requests.put(url=create_intf_url, data=intf_mapping_eos, cookies=cookies, headers=headers)
            intf_api_response = intf_api.json()
            #print(intf_api_response)

            # Adding an interswitch Connection 
            # Adding a network bridge for interswitch connection
            net_num = 1 + cloud.network_id

            P2P_intf = {
                            "count": 1,
                            "name": f"Net-vEOS1iface_{net_num}",
                            "type": "bridge",
                            #"left": 650,
                            #"top": 350,
                            "visibility": 1,
                            "postfix": 0
                    }
            P2P_intf = json.dumps(P2P_intf)
            net_p2p_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/networks'
            net_p2p_api = requests.post(url=net_p2p_url, data=P2P_intf, cookies=cookies, headers=headers)
            net_api_response = net_p2p_api.json()

            # P2P Interswitch Connection
            intersw_node_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/nodes/{node_id}/interfaces'
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
            
            new_bridge = {
                            "visibility": 0
                        }
            new_bridge = json.dumps(new_bridge)

            new_net_count = node_id + 1

            p2p_net_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/networks/{new_net_count}'
            p2p_net_api = requests.put(url=p2p_net_url, data=new_bridge, cookies=cookies, headers=headers)
            p2pnet_api_res = p2p_net_api.json()
            # print(p2pnet_api_res)
            print("P2P Connection has been connected!")

        elif hidden.platform == "nxos":
            nxos = {
                            "template": "nxosv9k",
                            "type": "qemu",
                            "count": "1",
                            "image": "nxosv9k-9500",
                            "name": f"rnrelab-lea{i}-nxos",
                            "icon": "Nexus7K.png",
                            "uuid": "",
                            "cpulimit": "undefined",
                            "cpu": "2",
                            "ram": "8192",
                            "ethernet": "8",
                            "qemu_version": "",
                            "qemu_arch": "",
                            "qemu_nic": "",
                            "qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -enable-kvm",
                            "ro_qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -enable-kvm",
                            "config": "0",
                            "delay": "0",
                            "console": "telnet",
                            "left": int("100") + i * 250,
                            "top": "403",
                            "postfix": 0
                        }
            nxos = json.dumps(nxos)
            create_node_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/nodes'
            create_node_api = requests.post(url=create_node_url, data=nxos, cookies=cookies, headers=headers)
            node_api_response = create_node_api.json()
            node_id = node_api_response["data"]["id"]
            # print(node_api_response)
            print(f"New Created Node ID: {node_id}")
            print("Connecting the interface/s to the Network Cloud")

            create_intf_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/nodes/{node_id}/interfaces'

            # interface mapping
            if cloud.cloud_name == 0:
                intf_cloud_net_id = cloud.network_id
            else:
                intf_cloud_net_id = cloud.network_id - 1
            # print(intf_cloud_net_id)
            intf_mapping_nxos = {"1":f"{intf_cloud_net_id}"}
            intf_mapping_nxos = json.dumps(intf_mapping_nxos)
            intf_api = requests.put(url=create_intf_url, data=intf_mapping_nxos, cookies=cookies, headers=headers)
            intf_api_response = intf_api.json()
            # print(intf_mapping_nxos)

            net_num = 1 + cloud.network_id

            P2P_intf = {
                            "count": 1,
                            "name": f"Net-NXOSiface_{net_num}",
                            "type": "bridge",
                            # "left": 741,
                            # "top": 469,
                            "visibility": 1,
                            "postfix": 0
                    }
            P2P_intf = json.dumps(P2P_intf)
            net_p2p_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/networks'
            net_p2p_api = requests.post(url=net_p2p_url, data=P2P_intf, cookies=cookies, headers=headers)
            net_api_response = net_p2p_api.json()
            
            # P2P Interswitch Connection
            intersw_node_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/nodes/{node_id}/interfaces'
            # print(intersw_node1_url)

            # Increment the assigned interface connecting the Cloud Network for Interswitch Connection
            if intf_cloud_net_id == 1:
                intersw_id = intf_cloud_net_id + 1
            else:
                Print("Interface not found!")

            intfsw_node_mapping_nxos = {"2":int(f"{intersw_id}")}
            # print(intfsw_node_mapping_eos)
            intfsw_node_mapping_nxos = json.dumps(intfsw_node_mapping_nxos)
            create_intfsw_api = requests.put(url=intersw_node_url, data=intfsw_node_mapping_nxos, cookies=cookies, headers=headers)
            intfsw_api_response = create_intfsw_api.json()
            print(f"Interswitch port/s for node{node_id}: Ethernet{intersw_id}") 
            

            new_bridge = {
                            "visibility": 0
                        }
            new_bridge = json.dumps(new_bridge)

            new_net_count = node_id + 1

            p2p_net_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/networks/{new_net_count}'
            p2p_net_api = requests.put(url=p2p_net_url, data=new_bridge, cookies=cookies, headers=headers)
            p2pnet_api_res = p2p_net_api.json()
            # print(p2pnet_api_res)
            print("P2P Connection has been connected!")

        iosl3 = {
                        "template": "vios",
                        "type": "qemu",
                        "count": "1",
                        "image": "vios-159-m3",
                        "name": f"rnrelab-wan{i}-vIOS",
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
                        "left": int("100") + i * 250,
                        "top": "396",
                        "postfix": 0    
                    }
        iosl3 = json.dumps(iosl3)

        iosl2 = {
                        "template": "viosl2",
                        "type": "qemu",
                        "count": "1",
                        "image": "viosl2-2020",
                        "name": f"anrelab-acc{i}-vEOS",
                        "icon": "Switch L3.png",
                        "uuid": "",
                        "cpulimit": "undefined",
                        "cpu": "1",
                        "ram": "1024",
                        "ethernet": "8",
                        "qemu_version": "",
                        "qemu_arch": "",
                        "qemu_nic": "",
                        "qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -nodefaults -rtc base=utc -cpu host",
                        "ro_qemu_options": "-machine type=pc,accel=kvm -serial mon:stdio -nographic -no-user-config -nodefaults -rtc base=utc -cpu host",
                        "config": "0",
                        "delay": "0",
                        "console": "telnet",
                        "left": int("100") + i * 250,
                        "top": "374",
                        "postfix": 0 
                    }
        iosl2 = json.dumps(iosl2)

        #Starting the Node/s
        node_url = f'http://192.168.0.15/api/labs/{folder.folders}/{lab.labs}.unl/nodes/{node_id}/start'
        start_node_api = requests.get(url=node_url, cookies=cookies, headers=headers)
        response = start_node_api.json()
        print(f"Node ID {node_id} Started.")
        # print(response)
total_node_instance = int(input("Enter the Total Node Instances Required: "))
create_node_instance(total_node_instance)


    