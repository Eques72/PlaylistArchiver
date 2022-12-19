import FormatFactory

class TextFormatFactory(FormatFactory.FormatFactory):

    def __init__(self) -> None:
        super().__init__()
        pass
    
    def prepareDataForTheFormat(self,itemsData: dict, includeParams: list) -> str:
        videosData:str = ""
          # options = ["Video name","Video address","Video author", "Playlist info","Video description","Upload date","Video thumbnail url",  "Playlist author"]
        for info in itemsData["items"]:
            if includeParams[0] == True: #name
                try:
                    videosData += (str)(info["snippet"]["position"]) + ". " + info["snippet"]["title"] + " "
                except:
                    videosData += "Video Unavailable "
            if includeParams[2] == True: #author
                try:
                    videosData += "- "+info["snippet"]["videoOwnerChannelTitle"] + ", "
                except:
                    try:
                        videosData += "- "+info["snippet"]["channelId"] + ", "
                    except:
                        videosData += " ,"
            if includeParams[4] == True: #description
                description = ""
                try:
                    description = info["snippet"]["description"]
                    description = ' '.join(description.splitlines())
                except:
                    description = "Unavailable"
                videosData += "Description: " + description + " "                
            if includeParams[1] == True: #address
                try:
                    videosData += "https://www.youtube.com/watch?v=" + info["contentDetails"]["videoId"] + " "                
                except:
                    videosData += "Video address unavailable "
            if includeParams[3] == True: #playlist info
                videosData += " "                
            if includeParams[5] == True: #date
                videosData += " "                
            if includeParams[6] == True: #thumbnail
                videosData += " "                
            if includeParams[7] == True: #playlist owner   
                videosData += " "
            videosData += "\n"                
        return videosData

    def prepareDataHeader(self,playlistInfo) -> str:
        header:str = ""
        readableInfo:str = ""
        for info in playlistInfo["items"]:
            header = "{\nplaylistId:"+info["id"]+"channelId:"+info["snippet"]["channelId"] + "\n" 
            readableInfo = "Playlist Title: " + info["snippet"]["title"] + " Created at: " + info["snippet"]["publishedAt"]
            readableInfo +=  "\nDescription: "+info["snippet"]["description"] + "\nVisible videos: " 
            readableInfo += (str)(info["contentDetails"]["itemCount"]) + "\nPlaylist owner: "+info["snippet"]["channelTitle"] + "\n}\n"
        return header+readableInfo
    
    pass