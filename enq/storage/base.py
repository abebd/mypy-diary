import logging

from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Storage(ABC):
    
    @abstractmethod
    def add_entry(self, title, message, timestamp):
        pass

    @abstractmethod
    def open_entry(self, title, message, timestamp):
        pass

    @abstractmethod
    def get_entries(self) -> list:
        pass
        
