from dataclasses import dataclass
import json

@dataclass
class Command:
    msgID: str
    msgPayload: str
    msgCommand: str

    def __init__(self, string_format_command):
        data:json = json.load(string_format_command)
        self.msgCommand=data['msgCommand']
        self.msgID = data['msgID']
        self.msgCommand = data['msgCommand']
    def get(self):
        map = {
            'msgID': self.msgID,
            'msgPayload': self.msgPayload,
            'msgCommand': self.msgCommand
        }
        return map

    def __str__(self):
        map = {
            'msgID': self.msgID,
            'msgPayload': self.msgPayload,
            'msgCommand': self.msgCommand
        }
        return str(map)