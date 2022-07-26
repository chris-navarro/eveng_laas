#! /usr/bin/python3

# Copyright (c) 2022, chris.navarro
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# Version 1.0, written 07-21-2022 by
# ejnavarro@gmail.com

import json
import requests
# import hidden

# login authentication
login_url = 'http://192.168.0.15/api/auth/login'

creds = '{"username": "admin","password": "eve","html5": "-1"}'

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

# print(cookies)

# adding a new user
def create_user():

    global user
    global pod_id
    user = input("Enter a Username(e.i. SOEID): ")
    pod_id = int(input("Enter POD ID (e.i. 1, 2, 3): "))

    user_data = {
                    "username":f"{user}",
                    "name":f"{user}",
                    "email":f"{user}@citi.com",
                    "password":"eve",
                    "role":"admin",
                    "expiration":"-1",
                    "pod":f"{pod_id}",
                    "pexpiration":"-1"
                }

    user_data = json.dumps(user_data)

    create_user_url = 'http://192.168.0.15/api/users'

    create_user_api = requests.post(url=create_user_url, data=user_data, cookies=cookies, headers=headers)
    user_api_response = create_user_api.json()
    #print(user_api_response)
    if user_api_response['status'] == 'success':
        print(f"New user {user} and POD ID {pod_id} has been created successfully.")
    elif user_api_response['code'] == 500:
        print(f"Failed in creating a new user. {user_api_response['message']}")
    else:
        print(f"Failed in creating a new user. {user_api_response['message']}")
        del_user_url = f'http://192.168.0.15/api/users/{user}'
        create_user_api = requests.delete(url=del_user_url,cookies=cookies, headers=headers)
        user_api_response = create_user_api.json()
        #print(user_api_response)
        print("Cleaning the Database.")
create_user()

logout_url = 'http://192.168.0.15/api/auth/logout'
login = requests.get(url=logout_url, data=creds)
