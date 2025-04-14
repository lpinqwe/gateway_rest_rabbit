from DataConverter.DataManager import ReturningData
from interfaces import messagesInterface
from interfaces.CommandStructure import Command
from interfaces.CommandStructure import Command


class CommandGetJSON(messagesInterface.MessageInterface):

    def __init__(self, map):
        """***this command will return json format from data***"""
        super.__init__(map)
        pass

    def execute(self) -> Command:
        answer = Command(ReturningData())

        return answer
