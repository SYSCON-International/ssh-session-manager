# ssh_session_manager

Execute commands on multiple remote SSH sessions

[PyPI](https://pypi.org/project/ssh-session-manager/)


## Example 1: Using the `SSHSession`

```python
from ssh_session_manager.Command import Command
from ssh_session_manager.SSHSession import SSHSession


ls_command = Command("ls -la")
ps_command = Command("ps -ax")

commands = [
    ls_command,
    ps_command
]

with SSHSession("Silver Server", "10.0.0.57", "user", "password") as ssh_session:
    for command in commands:
        ssh_session.run_command_in_ssh_session(command)

command_output_dictionary = ssh_session.get_command_output_dictionary(ps_command)

standard_output_lines = command_output_dictionary["standard_output_lines"]
standard_error_lines = command_output_dictionary["standard_error_lines"]
exit_status = command_output_dictionary["exit_status"]
```

## Example 2: Using the `SSHSessionManager`

```python
from ssh_session_manager.Command import Command
from ssh_session_manager.SSHSession import SSHSession
from ssh_session_manager.SSHSessionManager import SSHSessionManager


ssh_session_1 = SSHSession("Silver Server", "10.0.0.57", "user", "password")
ssh_session_2 = SSHSession("Black Server", "10.0.0.58", "user", "password")

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

with SSHSessionManager(ssh_sessions) as ssh_session_manager
    ssh_session_manager.run_commands_in_ssh_sessions(commands)

command_output_dictionary = ssh_session_manager.get_command_output_dictionary(ssh_session_1, ls_command)

standard_output_lines = command_output_dictionary["standard_output_lines"]
standard_error_lines = command_output_dictionary["standard_error_lines"]
exit_status = command_output_dictionary["exit_status"]
```
