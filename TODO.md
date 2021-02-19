# TODO

## Issues to Fix

### SSHSession

1. In order to keep Paramiko from executing before a command finishes, after you run

`run_command_in_ssh_session()`

you must run:

`print_command_output()`

The `print_command_output()` blocks Paramikos execution until the command is done producing output.

2. If you want to capture output into the `Command` object, you will again, have to run:

`print_command_output()`

Output will not be captured unless you do

Solution 1: We will probably have to change the `print_command_output()` function to be named
`capture_command_output()` that takes in a `should_print_output` parameter.  The function will
always capture output, but only print if the user wants.  Then, we will call
`capture_command_output()` from within the `run_command_in_ssh_session()` function.  The
`run_command_in_ssh_session()` function will also have the `should_print_output` parameter.  The
`SSHSessionManager` will need to change its `run_commands_in_all_ssh_sessions()` and might have to
use threads on each session, since the blocking will happen and stop each session from being
launched concurrently.

### SSHSessionManager

1. The `SSHSessionManager` currently takes in a list of `SSHSession`s and a list of `Command`s.
Each `Command` is ran on all `SSHSession`s.  When the functionality to capture output from a running
command was added, the captured output was simply stored on the `Command` object.  The issue with
this is, all `SSHSession`s will try to store their output to a single `Command` object - each
captured output from one session will be overwritten by the next.  We need to figure out the best to
way to store all captured output.

Solution 1: Clone each `Command` object an amount of times equal to the number of `SSHSessions`,
then store the captured output from each session in its own command.

Solution 2: Store the output of each `Command` on the `SSHSession` itself, as a list of captured
outputs.
