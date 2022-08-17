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
# print(creds)

headers = {'Accept': 'application/json'}

login = requests.post(url=login_url, data=creds)

cookies = login.cookies

# adding a new folder for the virtual lab
def create_folder():
    global folders
    folders = input("Enter Folder Name: ")

    new_folder = {
                    "path": "/",
                    "name": f"{folders}"
                }
    new_folder = json.dumps(new_folder)

    create_folder_url = 'http://192.168.0.15/api/folders'

    create_folder_api = requests.post(url=create_folder_url, data=new_folder, cookies=cookies, headers=headers)
    folder_api_response = create_folder_api.json()

    if folder_api_response['status'] == 'success':
        print("New Folder has been created.")
    else:
        print("Failed in creating New Folder.")

    # print(folder_api_response)
create_folder()