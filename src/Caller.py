import dotenv
import os
import googleapiclient.discovery
import spotipy
from spotipy.oauth2 import SpotifyOAuth

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

#https://jsonviewer.stack.hu/
class Caller:
    __apiServiceName = "youtube"
    __apiVersion  = "v3"

    def __init__(self) -> None:
        dotenv.load_dotenv(dotenv_path)
        self.key = os.getenv('KEY')
        self.youtube = googleapiclient.discovery.build(Caller.__apiServiceName,
                                                       Caller.__apiVersion,developerKey=self.key)

    def __scrap_playlist_id(self, address:str) -> str:
        index = address.find("list=")
        index += 5
        return address[index:]

    def __get_all_playlist_positions(self, playlistID: str) -> dict:
        try:
            answer = {}
            res = self.youtube.playlistItems().list(
                part="contentDetails,snippet,id",
                playlistId=playlistID,
                maxResults="50"
                ).execute()
            nextToken = self.__get_next_token(res)
            answer = answer | res
            while nextToken != None:
                res = self.youtube.playlistItems().list(
                part="contentDetails,snippet",
                pageToken=nextToken,
                playlistId=playlistID,
                maxResults="50"
                ).execute()
                nextToken = self.__get_next_token(res)
                answer["items"] = answer["items"] + res["items"]
            return answer
        except Exception as e:
            print(f'Error: {e}')
            raise

    def __get_next_token(self, response) -> str:
        token = ""
        try:
            token = response["nextPageToken"]
        except:
            token = None
        return token

    def get_playlist_response(self, address:str) -> tuple:
        playlist_id = self.__scrap_playlist_id(address)
        return self.make_playlist_request(playlist_id)

    def make_channel_request(self, channel_id: str) -> dict:
        res = self.youtube.playlists().list( 
        part="id,contentDetails,snippet",
        channelId=channel_id).execute()
        return res["items"]

    def make_playlist_request(self, playlist_id: str) -> tuple:
        try:
            playlistInfo = self.youtube.playlists().list(
                id=playlist_id,
                part="contentDetails,snippet,id",
                maxResults="1"
                ).execute()
            all_items = self.__get_all_playlist_positions(playlist_id)
            return (playlistInfo, all_items)
        except Exception as e:
            print(f'Error: {e}')
            raise

    def create_spotify_playlist(self, playlist_name:str, playlist_description:str, songs: list):
        CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
        SCOPE = 'playlist-modify-private playlist-modify-public'

        try:
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                        client_secret=CLIENT_SECRET,
                                                        redirect_uri=REDIRECT_URI,
                                                        scope=SCOPE))
            user_id = sp.current_user()['id']

            playlist_name = playlist_name
            if len(playlist_name) > 200:
                playlist_name = playlist_name[:200]
            if len(playlist_description) > 200:
                playlist_description = playlist_description[:200]
            playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True, description=playlist_description)
            playlist_id = playlist['id']

            track_ids = []
            for song in songs:
                result = sp.search(q=song, limit=1, type='track')
                if result['tracks']['items']:
                    track_ids.append(result['tracks']['items'][0]['id'])

            for i in range(0, len(track_ids), 100):
                print(i, ' : ', str(track_ids[i:i+100]))
                sp.playlist_add_items(playlist_id, track_ids[i:i+100])

            print(f'Playlist "{playlist_name}" created successfully, with {len(track_ids)} songs added to it.')
        except Exception as e:
            print(f'Error: {e}')
            raise