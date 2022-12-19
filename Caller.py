import dotenv
import os
import googleapiclient.discovery
import requests

import TextFormatFactory


class Caller:
    __apiServiceName = "youtube"
    __apiVersion  = "v3"

    def __init__(self) -> None:
        pass    

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
        
    def getPlaylistData(self, address, includes):
        playlistID = self.scrapPlaylistID(address)
        responses = self.makePlaylistRequest(playlistID)
        tFF = TextFormatFactory.TextFormatFactory()
        formattedData = tFF.prepareDataToBeIncluded(includes, responses[1], responses[0])
        return formattedData

    def scrapPlaylistID(self, address:str) -> str:
        index = address.find("list=")
        index += 5
        return address[index:]

    def makeChannelRequest(self):
        dotenv.load_dotenv()
        key = os.getenv('KEY')
        youtube = googleapiclient.discovery.build(Caller.__apiServiceName,Caller.__apiVersion,developerKey=key)
        res = youtube.playlists().list( 
        part="id,contentDetails,snippet",
        channelId="UC0KfUunv1cE_EL6y8-wqBFQ").execute()
        pass

    def makePlaylistRequest(self, playlistID: str) -> tuple:
        dotenv.load_dotenv()
        key = os.getenv('KEY')
        youtube = googleapiclient.discovery.build(Caller.__apiServiceName,Caller.__apiVersion,developerKey=key)
        
        playlistInfo = youtube.playlists().list(
            id=playlistID,
            part="contentDetails,snippet,id",
            maxResults="1"
            ).execute()
        answer = {}
        res = youtube.playlistItems().list(
            part="contentDetails,snippet,id",
            playlistId=playlistID,
            maxResults="50"
            ).execute()

        nextToken = self.getNextToken(res)
        answer = answer | res
        #answer += self.prepAnswer(res, True)
        while nextToken != None:
            res = youtube.playlistItems().list(
            part="contentDetails,snippet",
            pageToken=nextToken,
            playlistId=playlistID,
            maxResults="50"
            ).execute()
            nextToken = self.getNextToken(res)
            answer["items"] = answer["items"] + res["items"]
        #    answer += self.prepAnswer(res, False)
        return (playlistInfo, answer)
        
    def getNextToken(self, response) -> str:
        token = ""
        try:
            token = response["nextPageToken"]
        except:
            token = None
        return token

    #isNeeded?
    def prepAnswer(self, response, makeHeader: bool):
        pass    



# dotenv.load_dotenv()
# key = os.getenv('KEY')
# apiServiceName = "youtube"
# apiVersion  = "v3"

# youtube = googleapiclient.discovery.build(apiServiceName,apiVersion,developerKey=key)


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