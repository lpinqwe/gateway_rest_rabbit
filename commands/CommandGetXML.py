import json

from _distutils_hack import override

from DataConverter.DataManager import ReturningData
from interfaces import messagesInterface
from interfaces.CommandStructure import Command

class CommandGetXML(messagesInterface.MessageInterface):

    def __init__(self, map):
        """***this command will return XML format from data***"""
        super.__init__(map)
        pass

    def execute(self) -> Command:
        map={}
        answer = Command(ReturningData())

        return answer