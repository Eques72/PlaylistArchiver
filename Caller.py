import dotenv
import os
import googleapiclient.discovery
import requests

# import PlaylistResponseParser
import TextFormatFactory


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

        #redundant
    def getAllPlaylistsData(self, address, includes):
        response = requests.get("view-source:"+address)

        if(response.status_code == 200):
            #<link rel="canonical" href
            #continue=https://www.youtube.com/channel/
            pos = response.text.find("<link rel=\"canonical\" href=\"https://www.youtube.com/channel/")
            posEnd = -1
            if(pos != -1):
                posEnd = response.text.find("\"", pos+60)
            if(posEnd != -1):
                channelID = response.text[pos:posEnd]
        else:
            #FAIL
            pass
        pass
    
    #Types: 1 - TXT
    def readExistingPlaylist(self, type:int, fileData: str) ->tuple:
        info:dict
        if type == 1:
            tFF = TextFormatFactory.TextFormatFactory()
            info = tFF.readHeader(fileData)
            if len(info) == 0:
                return (False,None)
        return (True, info)

    def getPlaylistData(self, address, includes):
        playlistID = self.scrapPlaylistID(address)

        responses = self.make_playlist_request(playlistID)
        formattedData = tFF.prepareDataToBeIncluded(includes, responses[1], responses[0])
        return formattedData

    def get_playlist_response(self, address:str) -> tuple:
        playlist_id = self.scrapPlaylistID(address)
        return self.make_playlist_request(playlist_id)

    def scrapPlaylistID(self, address:str) -> str:
        index = address.find("list=")
        index += 5
        return address[index:]

    #works for public playlists created by user, playlists ids can be obtained
    def makeChannelRequest(self):
        res = self.youtube.playlists().list( 
        part="id,contentDetails,snippet",
       # channelId="UCXnI7wpHJ-x8bafp1BK3DUQ").execute()
        channelId="UC0KfUunv1cE_EL6y8-wqBFQ").execute()
        return res["items"]

    def make_channel_request(self, channel_id: str) -> dict:
        res = self.youtube.playlists().list( 
        part="id,contentDetails,snippet",
        channelId=channel_id).execute()
        return res["items"]

    def get_all_playlist_positions(self, playlistID: str) -> dict:
        answer = {}
        res = self.youtube.playlistItems().list(
            part="contentDetails,snippet,id",
            playlistId=playlistID,
            maxResults="50"
            ).execute()
        nextToken = self.getNextToken(res)
        answer = answer | res
        while nextToken != None:
            res = self.youtube.playlistItems().list(
            part="contentDetails,snippet",
            pageToken=nextToken,
            playlistId=playlistID,
            maxResults="50"
            ).execute()
            nextToken = self.getNextToken(res)
            answer["items"] = answer["items"] + res["items"]
        return answer

    def make_playlist_request(self, playlist_id: str) -> tuple:
        playlistInfo = self.youtube.playlists().list(
            id=playlist_id,
            part="contentDetails,snippet,id",
            maxResults="1"
            ).execute()
        all_items = self.get_all_playlist_positions(playlist_id)
        return (playlistInfo, all_items)
    
    def make_playlist_request_without_playlist_info(self, playlistInfo: dict) -> dict:
        all_items = self.get_all_playlist_positions(playlistInfo["id"])
        return all_items

    def getNextToken(self, response) -> str:
        token = ""
        try:
            token = response["nextPageToken"]
        except:
            token = None
        return token

    def debugFun(self):
        print(self.makeChannelRequest())
        # a = self.make_playlist_request("PL3PsnSHm-8ZIUHsVHORJdgGwx9EF-3aRT")
        # parser = PlaylistResponseParser.PlaylistResponseParser()
        # h = parser.parse_response_header(a[0], default_playlist_params)
        # b = parser.parse_response_body(a[1], default_video_params)
        # print(parser.join_header_and_body(h,b))
        pass

# apiServiceName = "youtube"
# apiVersion  = "v3"

# youtube = googleapiclient.discovery.build(apiServiceName,apiVersion,developerKey=self.key)


# # res1 = youtube.playlists().list( 
# #     part="id,contentDetails,snippet",
# #     channelId="UC0KfUunv1cE_EL6y8-wqBFQ").execute()
# # print(res1)

#     #  "nextPageToken": "EAAaBlBUOkNBOA", zeby dostac kolejne 50 z playlisty
#     #  "prevPageToken": "EAEaBlBUOkNBbw", poprzednie..
# res = youtube.playlistItems().list(
#     part="contentDetails,snippet,id",
#     #pageToken="EAAaBlBUOkNBbw",
#     playlistId="PL3PsnSHm-8ZLkj26544Iw7B0trcoc66cK",
#     maxResults="3"
#     ).execute()
# print(res["playlistId"])
# for it in res["items"]:
#     print(it["snippet"])

# # print(res["nextPageToken"])
# # print(res["items"])
# for it in res["items"]:
#     print(it["snippet"]["videoOwnerChannelTitle"] + " - " + it["snippet"]["title"])

# print(res)

# from googleapiclient.discovery import build

# api_key = 'YOUR_API_KEY'
# youtube = build('youtube', 'v3', developerKey=api_key)

# # The channelId for the YouTube channel
# channel_id = 'CHANNEL_ID'

# # Make the API request to get the list of playlists
# request = youtube.playlists().list(
#     part='snippet',
#     channelId=channel_id,
#     maxResults=50  # You can fetch up to 50 playlists per request
# )

# response = request.execute()

# # Print the playlist titles
# for playlist in response['items']:
#     print(f"Playlist Title: {playlist['snippet']['title']}, Playlist ID: {playlist['id']}")
    
# # Handle pagination if more than 50 playlists
# next_page_token = response.get('nextPageToken')
# while next_page_token:
#     request = youtube.playlists().list(
#         part='snippet',
#         channelId=channel_id,
#         maxResults=50,
#         pageToken=next_page_token
#     )
#     response = request.execute()
    
#     for playlist in response['items']:
#         print(f"Playlist Title: {playlist['snippet']['title']}, Playlist ID: {playlist['id']}")
    
#     next_page_token = response.get('nextPageToken')

# c = Caller()
# #c.makeChannelRequest()
# c.debugFun()