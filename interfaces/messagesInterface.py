import json
from abc import abstractmethod,ABC
from interfaces.CommandStructure import Command
class MessageInterface(ABC):


    @abstractmethod
    def __init__(self,command_to_process:Command):
        self.command=command_to_process
        return


    @abstractmethod
    def execute(self)->Command:
        return
