# Spotify Smart Playlists - Recent Songs
This utility maintains a playlist of your most recent 1500 liked songs (configurable via `TOP_SONG_AMOUNT` in `main.py`). You can change the logic in `main.py` to do alternative Smart Playlist logic.

## Setup
### 1. Spotify Development App
This codebase uses [Spotipy](https://github.com/spotipy-dev/spotipy) to interact with Spotify API. To use it, you must create a development app using the following steps:

1. Visit the [Spotify developer portal](https://developer.spotify.com/dashboard/). If you already have a Spotify account, click "Log in" and enter your username and password. Otherwise, click "Sign up" and follow the steps to create an account. After you've signed in or signed up, you should be redirected to your developer dashboard.
2. Click the "Create an App" button. Enter any name and description you'd like for your new app. Accept the terms of service and click "Create."
3. In your new app's Overview screen, click the "Edit Settings" button and scroll down to "Redirect URIs." Add "http://127.0.0.1:5000/api_callback". Hit the "Save" button at the bottom of the Settings panel to return to you App Overview screen.
4. Underneath your app name and description on the lefthand side, you'll see a "Show Client Secret" link. Click that link to reveal your Client Secret, then copy both your Client Secret and your Client ID somewhere on your computer. You'll need to access them later.

### 2. Creating a Spotify Playlist
1. Create a Spotify playlist (regularly).
2. On desktop - right click on your playlist, click "Share" and choose "Copy link to playlist".
3. Paste from your clipboard, you'll see a URL formatted as "https://open.spotify.com/playlist/37i9dQZF1DX7YCknf2jT6s?si=5ceb1ef28324483d". Write down the section after "playlist/" and before "?si=...", in this case - `37i9dQZF1DX7YCknf2jT6s`. This is the playlist ID.

### 3. Server Setup
1. Grab a Linux machine and checkout this repo (`git clone https://github.com/GuyLewin/spotify-recent-songs.git`).
2. Enter the checkout by running `cd spotify-recent-songs`.
3. Create a Python virtual environment named "venv" by running `python3 -m venv venv`.
4. Install the requirements by running `. ./venv/bin/activate; pip3 install -r requirements.txt`.
5. Edit `run.sh` and replace the following:
    * `<REPLACE_WITH_CHECKOUT_PATH>` - replace with the absolute directory path from the previous step. Can be retrieved by running `pwd`.
    * `<REPLACE_WITH_SPOTIFY_CLIENT_ID>` and `<REPLACE_WITH_SPOTIFY_CLIENT_SECRET>` - replace with the credentials you obtained after creating a development app.
    * `<REPLACE_WITH_SPOTIFY_PLAYLIST_ID>` - replace with the playlist ID you obtained in "2. Creating a Spotify Playlist".
6. Run the script using `./run.sh`. If all goes well - you should be getting a prompt similar to:
```
2025-01-01 15:28:51,288 [INFO] Starting run!
2025-01-01 15:28:51,289 [INFO] User authentication requires interaction with your web browser. Once you enter your credentials and give authorization, you will be redirected to a url.  Paste that url you were directed to to complete the authorization.
Go to the following URL: https://accounts.spotify.com/authorize?<redacted>
Enter the URL you were redirected to: 
```
7. Visit the URL written in the prompt and follow through the authentication flow. When it's completed, you'll be redirected to a nonexistent URL formatted as "http://127.0.0.1:5000/api_callback?code=<redacted>". It's expected for this page to not load - you only need the URL itself.
8. Copy that full URL from your browser back into your Linux terminal and press Enter. The code should now successfully populate your playlist with your recently liked songs.

### 4. (Optional) Cron Job Setup
Although the script now works, you probably want to run it periodically to keep the Smart Playlist up-to-date. To do that, you can setup a cron job to run periodically by following these steps:
1. On the same Linux machine from above, run `crontab -e`.
2. Add this line as the last line in the opened file (replace `<REPLACE_WITH_spotify-recent-songs_CHECKOUT>` with the checkout directory path):
```
0 4 * * * <REPLACE_WITH_spotify-recent-songs_CHECKOUT>/run.sh >> <REPLACE_WITH_spotify-recent-songs_CHECKOUT>/cronlogs.log 2>&1
```
This will run the utility ever day at 4am.