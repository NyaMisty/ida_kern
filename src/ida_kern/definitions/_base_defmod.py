__all__ = ['BaseDefinitionMod']
from typing import *
from abc import ABCMeta, abstractmethod

from ida_kern.utils.platform_helper import IDAInfo


class BaseDefinitionMod(metaclass=ABCMeta):
    @abstractmethod
    def dll_needed(self) -> List[str]:
        pass

    @abstractmethod
    def load_definition(self, dlls: Dict[str, Any], idainfo: IDAInfo) -> Dict[str, Any]:
        pass