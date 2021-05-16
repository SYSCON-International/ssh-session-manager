# ssh_session_manager

Execute commands on multiple remote SSH sessions

[PyPI](https://pypi.org/project/ssh-session-manager/)


## Example 1: Using the `SSHSession`

```python
#!/usr/bin/env python

from ssh_session_manager.Command import Command
from ssh_session_manager.SSHSession import SSHSession


ssh_session = SSHSession("Silver Server", "10.0.0.57", "user", "password")

ls_command = Command("ls -la")
ps_command = Command("ps -ax")

commands = [
    ls_command,
    ps_command
]

ssh_session.open_ssh_session()

for command in commands:
    ssh_session.run_command_in_ssh_session(command)

ssh_session.close_ssh_session()

command_output_dictionary = ssh_session.get_command_output_dictionary(ps_command)

standard_output_lines = command_output_dictionary["standard_output_lines"]
standard_error_lines = command_output_dictionary["standard_error_lines"]
exit_status = command_output_dictionary["exit_status"]
```

## Example 2: Using the `SSHSessionManager`

```python
#!/usr/bin/env python

from ssh_session_manager.Command import Command
from ssh_session_manager.SSHSession import SSHSession
from ssh_session_manager.SSHSessionManager import SSHSessionManager


ssh_session_1 = SSHSession("Silver Server", "10.0.0.57", "user", "password")
ssh_session_2 = SSHSession("Black Server", "10.0.0.57", "user", "password")

ssh_sessions = [
    ssh_session_1,
    ssh_session_2
]

ls_command = Command("ls -la")
ps_command = Command("ps -ax")

commands = [
    ls_command,
    ps_command
]

ssh_session_manager = SSHSessionManager(ssh_sessions)
ssh_session_manager.open_all_ssh_sessions()
ssh_session_manager.run_commands_in_ssh_sessions(commands)
ssh_session_manager.close_all_ssh_sessions()

command_output_dictionary = ssh_session_manager.get_command_output_dictionary(ssh_session_1, ls_command)

standard_output_lines = command_output_dictionary["standard_output_lines"]
standard_error_lines = command_output_dictionary["standard_error_lines"]
exit_status = command_output_dictionary["exit_status"]
```
