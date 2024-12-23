import dotenv
import os
import googleapiclient.discovery
import spotipy
from spotipy.oauth2 import SpotifyOAuth
5
default_playlist_params= {
    "itemCount": True,
    "channelTitle": True,
    "address": True,
    "channel_address": True,
    "description": True,
    "publishedAt": True,
    "thumbnail": True
}
default_video_params= {
    "channelId": True,
    "channelTitle": True,
    "description": True,
    "videoPublishedAt": True,
    "thumbnail": True
}
#https://jsonviewer.stack.hu/
class Caller:
    __apiServiceName = "youtube"
    __apiVersion  = "v3"

    def __init__(self) -> None:
        dotenv.load_dotenv()
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
            nextToken = self.get_next_token(res)
            answer = answer | res
            while nextToken != None:
                res = self.youtube.playlistItems().list(
                part="contentDetails,snippet",
                pageToken=nextToken,
                playlistId=playlistID,
                maxResults="50"
                ).execute()
                nextToken = self.get_next_token(res)
                answer["items"] = answer["items"] + res["items"]
            return answer
        except Exception as e:
            print(f'Error: {e}')
            raise

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

    def make_playlist_request_without_playlist_info(self, playlistInfo: dict) -> dict:
        all_items = self.__get_all_playlist_positions(playlistInfo["id"])
        return all_items

    def get_next_token(self, response) -> str:
        token = ""
        try:
            token = response["nextPageToken"]
        except:
            token = None
        return token

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

        #redundant
    # def getAllPlaylistsData(self, address, includes):
    #     response = requests.get("view-source:"+address)

    #     if(response.status_code == 200):
    #         #<link rel="canonical" href
    #         #continue=https://www.youtube.com/channel/
    #         pos = response.text.find("<link rel=\"canonical\" href=\"https://www.youtube.com/channel/")
    #         posEnd = -1
    #         if(pos != -1):
    #             posEnd = response.text.find("\"", pos+60)
    #         if(posEnd != -1):
    #             channelID = response.text[pos:posEnd]
    #     else:
    #         #FAIL
    #         pass
    #     pass
    
    # #Types: 1 - TXT
    # def readExistingPlaylist(self, type:int, fileData: str) ->tuple:
    #     info:dict
    #     if type == 1:
    #         tFF = TextFormatFactory.TextFormatFactory()
    #         info = tFF.readHeader(fileData)
    #         if len(info) == 0:
    #             return (False,None)
    #     return (True, info)

    # def getPlaylistData(self, address, includes):
    #     playlistID = self.scrap_playlist_id(address)

    #     responses = self.make_playlist_request(playlistID)
    #     formattedData = tFF.prepareDataToBeIncluded(includes, responses[1], responses[0])
    #     return formattedData

    # #works for public playlists created by user, playlists ids can be obtained
    # def makeChannelRequest(self):
    #     res = self.youtube.playlists().list( 
    #     part="id,contentDetails,snippet",
    #    # channelId="UCXnI7wpHJ-x8bafp1BK3DUQ").execute()
    #     channelId="UC0KfUunv1cE_EL6y8-wqBFQ").execute()
    #     return res["items"]
