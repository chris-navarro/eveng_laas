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

# login authentication
login_url = 'http://192.168.0.15/api/auth/login'

creds = '{"username": "admin","password": "eve","html5": "-1"}'

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

# print(cookies)

# adding a new user
def create_user():
    #global user
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

    if user_api_response['status'] == 'success':
        print("New User and POD ID has been created.")
    else:
        print(f"Failed in creating a new user. {user_api_response['message']}")
    #print(user_api_response)
create_user()

logout_url = 'http://192.168.0.15/api/auth/logout'
login = requests.get(url=logout_url, data=creds)
print("User has logout Successfully.")