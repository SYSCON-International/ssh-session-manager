class Command:
    def __init__(self, command_to_execute, command_user_input=None):
        self.command_to_execute = command_to_execute
        # Do not forget to supply any newlines expected by the command in order to execute the input
        self.command_user_input = command_user_input

    def __str__(self):
        return f"\"{self.command_to_execute}\""
