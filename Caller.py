import dotenv
import os
import googleapiclient.discovery

class Caller:
    __apiServiceName = "youtube"
    __apiVersion  = "v3"

    def __init__(self) -> None:
        pass    

    def getAllPlaylistsData(self, address, includes):
        pass
        
    def getPlaylistData(self, address, includes):
        pass    

    def makeChannelRequest(self):
        dotenv.load_dotenv()
        key = os.getenv('KEY')
        youtube = googleapiclient.discovery.build(Caller.__apiServiceName,Caller.__apiVersion,developerKey=key)
        res = youtube.playlists().list( 
        part="id,contentDetails,snippet",
        channelId="UC0KfUunv1cE_EL6y8-wqBFQ").execute()
        pass

    def makePlaylistRequest(self, playlistID: str) -> str:
        dotenv.load_dotenv()
        key = os.getenv('KEY')
        youtube = googleapiclient.discovery.build(Caller.__apiServiceName,Caller.__apiVersion,developerKey=key)
        #REMEMBER TOKENS
        answer = ""
        res = youtube.playlistItems().list(
            part="contentDetails,snippet,id",
            playlistId=playlistID,
            maxResults="50"
            ).execute()
        nextToken = self.getNextToken(res)
        answer += self.prepAnswer(res, True)
        while nextToken != None:
            res = youtube.playlistItems().list(
            part="contentDetails,snippet",
            pageToken=nextToken,
            playlistId=playlistID,
            maxResults="50"
            ).execute()
            nextToken = self.getNextToken(res)
            answer += self.prepAnswer(res, False)
        pass
        
    def getNextToken(self, response):
        pass

    def prepAnswer(self, response, makeHeader: bool):
        pass    



# dotenv.load_dotenv()
# key = os.getenv('KEY')
# apiServiceName = "youtube"
# apiVersion  = "v3"

# youtube = googleapiclient.discovery.build(apiServiceName,apiVersion,developerKey=key)

# res1 = youtube.playlists().list( 
#     part="id,contentDetails,snippet",
#     channelId="UC0KfUunv1cE_EL6y8-wqBFQ").execute()
# print(res1)

    #  "nextPageToken": "EAAaBlBUOkNBOA", zeby dostac kolejne 50 z playlisty
    #  "prevPageToken": "EAEaBlBUOkNBbw", poprzednie..
# res = youtube.playlistItems().list(
#     part="contentDetails,snippet,id",
#     #pageToken="EAAaBlBUOkNBbw",
#     playlistId="PL3PsnSHm-8ZLkj26544Iw7B0trcoc66cK",
#     maxResults="3"
#     ).execute()

# # print(res["nextPageToken"])
# # print(res["items"])
# for it in res["items"]:
#     print(it["snippet"]["videoOwnerChannelTitle"] + " - " + it["snippet"]["title"])

# print(res)