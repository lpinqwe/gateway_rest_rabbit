from commands import TestCommand
from interfaces.CommandStructure import Command

class Factory:
    def __init__(self):
        self.commands = {
            'getjson': TestCommand,
            'getxml': TestCommand,
            'test': TestCommand

        }
    def execute_command(self,command:Command)->Command:
        try:
            cmd = command.msgCommand.lower()
            command_to_execute = self.commands.get(cmd)

            if command_to_execute is None:
                raise ValueError(f"Unknown command type: {command_to_execute}")
            if not callable(command_to_execute):
                raise TypeError(f"Command {command_to_execute} is not callable.")
            cmd_obj=command_to_execute(command)
            return cmd_obj.execute()

        except Exception as e:
            print(Command)
            print("sthGoneWrong")
            print(e)
            raise e