import os
import platform
import subprocess
from functools import cache
from pathlib import PurePosixPath

import paramiko


class SSHSession:
    OPEN_SSH_SESSION_WITH_PARAMIKO_TEXT = "Open SSH session with Paramiko"
    CLOSE_SSH_SESSION_WITH_PARAMIKO_TEXT = "Close SSH session with Paramiko"

    def __init__(self, name, ip_address, username, password, port=22):
        self.name = name
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.port = port

        self.paramiko_ssh_client = None

        self.standard_input_stream = None
        self.standard_output_stream = None
        self.standard_error_stream = None

        self.session_opened_successfully = None

        self.command_to_command_output_information_dictionary = {}

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    def open_ssh_session(self):
        self.__information_print("Opening SSH session", SSHSession.OPEN_SSH_SESSION_WITH_PARAMIKO_TEXT)

        try:
            paramiko_ssh_client = paramiko.SSHClient()
            paramiko_ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            paramiko_ssh_client.connect(self.ip_address, username=self.username, password=self.password, port=self.port)

            self.paramiko_ssh_client = paramiko_ssh_client
            self.session_opened_successfully = True
        except OSError as os_error:
            self.__information_print(
                f"Session failed to open with error: \"{os_error}\".  All future operations for this session be skipped.", SSHSession.CLOSE_SSH_SESSION_WITH_PARAMIKO_TEXT
            )
            self.session_opened_successfully = False

    def close_ssh_session(self):
        if self.session_opened_successfully:
            self.__information_print("Closing SSH session", SSHSession.CLOSE_SSH_SESSION_WITH_PARAMIKO_TEXT)

            if self.standard_input_stream:
                self.standard_input_stream.close()

            if self.standard_output_stream:
                self.standard_output_stream.close()

            if self.standard_error_stream:
                self.standard_error_stream.close()

            if self.paramiko_ssh_client:
                self.paramiko_ssh_client.close()

    def run_command_in_ssh_session(self, command, should_print_output=True, session_output_lock=None):
        if self.session_opened_successfully:
            try:
                self.standard_input_stream, self.standard_output_stream, self.standard_error_stream = self.paramiko_ssh_client.exec_command(command.command_to_execute)

                if command.command_user_input is not None:
                    self.standard_input_stream.write(command.command_user_input)
                    self.standard_input_stream.flush()

                self.__get_output_information_dictionary(command, should_print_output=should_print_output, session_output_lock=session_output_lock)
            except EOFError as eof_error:
                self.__information_print(f"Command failed to run with error: \"{eof_error}\".", command)

    def upload_file(self, local_source_file_path, remote_target_file_path, should_make_missing_directories=True):
        sftp_client = self.paramiko_ssh_client.open_sftp()

        if should_make_missing_directories:
            remote_target_file_path = PurePosixPath(remote_target_file_path)
            self.__makedirs(sftp_client, str(remote_target_file_path.parent))

        sftp_client.put(str(local_source_file_path), str(remote_target_file_path))

        self.__information_print("Uploading file", f"Uploading {local_source_file_path.name}")

        sftp_client.close()

    # Taken from: https://stackoverflow.com/a/14819803
    def __makedirs(self, sftp, remote_directory):
        """
        Change to this directory, recursively making new folders if needed.
        Returns True if any folders were created.
        """

        if remote_directory == "/":
            # Absolute path so change directory to root
            sftp.chdir("/")
            return

        if remote_directory == "":
            # Top-level relative directory must exist
            return

        try:
            sftp.chdir(remote_directory) # Sub-directory exists
        except IOError:
            directory_name, base_name = os.path.split(str(remote_directory.rstrip("/")))
            self.__makedirs(sftp, directory_name) # Make parent directories
            sftp.mkdir(base_name) # Sub-directory missing, so created it
            sftp.chdir(base_name)

            return True

    @cache
    def ping_cached(self):
        return self.ping()

    # Based on: https://stackoverflow.com/a/32684938
    def ping(self):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        if platform.system().lower() == "windows":
            ping_system_parameter = "n"
        else:
            ping_system_parameter = "c"

        ping_command = ["ping", f"-{ping_system_parameter}", "1", self.ip_address]

        # Use `subprocess.DEVNULL` to suppress ping output
        ping_was_successful = subprocess.call(ping_command, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL) == 0

        return ping_was_successful

    # TODO: Consider the idea of returning this after running `run_command_in_ssh_session()` and from `run_commands_in_all_ssh_sessions()` instead of storing it
    # Not sure which solution is better
    def get_command_output_information_dictionary(self, command):
        return self.command_to_command_output_information_dictionary.get(command, None)

    # This function blocks this thread's execution until standard output, standard error, and the exit code is returned, so that the thread doesn't exit before the command in the
    # session finishes
    def __get_output_information_dictionary(self, command, should_print_output, session_output_lock):
        if should_print_output and session_output_lock:
            with session_output_lock:
                self.__information_print("Running command", command)
                standard_output_lines = SSHSession.__capture_output(self.standard_output_stream, should_print_output)
                standard_error_lines = SSHSession.__capture_output(self.standard_error_stream, should_print_output)
        else:
            self.__information_print("Running command", command)
            standard_output_lines = SSHSession.__capture_output(self.standard_output_stream, should_print_output)
            standard_error_lines = SSHSession.__capture_output(self.standard_error_stream, should_print_output)

        command_output_information_dictionary = {
            "standard_output_lines": standard_output_lines,
            "standard_error_lines": standard_error_lines,
            "exit_status": self.standard_output_stream.channel.recv_exit_status()
        }

        self.command_to_command_output_information_dictionary[command] = command_output_information_dictionary

    def __information_print(self, summary, command, border_symbol="*"):
        summary = f"{border_symbol} Summary: {summary} "
        command = f"{border_symbol} Command: {command} "
        ssh_session = f"{border_symbol} SSH Session: {self} "

        lines = [summary, command, ssh_session]
        longest_line_length = len(max(lines, key=len))

        summary = summary.ljust(longest_line_length) + border_symbol
        command = command.ljust(longest_line_length) + border_symbol
        ssh_session = ssh_session.ljust(longest_line_length) + border_symbol

        longest_line_length += len(border_symbol)

        border_line = border_symbol * longest_line_length

        print()
        print(border_line)
        print(summary)
        print(command)
        print(ssh_session)
        print(border_line)
        print()

    @staticmethod
    def __capture_output(stream, should_print_output):
        output_lines = []

        while True:
            try:
                output_line = stream.readline()
            except UnicodeDecodeError:
                # Should we output that a line was omitted?
                continue

            if not output_line:
                break

            if should_print_output:
                print(output_line, end="")

            output_lines.append(output_line)

        return output_lines
