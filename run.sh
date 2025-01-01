#!/bin/bash
cd <REPLACE_WITH_CHECKOUT_PATH>
source venv/bin/activate
export SPOTIFY_CLIENT_ID=<REPLACE>
export SPOTIFY_CLIENT_SECRET=<REPLACE>
export SPOTIFY_PLAYLIST=<REPLACE>
python3 main.py