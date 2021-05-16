# CHANGELOG

## v0.3.2

- **Note:** v0.3.2 has breaking changes
- `get_command_output_information_dictionary()` has been renamed to
  `get_command_output_dictionary()`
- Some documentation added
- General package / repository cleanup

## v0.3.1

- **Note:** v0.3.1 has breaking changes
- Removed cached ping methods - these never really made much sense
- Swapped out custom ping method for [ping3](https://pypi.org/project/ping3/), which allows us to
  provide a `timeout_in_seconds` parameter to ping methods

## v0.3.0

- Added ping methods to `SSHSession` and `SSHSessionManager`
## v0.2.0

- **Note:** v0.2.0 has breaking changes
- The `SSHSessionManager` now spins up a separate thread for each `SSHSession`, a change needed to
  fix the previous strange requirement of having to call a `print_command_output()` in order to keep
  the `SSHSession` from exiting before the command finished.  This function no longer exists,
  blocking happens automatically, and printing out output is set via an input parameter to both
  `run_commands_in_all_ssh_sessions()` and `run_command_in_ssh_session()`.
- `SSHSession`s now store standard output, standard error, and the command exit code
- `SSHSession` no longer provides the ability to capture specific output.  Since all output is now
  captured and saved, it is up to the user to search through it to find what they need.
- Removed some code, marked some items as "private" via `__`.
- Some functions have been renamed
- `SSHSession` no longer takes in a `session_description` variable in the `__init__()`

## v0.1.0

- **NOTE:** v0.1.0 has breaking changes
- Implemented a system to hold the output of all commands ran on a session.  The `SSHSessionManager`
  holds a dictionary that maps an `SSHSession` object to an internal dictionary.  This internal
  dictionary maps the `Command` object to the captured output message.  Output is no longer  stored
  in the `Command` objects.
- The internal dictionary that holds the captured output, as mentioned above, will now also capture
  the exit code for the command that ran as well.  Execution is now blocked on both the captured
  output and the exit code of the command, so that the session will not end until both of these are
  captured (unless the user doesn't request any output to be captured, then execution blocking will
  only happen on the exit code).
- Added print statements for some errors that were previously being omitted from output.

## v0.0.2

- Small documentation / repository changes

## v.0.0.1

- Initial release
