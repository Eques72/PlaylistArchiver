
from abc import ABC, abstractmethod

class FormatFactory(ABC):
    def __init__(self) -> None:
        pass
    
    def prepareDataToBeIncluded(self, includeParams: list,itemsData: dict, playlistInfo: dict) -> str:
        data = self.prepareDataHeader(playlistInfo)
        data += self.prepareDataForTheFormat(itemsData , includeParams)
        return data

    @abstractmethod
    def prepareDataForTheFormat(self,itemsData: dict, includeParams: list) -> str:
        pass

    @abstractmethod
    def prepareDataHeader(self,playlistInfo: dict) -> str:
        pass

    pass


