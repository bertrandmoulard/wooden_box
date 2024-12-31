import os
import requests
import sys
import json

# Get the directory of the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the access token from access_token.txt
with open(os.path.join(SCRIPT_DIR, 'access_token.txt'), 'r') as file:
    ACCESS_TOKEN = file.read().strip()

# Spotify API Base URL
BASE_URL = 'https://api.spotify.com/v1/me/player'
device_name = "Wooden Box"

# Function to send a request to the Spotify API with retry logic
def send_request(method, endpoint, data=None, attempt=1):
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = None

    try:
        if method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        print(f"Executing: {method} {url}")
        if response.text:
            print(f"Response: {response.status_code} {response.text}")

        if response.status_code >= 400 and attempt < 2:
            print(f"Error encountered. Retrying request... (Attempt {attempt + 1})")
            return send_request(method, endpoint, data, attempt + 1)

        return response
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Function to list available devices
def list_devices():
    response = send_request('GET', 'devices')
    devices = response.json().get('devices', [])
    if devices:
        print(f"Devices: {devices}")
    return devices

# Function to activate a specific device by name
def activate_device(device_name):
    devices = list_devices()
    target_device = next((device for device in devices if device['name'] == device_name), None)

    if not target_device:
        print(f"Device '{device_name}' not found. Ensure the device is online and connected to Spotify.")
        sys.exit(1)

    device_id = target_device['id']

    # Activate the device
    response = send_request('PUT', '', {"device_ids": [device_id], "play": False})
    if response.status_code == 204:
        print(f"Device '{device_name}' activated successfully.")
    else:
        print(f"Failed to activate device '{device_name}'.")
        sys.exit(1)

    return device_id

# Functions for playback control
def play_uri(uri):
    activate_device(device_name)
    send_request('PUT', 'play', {"context_uri": uri})

def resume_playback():
    send_request('PUT', 'play')

def pause_playback():
    send_request('PUT', 'pause')

def previous_track():
    send_request('POST', 'previous')

def next_track():
    send_request('POST', 'next')

# Main logic to handle commands
def main():
    if len(sys.argv) < 2:
        print('Usage: python wooden_box.py {play <spotify_uri>|play|pause|previous|next|list}')
        return

    command = sys.argv[1]
    argument = sys.argv[2] if len(sys.argv) > 2 else None

    if command == 'play':
        if argument:
            play_uri(argument)
        else:
            resume_playback()
    elif command == 'pause':
        pause_playback()
    elif command == 'previous':
        previous_track()
    elif command == 'next':
        next_track()
    elif command == 'list':
        list_devices()
    elif command == 'activate':
        activate_device(device_name)
    else:
        print('Usage: python wooden_box.py {play <spotify_uri>|play|pause|previous|next|list}')

if __name__ == '__main__':
    main()
