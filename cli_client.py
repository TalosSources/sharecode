"""
CLI-Based client for testing purposes
"""

import sys
import os
import time
import requests

"""Address of the API"""
address = 'http://localhost:5000'

"""Command Line Interface Loop, that allows the user to ask for an object, or to quit"""
while True:
    command = input('Enter a command (status, get, quit): ')

    if command == 'quit':
        sys.exit(0)

    elif command == 'status':
        response = requests.get(address + '/getStatus')
        if response.status_code == 200:
            if 'status' in response.json():
                print('Status: {}'.format(response.json()['status']))
                match response.json()['status']:
                    case 'waiting':
                        print(' Time left: {}'.format(response.json()['time_left']))
                    case 'unavailable':
                        print(' No object available for today :(')
                    case 'available':
                        print(' An object is available ! Use the "get" command to get it.')
                    case _:
                        print('Invalid response')
            else:
                print('Invalid response')

    elif command == 'get':
        response = requests.post(address + '/getObject')
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
