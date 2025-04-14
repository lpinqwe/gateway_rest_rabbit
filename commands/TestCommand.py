
import json

from _distutils_hack import override
from interfaces.CommandStructure import Command
from interfaces import messagesInterface
class TestCommand(messagesInterface.MessageInterface):


    def __init__(self, map):
        """***this command will return TEST ***"""
        super.__init__(map)
        pass

    def execute(self) -> Command:
        map = {
            'msgID': 'test',
            'msgPayload': 'test',
            'msgCommand': 'test'
        }
        answer = Command(str(map))

        return answer