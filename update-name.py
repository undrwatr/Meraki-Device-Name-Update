#!/usr/bin/python

#Script to rename the devices in a site based on the network name. This was done to make better use of the up/down API for monitoring.

#imports
import requests
import json
import sys
import time

#Import the CRED module from a separate directory
import cred

#custom variables for the program imported from the cred.py file located in the same directory
organization = cred.organization
key = cred.key
hub = cred.hub

#Main URL for the Meraki Platform
dashboard = "https://dashboard.meraki.com/api/v0"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

#pull back the network id and s/n of devices for a network
get_networks_url = dashboard + '/organizations/%s/networks' % organization
get_networks_response = requests.get(get_networks_url, headers=headers)
get_networks_json = get_networks_response.json()

for network_id in get_networks_json:
    get_device_sn_url = dashboard + '/networks/%s/devices' % network_id["id"]
    get_device_sn_response = requests.get(get_device_sn_url, headers=headers)
    get_device_sn_json = get_device_sn_response.json()
    for device_sn in get_device_sn_json:
        #Sites I don't want to rename, so that this script can be reused without affecting the names of devices I don't want touched.
        if network_id["name"] == "CA-HQ" or network_id["name"] == "TNDC":
            continue
        else:
            time.sleep(2)
            update_device_url = dashboard + '/networks/%s/devices/%s' % (network_id["id"], device_sn["serial"])
            UPDATE_DEVICE = {}
            UPDATE_DEVICE["name"] = network_id["name"]
            update_device_url_response = requests.put(update_device_url, data=json.dumps(UPDATE_DEVICE), headers=headers)
            print(str(network_id["name"]) + " changed")