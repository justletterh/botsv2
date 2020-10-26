#!/bin/bash
echo "{\"bot_token\": \"$DISCORD_TOKEN\",\"owner_token\": \"$HTOKE\",\"pluralkit_api_token\": \"$PK\",\"prefix\": \"lgs.\",\"owners\": [\"$HID\"]}">/app/config.json
cd /app;node /app/index.js