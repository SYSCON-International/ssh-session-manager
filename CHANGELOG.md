# CHANGELOG

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
