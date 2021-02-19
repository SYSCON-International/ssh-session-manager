class SSHSessionManager:
    def __init__(self, ssh_sessions):
        self.ssh_sessions = ssh_sessions

    def open_all_ssh_sessions(self):
        for ssh_session in self.ssh_sessions:
            ssh_session.open_ssh_session()

    def close_all_ssh_sessions(self):
        for ssh_session in self.ssh_sessions:
            ssh_session.close_ssh_session()

    def run_commands_in_all_ssh_sessions(self, commands):
        for command in commands:
            for ssh_session in self.ssh_sessions:
                ssh_session.run_command_in_ssh_session(command)

            for ssh_session in self.ssh_sessions:
                ssh_session.print_command_output(command)

    def upload_file_to_all_sessions(self, local_source_file_path, remote_target_file_path):
        for ssh_session in self.ssh_sessions:
            ssh_session.upload_file(local_source_file_path, remote_target_file_path)
