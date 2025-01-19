from PlaylistResponseParser import PlaylistResponseParser
from Caller import Caller
import json
from enum import Enum
import re
import os

class ManagerState(Enum):
    CREATING_MULTIPLE = 1
    CREATING_SINGLE = 2
    FREE = 3

class PlaylistManager:
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

    def __init__(self):
        self.playlist_response_parser = PlaylistResponseParser()
        self.caller = Caller()
        self.playlist_data = []
        self.state = ManagerState.FREE
        self.playlist_analysis = {}

    def __handle_state(self, desired_prev_states, desired_next_state:ManagerState) -> bool:
        if not isinstance(desired_prev_states, list):
            desired_prev_states = [desired_prev_states]
        if self.state not in desired_prev_states:
            print("Manager is busy or in wrong state")
            return False
        else:
            self.state = desired_next_state
        return True
    
    def create_multiple_new_playlist_records(self, channel_address, includes) -> None:
        if not self.__handle_state(ManagerState.FREE, ManagerState.CREATING_MULTIPLE):
            return
        try:
            playlist_items = self.caller.make_channel_request(channel_address)
            for item in playlist_items:
                res = self.caller.make_playlist_request(item["id"])
                h = self.playlist_response_parser.parse_response_header(res[0], self.default_playlist_params, includes.copy())
                b = self.playlist_response_parser.parse_response_body(res[1], includes.copy())
                self.playlist_data.append(self.playlist_response_parser.join_header_and_body(h, b))
        except Exception as e:
            print(f'Error: {e}')
            raise

    def create_new_playlist_record(self, address, includes) -> None:
        try:
            res = self.caller.get_playlist_response(address)
        except Exception as e:
            print(f'Error: {e}')
            raise
        h = self.playlist_response_parser.parse_response_header(res[0], self.default_playlist_params, includes.copy())
        b = self.playlist_response_parser.parse_response_body(res[1], includes)
        self.playlist_data.append(self.playlist_response_parser.join_header_and_body(h,b))
        pass

    def get_playlist_name(self, sanitized:bool=False, playlist_index:int=0) -> str:
        if playlist_index < 0 or playlist_index >= len(self.playlist_data):
            return "None"
        name = str(self.playlist_data[playlist_index]["header"]["title"]) if self.playlist_data[playlist_index]["header"]["title"] else "No title"
        if sanitized:
            invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'
            name = re.sub(invalid_chars, "_", name)
        return name

    def get_playlist_basic_info(self, playlist_index:int=0) -> str:
        if playlist_index < 0 or playlist_index >= len(self.playlist_data):
            return {"title":"None", "channelId":"None", "description":"None", "itemCount":"None"}
        return {"title":self.playlist_data[playlist_index]["header"]["title"],
                "channelId": self.playlist_data[playlist_index]["header"]["channelId"],
                "description": self.playlist_data[playlist_index]["header"]["description"],
                "itemCount": self.playlist_data[playlist_index]["header"]["itemCount"]}

    def load_playlist_record(self, filepath:str) -> None:
        with open(filepath, "r", -1, "utf-8") as file:
            self.playlist_data.append(json.loads(file.read()))
        
    def compare_playlist_record_with_online(self, playlist_index:int=0, by_index:bool=True, by_ids:bool=True) -> None:
        if playlist_index < 0 or playlist_index >= len(self.playlist_data):
            print("Playlist index out of range or no playlist data")
            return [],[],[]
        try:
            res = self.caller.make_playlist_request(self.playlist_data[playlist_index]["header"]["id"])
        except Exception as e:
            print(f'Error: {e}')
            raise
        i_h, i_b = self.playlist_response_parser.deserialize_playlist_includes(self.playlist_data[playlist_index]["header"])
        h = self.playlist_response_parser.parse_response_header(res[0], self.default_playlist_params, i_h)
        b = self.playlist_response_parser.parse_response_body(res[1], i_b)
        self.playlist_data.append(self.playlist_response_parser.join_header_and_body(h,b))

        new_elements = []
        missing_elements = []
        if by_ids:
            # elements that are in the online playlist but not in the local one
            local_playlist_copy = self.playlist_data[playlist_index]["body"].copy()
            for element_o in self.playlist_data[playlist_index+1]["body"]:
                for element_l in local_playlist_copy:
                    if element_o["videoId"] == element_l["videoId"]:
                        local_playlist_copy.remove(element_l)
                        break
                else:
                    new_elements.append(element_o)
            # elements that are in the local playlist but not in the online one
            missing_elements = local_playlist_copy
        mismatched_index_elements = []
        if by_index:
            #elements that are in both playlists but have different indexes - data structure: pos, id1, id2, title1, title2
            min_len = min(self.playlist_data[playlist_index]["header"]["itemCount"], 
                          self.playlist_data[playlist_index+1]["header"]["itemCount"])
            for i in range(0, min_len):
                if self.playlist_data[playlist_index]["body"][i]["videoId"] != self.playlist_data[playlist_index+1]["body"][i]["videoId"]:
                    mismatched_index_elements.append([i, self.playlist_data[playlist_index]["body"][i]["videoId"], 
                                                      self.playlist_data[playlist_index+1]["body"][i]["videoId"], 
                                                      self.playlist_data[playlist_index]["body"][i]["title"], 
                                                      self.playlist_data[playlist_index+1]["body"][i]["title"]])
        self.playlist_analysis[self.get_playlist_name(playlist_index)] = (new_elements, missing_elements, mismatched_index_elements)
        return new_elements, missing_elements, mismatched_index_elements

    def update_playlist_record(self, playlist_index:int=0,
                               remove_missing:bool=False, 
                               add_new:bool=True) -> None:
        if playlist_index < 0 or playlist_index >= len(self.playlist_data):
            print("Playlist index out of range or no playlist data")
            return
        new_elements, missing_elements, _ = self.playlist_analysis[self.get_playlist_name(playlist_index)]
        if remove_missing:
            for element in self.playlist_data[0]["body"]:
                if element in missing_elements:
                    self.playlist_data[0]["body"].remove(element)
        if add_new:
            for element in new_elements:
                self.playlist_data[0]["body"].append(element)
        self.playlist_data[0]["header"]["itemCount"] = len(self.playlist_data[0]["body"])
        for element in self.playlist_data[0]["body"]:
            element["index"] = self.playlist_data[0]["body"].index(element)
        self.playlist_data.pop(1)

    def save_playlist_record(self, filepath:str, playlist_index:int=0, remove_from_list:bool=False, safe_to_save:bool=True) -> None:
        if not safe_to_save and playlist_index < 0 or playlist_index >= len(self.playlist_data):
            print("Playlist index out of range or no playlist data")
            return False
        with open(filepath, "w", -1, "utf-8") as file:
            file.write(json.dumps(self.playlist_data[playlist_index], ensure_ascii=False, indent=4))
            if remove_from_list:
                self.playlist_data.pop(playlist_index)
        print("Playlist saved to file: " + filepath)
        return True

    def save_multiple_playlist_records(self, filepath:str, safe_to_save:bool=True, get_unique_names=True) -> None:
        if not safe_to_save:
            return False
        for i in range(0,len(self.playlist_data)):
            single_filepath = ""
            if get_unique_names:
                single_filepath = os.path.join(filepath, self.playlist_data[i]["header"]["title"] + ".json")
            else:
                single_filepath = os.path.splitext(filepath)[0] + "_" + str(i) + ".json"
            self.save_playlist_record(single_filepath, i)
        self.playlist_data.clear()
        return True

    def export_to_spotify(self, playlist_index:int=0, safe_to_save:bool=True) -> int:
        if not safe_to_save and playlist_index < 0 or playlist_index >= len(self.playlist_data):
            print("Playlist index out of range or no playlist data")
            return 0
        print(self.playlist_data[playlist_index]["header"]["itemCount"])
        all_titles = [self.playlist_data[playlist_index]["body"][i]["title"] for i in range(0,int(self.playlist_data[playlist_index]["header"]["itemCount"]))]
        for i in range(0,len(all_titles)):
            all_titles[i] = re.sub(r'[^a-zA-Z0-9]', ' ', all_titles[i])
            all_titles[i] = re.sub(r'\s+', ' ', all_titles[i])
            all_titles[i] = all_titles[i].strip()
        try:
            return self.caller.create_spotify_playlist(
                self.playlist_data[playlist_index]["header"]["title"],
                self.playlist_data[playlist_index]["header"]["description"],
                all_titles)
        except Exception as e:
            print(f'Error: {e}')
            raise

    def reset(self):
        self.playlist_data.clear()
        self.state = ManagerState.FREE
        self.playlist_analysis = {}
