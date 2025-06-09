import requests
import spotipy
from dotenv import load_dotenv
import os
from spotipy.oauth2 import SpotifyOAuth
from src.plugin.base_plugin import BasePluging


class Spotify(BasePluging): 
    def __init__(self):

        load_dotenv()

        self.scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private"
        self.client_id = os.getenv("SPOTIFY_CLIENT_KEY")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET_KEY")
        self.callback = os.getenv("SPOTIFY_CALLBACK_URL")
        self.user_name = os.getenv("USERNAME")

                
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=self.scope,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri = self.callback,
            username=self.user_name           

        ))

        self.is_playing = False
    def play_song(self, songs):
        # me = self.sp.me() 
        
        smt = self.sp.start_playback(uris=[f"spotify:track:{song}" for song in songs])
        self.is_playing = True 
        print(smt)

    def pause_song(self):
        if not self.is_playing:
            self.sp.pause_playback()

    
    def get_user_playlist_tracks(self):
        user_playlists = self.sp.current_user_playlists() 
        first_playlist_id = user_playlists["items"][1]["id"]

        playlist_name_id_map = []
        for playlist in user_playlists["items"]:
            playlist_name_id_map.append({playlist["name"]: playlist["id"]})

        playlist_tracks_response = self.sp.playlist_items(first_playlist_id)
        track_items = playlist_tracks_response['items']

        track_ids = []
        for item in track_items:
            track_ids.append(item["track"]["id"])

        return track_ids, playlist_name_id_map


    def search_song(self, song):
        search = self.sp.search(song, type="track", limit=1)
        if not search: 
            print("Spotify returned none in search")
            return

        song_id = search["tracks"]['items'][0]["id"]
        return song_id

    def get_current(self):
        me = self.sp.me() 
        print(me)

    def run(self, value):
        self.play_song([self.search_song(value)])
    
    def can_run(self,value: str):
        return value == "spotify"