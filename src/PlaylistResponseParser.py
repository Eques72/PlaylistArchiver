class PlaylistResponseParser:
    def __init__(self) -> None:
        pass
    
    def parse_single_video(self, video_data: dict, included_params: dict) -> dict:
        video = {}
        try:
            video.update({
                "videoId": video_data["contentDetails"]["videoId"],
                "title": video_data["snippet"]["title"],
                "position": video_data["snippet"]["position"]
            })
        except:
            video.update({
                "videoId": "Unavailable",
                "title": "Unavailable",
                "position": "Unavailable"
            })
        if included_params["channelId"]:
            try:
                video["channelId"] = video_data["snippet"]["videoOwnerChannelId"]
            except:
                video["channelId"] = ""
        if included_params["channelTitle"]:
            try:
                video["channelTitle"] = video_data["snippet"]["videoOwnerChannelTitle"]
            except:
                video["channelTitle"] = ""
        if included_params["description"]:
            try:
                video["description"] = video_data["snippet"]["description"]
            except:
                video["description"] = ""
        if included_params["videoPublishedAt"]:
            try:
                video["videoPublishedAt"] = video_data["contentDetails"]["videoPublishedAt"]
            except:
                video["videoPublishedAt"] = ""
        if included_params["thumbnail"]:
            try:
                video["thumbnail"] = video_data["snippet"]["thumbnails"]["maxres"]["url"]
            except:
                try:
                    video["thumbnail"] = video_data["snippet"]["thumbnails"]["default"]["url"]
                except:
                    video["thumbnail"] = ""
        return video
                 
    def parse_response_body(self, items_data: dict, included_params: dict) -> list:
        videos_data = []
        for item in items_data["items"]:
            videos_data.append(self.parse_single_video(item, included_params))
        return videos_data

    def parse_response_header(self, playlistInfo: dict, included_params: dict, included_video_params :dict) -> dict:
        header = {}
        for item in playlistInfo["items"]:
            header.update({
                "id": item["id"],
                "publishedAt": item["snippet"]["publishedAt"],
                "channelId": item["snippet"]["channelId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "itemCount": item["contentDetails"]["itemCount"]
            })
        for key, val in included_params.items():
            included_params.update({key: "True" if val else "False"})
        header.update({"included_playlist_params": included_params})
        for key, val in included_video_params.items():
            included_video_params.update({key: "True" if val else "False"})
        header.update({"included_video_params": included_video_params})
        return header
    
    def join_header_and_body(self, header: dict, body: list) -> dict:
        return {"header": header, "body": body}
    
    def deserialize_playlist_includes(self, headerInfo: dict) -> tuple:
        included_playlist_params = {}
        included_video_params = {}
        for key, val in headerInfo["included_playlist_params"].items():
            included_playlist_params.update({key: True if val == "True" else False})
        for key, val in headerInfo["included_video_params"].items():
            included_video_params.update({key: True if val == "True" else False})
        return (included_playlist_params, included_video_params)
