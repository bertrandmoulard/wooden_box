#!/bin/bash

# Get the directory of the script
SCRIPT_DIR=$(dirname "$0")

# Load credentials from credentials.txt in the script's directory
source "$SCRIPT_DIR/credentials.txt"

# Spotify Token URL
TOKEN_URL="https://accounts.spotify.com/api/token"

# Generate base64-encoded credentials
BASIC_AUTH=$(echo -n "$CLIENT_ID:$CLIENT_SECRET" | base64)

# Request a new access token
RESPONSE=$(curl -s -X POST -H "Content-Type: application/x-www-form-urlencoded" \
     -H "Authorization: Basic $BASIC_AUTH" \
     -d "grant_type=refresh_token" \
     -d "refresh_token=$REFRESH_TOKEN" \
     $TOKEN_URL)

# Extract the new access token
ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access_token')

# Check if the response contains a valid token
if [ "$ACCESS_TOKEN" != "null" ]; then
    echo "$ACCESS_TOKEN" > "$SCRIPT_DIR/access_token.txt"
    echo "Token refreshed successfully: $ACCESS_TOKEN"
else
    echo "Failed to refresh token: $RESPONSE"
fi
