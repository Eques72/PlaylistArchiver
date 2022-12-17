import FormatFactory

class TextFormatFactory(FormatFactory):
    def __init__(self) -> None:
        super().__init__()
        pass
        # for it in res["items"]:
#     print(it["snippet"]["videoOwnerChannelTitle"] + " - " + it["snippet"]["title"])
    def prepareDataForTheFormat(self,itemsData: dict, includeParams: list) -> str:
        videosData:str = ""
          # options = ["Video name","Video address","Video author", "Playlist info","Video description","Upload date","Video thumbnail url",  "Playlist author"]
        for info in itemsData["items"]:
            if includeParams[0] == True: #name
                videosData += info["snippet"]["title"] + " "
            if includeParams[2] == True: #author
                videosData += "- "+info["snippet"]["videoOwnerChannelTitle"] + ", "
            if includeParams[4] == True: #description
                videosData += "Description: " + info["snippet"]["description"] + " "                
            if includeParams[1] == True: #address
                videosData += "https://www.youtube.com/watch?v=" + info["contentDetails"]["videoId"] + " "                
            if includeParams[3] == True: #playlist info
                videosData += " "                
            if includeParams[5] == True: #date
                videosData += " "                
            if includeParams[6] == True: #thumbnail
                videosData += " "                
            if includeParams[7] == True: #playlist owner   
                videosData += " "
            videosData += "\n"                
            pass
        pass

    def prepareDataHeader(self,playlistInfo) -> str:
        header:str = ""
        readableInfo:str = ""
        for info in playlistInfo["items"]:
            header = "{playlistId:"+info["id"]+"channelId:"+info["snippet"]["channelId"] + "\n" 
            readableInfo = ("Playlist Title: " + info["snippet"]["title"] + 
                " Created at: " + info["snippet"]["publishedAt"] + "\nDescription: "+info["snippet"]["description"]
                + "\nVisible videos: " + info["contentDetails"]["itemCount"] +
                "\nPlaylist owner: "+info["snippet"]["channelTitle"])
        return header+readableInfo
    
    pass