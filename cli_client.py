"""
CLI-Based client for testing purposes
"""

import sys
import os
import time
import requests

"""Address of the API"""
address = 'http://localhost:5000/api'

"""Command Line Interface Loop, that allows the user to ask for an object, or to quit"""
while True:
    command = input('Enter a command (get, quit): ')
    if command == 'quit':
        sys.exit(0)
    elif command == 'get':
        response = requests.post(address)
        if response.status_code == 200:
            if 'object' in response.json():
                print('Object: {}'.format(response.json()['object']))
            elif 'time_left' in response.json():
                print('Time left: {}'.format(response.json()['time_left']))
            elif 'error' in response.json():
                print('{}'.format(response.json()['error']))
            else:
                print('Invalid response')
        else:
            print('Invalid response')
    else:
        print('Invalid command')
