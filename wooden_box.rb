require 'net/http'
require 'json'

# Get the directory of the script
SCRIPT_DIR = File.dirname(__FILE__)

# Load the access token from access_token.txt
ACCESS_TOKEN = File.read(File.join(SCRIPT_DIR, 'access_token.txt')).strip

# Spotify API Base URL
BASE_URL = 'https://api.spotify.com/v1/me/player'

# Function to send a request to the Spotify API
def send_request(method, endpoint, data = nil)
  uri = URI("#{BASE_URL}/#{endpoint}")
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true

  request = case method.upcase
            when 'PUT' then Net::HTTP::Put.new(uri)
            when 'POST' then Net::HTTP::Post.new(uri)
            when 'GET' then Net::HTTP::Get.new(uri)
            else raise ArgumentError, "Unsupported HTTP method: #{method}"
            end

  request['Authorization'] = "Bearer #{ACCESS_TOKEN}"
  request['Content-Type'] = 'application/json'
  request.body = data.to_json if data

  response = http.request(request)

  puts "Executing: #{method} #{uri}"
  puts "Response: #{response.code} #{response.body}" unless response.body.nil?

  response
end

# Function to list available devices
def list_devices
  response = send_request('GET', 'devices')
  devices = JSON.parse(response.body)['devices']
  puts "Devices: #{devices}" if devices.any?
  devices
end

# Function to activate a specific device by name
def activate_device(device_name)
  devices = list_devices
  target_device = devices.find { |device| device['name'] == device_name }

  if target_device.nil?
    puts "Device '#{device_name}' not found. Ensure the device is online and connected to Spotify."
    exit(1)
  end

  device_id = target_device['id']

  # Activate the device
  response = send_request('PUT', '', { device_ids: [device_id], play: false })
  if response.code.to_i == 204
    puts "Device '#{device_name}' activated successfully."
  else
    puts "Failed to activate device '#{device_name}'."
    exit(1)
  end

  device_id
end

# Functions for playback control
def play_uri(uri)
  activate_device("Bertie's RaspeberryPI")
  send_request('PUT', 'play', { context_uri: uri })
end

def resume_playback
  activate_device("Bertie's RaspeberryPI")
  send_request('PUT', 'play')
end

def pause_playback
  activate_device("Bertie's RaspeberryPI")
  send_request('PUT', 'pause')
end

def previous_track
  activate_device("Bertie's RaspeberryPI")
  send_request('POST', 'previous')
end

def next_track
  activate_device("Bertie's RaspeberryPI")
  send_request('POST', 'next')
end

# Main logic to handle commands
def main
  command = ARGV[0]
  argument = ARGV[1]

  case command
  when 'play'
    if argument
      play_uri(argument)
    else
      resume_playback
    end
  when 'pause'
    pause_playback
  when 'previous'
    previous_track
  when 'next'
    next_track
  else
    puts 'Usage: ruby spotify_control.rb {play <spotify_uri>|play|pause|previous|next}'
  end
end

main if __FILE__ == $PROGRAM_NAME
