# TODO

## Write README.md

## Issues to Fix

### Printing and Capturing Output

1. In order to keep Paramiko from executing before a command finishes, after you run

`run_command_in_ssh_session()`

you must run:

`print_command_output()`

The `print_command_output()` blocks Paramiko's execution until the command is done producing output.

2. If you want to capture output into the `Command` object, you will again, have to run:

`print_command_output()`

Output will not be captured unless you do

Solution 1: We will probably have to change the `print_command_output()` function to be named
`capture_command_output()` that takes in a `should_print_output` parameter.

The function will always capture output, but only print if the user wants.  Then, we will call
`capture_command_output()` from within the `run_command_in_ssh_session()` function.  The
`run_command_in_ssh_session()` function will also have the `should_print_output` parameter.  The
`SSHSessionManager` will need to change its `run_commands_in_all_ssh_sessions()` and might have to
use threads on each session, since the blocking will happen and stop each session from being
launched concurrently.

### Storing Standard Error and Return Codes

- Rework system to also store items for stderr into the dictionaries on `SSHSession`; there should
  probably be some sort of sub dictionary with a "standard output" key and a "standard error" key.
- This will require changes to the way output is capture, so it may as well be done with the changes
  above for SSHSession
