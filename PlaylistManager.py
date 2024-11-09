from PlaylistResponseParser import PlaylistResponseParser
from Caller import Caller
import json
from enum import Enum

class ManagerState(Enum):
    CREATING_MULTIPLE = 1
    CREATING_SINGLE = 2
    FREE = 3
    UPDATING_SINGLE = 4

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
    # manager_states
    def __init__(self):
        self.playlist_response_parser = PlaylistResponseParser()
        self.caller = Caller()
        self.playlist_data = []
        self.state = ManagerState.FREE
        self.playlist_analysis = {}

    def handle_state(self, desired_prev_states, desired_next_state:ManagerState) -> bool:
        if not isinstance(desired_prev_states, list):
            desired_prev_states = [desired_prev_states]
        if self.state not in desired_prev_states:
            print("Manager is busy or in wrong state")
            return False
        else:
            self.state = desired_next_state
    
    def create_multiple_new_playlist_records(self, channel_address, includes) -> None:
        if not self.handle_state(ManagerState.FREE, ManagerState.CREATING_MULTIPLE):
            return
        playlist_items = self.caller.make_channel_request(channel_address)
        for item in playlist_items:
            res = self.caller.make_playlist_request_without_playlist_info(item)
            h = self.playlist_response_parser.parse_response_header(item, self.default_playlist_params, includes)
            b = self.playlist_response_parser.parse_response_body(res, includes)
            self.playlist_data.append(self.playlist_response_parser.join_header_and_body(h,b))

    def create_new_playlist_record(self, address, includes) -> None:
        res = self.caller.get_playlist_response(address)
        h = self.playlist_response_parser.parse_response_header(res[0], self.default_playlist_params, includes)
        b = self.playlist_response_parser.parse_response_body(res[1], includes)
        self.playlist_data.append(self.playlist_response_parser.join_header_and_body(h,b))
        pass

    def get_playlist_name(self, playlist_index:int=0) -> str:
        return str(self.playlist_data[playlist_index]["header"]["title"])

    def load_playlist_record(self, filepath:str) -> None:
        with open(filepath, "r", -1, "utf-8") as file:
            self.playlist_data.append(json.loads(file.read()))
        
    def compare_playlist_record_with_online(self, playlist_index:int=0, by_index:bool=True, by_ids:bool=True) -> None:
        res = self.caller.make_playlist_request(self.playlist_data[playlist_index]["header"]["id"])
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
                               remove_missing:bool=False, add_new:bool=True) -> None:
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

    def save_playlist_record(self, filename:str, playlist_index:int=0, remove_from_list:bool=False) -> None:
        with open(filename, "w", -1, "utf-8") as file:
            file.write(json.dumps(self.playlist_data[playlist_index], ensure_ascii=False, indent=4))
            if remove_from_list:
                self.playlist_data.pop(playlist_index)
        print("Playlist saved to file: " + filename)

    def save_multiple_playlist_records(self, filename:str) -> None:
        for i in range(0,len(self.playlist_data)):
            self.save_playlist_record(filename + "_" + str(i), i)
        self.playlist_data.clear()
        pass

        #     if self.state.get() == 1: #all playlists        
        #     for i in range(0,len(response)):
        #         with open(filename + str(i), "w", -1, "utf-8") as file:
        #             file.write(response[i](1.0, tk.END))
        # if self.state.get() == 0: #all playlists        
        #     with open(filename, "w", -1, "utf-8") as file:
        #         file.write(response)  