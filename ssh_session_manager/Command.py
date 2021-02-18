class Command:
    def __init__(
        self, command_to_execute, command_user_input=None, command_provides_output=False, prefix_to_match_on_to_capture_specific_output_line=None,
        suffix_to_match_on_to_capture_specific_output_line=None
    ):
        self.command_to_execute = command_to_execute
        # Do not forget to supply any newlines expected by the command in order to execute the input
        self.command_user_input = command_user_input

        self.command_provides_output = command_provides_output
        self.prefix_to_match_on_to_capture_specific_output_line = prefix_to_match_on_to_capture_specific_output_line
        self.suffix_to_match_on_to_capture_specific_output_line = suffix_to_match_on_to_capture_specific_output_line
        self.specifically_captured_output_text = None

    def __str__(self):
        return f"\"{self.command_to_execute}\""
