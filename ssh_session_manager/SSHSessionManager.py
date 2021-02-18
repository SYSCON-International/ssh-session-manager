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

    # def download_file_from_all_sessions(self, remote_source_file_path, local_target_file_path):
    #     for ssh_session in self.ssh_sessions:
    #         # Will need to figure out how to resolve names of same file (probably by appending it with "_<number>"
    #         ssh_session.download_file(self, remote_source_file_path, local_target_file_path)

    def upload_file_to_all_sessions(self, local_source_file_path, remote_target_file_path):
        for ssh_session in self.ssh_sessions:
            ssh_session.upload_file(local_source_file_path, remote_target_file_path)
