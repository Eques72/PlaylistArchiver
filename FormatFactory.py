
from abc import ABC, abstractmethod

class FormatFactory(ABC):
    def __init__(self) -> None:
        pass
    
    def prepareDataToBeIncluded(self, includeParams: list,itemsData: dict, playlistInfo: dict) -> str:
        data = self.prepareDataHeader(itemsData)
        data += self.prepareDataForTheFormat(playlistInfo, includeParams)
        return data

    @abstractmethod
    def prepareDataForTheFormat(self,itemsData: dict, includeParams: list) -> str:
        pass

    @abstractmethod
    def prepareDataHeader(self,playlistInfo: dict) -> str:
        pass

    pass


