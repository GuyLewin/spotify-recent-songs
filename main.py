import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger(__name__)

TOP_SONG_AMOUNT = 1500
# Based on API:
CHUNK_SIZE = 100
PLAYLIST = os.environ["SPOTIFY_PLAYLIST"]
SPOTIPY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]


def add_song(item, top_songs):
    if len(top_songs) >= TOP_SONG_AMOUNT:
        return
    top_songs.append(item["track"]["id"])


def get_chunk(top_songs):
    chunk_size = min(CHUNK_SIZE, len(top_songs))
    next_chunk = top_songs[:chunk_size]
    top_songs = top_songs[chunk_size:]
    return next_chunk, top_songs


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()]
    )

    logger.info("Starting run!")
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                                      client_secret=SPOTIPY_CLIENT_SECRET,
                                                                      redirect_uri="http://127.0.0.1:5000/api_callback",
                                                                      scope="user-library-read,playlist-modify-private",
                                                                      open_browser=False))

    # Get all saved tracks
    result = spotify.current_user_saved_tracks()
    top_songs = []
    [add_song(item, top_songs) for item in result["items"]]
    logger.info(f"Fetched first batch of {len(result["items"])} songs")
    while result['next'] and len(top_songs) < TOP_SONG_AMOUNT:
        result = spotify.next(result)
        logger.info(f"Fetched next batch of {len(result["items"])} songs")
        [add_song(item, top_songs) for item in result["items"]]

    top_songs_found = len(top_songs)
    first_chunk, top_songs = get_chunk(top_songs)
    # Replace all songs with first chunk
    spotify.playlist_replace_items(PLAYLIST, first_chunk)
    logger.info(f"Replaced playlist tracks with {len(first_chunk)} songs. {len(top_songs)} songs remaining.")
    while len(top_songs) > 0:
        next_chunk, top_songs = get_chunk(top_songs)
        logger.info(f"Added {len(next_chunk)} songs to playlist. {len(top_songs)} songs remaining.")
        spotify.playlist_add_items(PLAYLIST, next_chunk)
    logger.info(f"Finished adding {top_songs_found} songs to playlist!")


if __name__ == '__main__':
    main()
