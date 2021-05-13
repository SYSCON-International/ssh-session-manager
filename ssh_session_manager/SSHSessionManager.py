import threading
from functools import cache


class SSHSessionManager:
    def __init__(self, ssh_sessions):
        self.ssh_sessions = ssh_sessions

    def open_all_ssh_sessions(self):
        for ssh_session in self.ssh_sessions:
            ssh_session.open_ssh_session()

    def close_all_ssh_sessions(self):
        for ssh_session in self.ssh_sessions:
            ssh_session.close_ssh_session()

    def run_commands_in_ssh_sessions(self, commands, should_print_output=True):
        threads = []
        session_output_lock = threading.Lock()

        for ssh_session in self.ssh_sessions:
            thread = threading.Thread(target=SSHSessionManager.__run_commands_in_ssh_sessions_thread_main, args=(ssh_session, commands, should_print_output, session_output_lock))
            thread.start()

            threads.append(thread)

        for thread in threads:
            thread.join()

    @staticmethod
    def __run_commands_in_ssh_sessions_thread_main(ssh_session, commands, should_print_output, session_output_lock):
        for command in commands:
            ssh_session.run_command_in_ssh_session(command, should_print_output=should_print_output, session_output_lock=session_output_lock)

    def get_command_output_information_dictionary(self, ssh_session, command):
        if ssh_session in self.ssh_sessions:
            command_output_information_dictionary = ssh_session.get_command_output_information_dictionary(command)
        else:
            command_output_information_dictionary = None

        return command_output_information_dictionary

    def upload_file_to_all_sessions(self, local_source_file_path, remote_target_file_path):
        for ssh_session in self.ssh_sessions:
            ssh_session.upload_file(local_source_file_path, remote_target_file_path)

    @cache
    def ping_all_cached(self):
        return self.ping_all()

    def ping_all(self):
        ping_dictionary = {}
        threads = []

        for ssh_session in self.ssh_sessions:
            thread = threading.Thread(target=SSHSessionManager.__ping_all_thread_main, args=(ssh_session, ping_dictionary))
            thread.start()

            threads.append(thread)

        for thread in threads:
            thread.join()

        return ping_dictionary

    # A basic wrapper function so that I dont have to add thread-specific modifications to `SSHSession.ping_cached()`
    @staticmethod
    def __ping_all_thread_main(ssh_session, ping_result_dictionary):
        ping_was_successful = ssh_session.ping()
        ping_result_dictionary[ssh_session] = ping_was_successful
