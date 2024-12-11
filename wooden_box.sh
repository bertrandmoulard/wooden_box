#!/bin/bash

# Get the directory of the script
SCRIPT_DIR=$(dirname "$0")

# Load the access token from access_token.txt
ACCESS_TOKEN=$(cat "$SCRIPT_DIR/access_token.txt")

# Spotify API Base URL
BASE_URL="https://api.spotify.com/v1/me/player"

# Function to send a request to the Spotify API
send_request() {
    local method=$1
    local endpoint=$2
    local data=$3

    curl -s -X "$method" "$BASE_URL/$endpoint" \
         -H "Authorization: Bearer $ACCESS_TOKEN" \
         -H "Content-Type: application/json" \
         -d "$data"
}

# Functions for playback control
play_uri() {
    local uri=$1
    send_request "PUT" "play" "{\"context_uri\": \"$uri\"}"
}

resume_playback() {
    send_request "PUT" "play"
}

pause_playback() {
    send_request "PUT" "pause"
}

previous_track() {
    send_request "POST" "previous"
}

next_track() {
    send_request "POST" "next"
}

# Main logic to handle commands
case $1 in
    play)
        if [ -n "$2" ]; then
            play_uri "$2"
        else
            resume_playback
        fi
        ;;
    pause)
        pause_playback
        ;;
    previous)
        previous_track
        ;;
    next)
        next_track
        ;;
    *)
        echo "Usage: $0 {play <spotify_uri>|play|pause|previous|next}"
        ;;
esac
