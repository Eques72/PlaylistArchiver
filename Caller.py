import dotenv
import os

dotenv.load_dotenv()
key = os.getenv('KEY')
apiServiceName = "youtube"
apiVersion  = "v3"

youtube = googleapiclient.discovery.build(apiServiceName,apiVersion,developerKey=key)

res1 = youtube.playlists().list( 
    part="id,contentDetails,snippet",
    channelId="UC0KfUunv1cE_EL6y8-wqBFQ").execute()
print(res1)

    #  "nextPageToken": "EAAaBlBUOkNBOA", zeby dostac kolejne 50 z playlisty
    #  "prevPageToken": "EAEaBlBUOkNBbw", poprzednie..
res = youtube.playlistItems().list(
    part="contentDetails,snippet,id",
    #pageToken="EAAaBlBUOkNBbw",
    playlistId="PL3PsnSHm-8ZLkj26544Iw7B0trcoc66cK",
    maxResults="50"
    ).execute()

print(res["nextPageToken"])
print(res["items"])
for it in res["items"]:
    print(it["snippet"]["videoOwnerChannelTitle"] + " - " + it["snippet"]["title"])

print(res)