"""SSH transport used by the MCP tools."""

from __future__ import annotations

import os
from dataclasses import dataclass

import paramiko


@dataclass
class SSHResult:
    stdout: str
    stderr: str
    exit_code: int


class KaliSSH:
    def __init__(self, host: str, port: int, username: str, key_path: str, timeout: float = 10) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.key_path = os.path.expanduser(key_path)
        self.timeout = timeout

    def _connect(self) -> paramiko.SSHClient:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(
            hostname=self.host,
            port=self.port,
            username=self.username,
            key_filename=self.key_path,
            timeout=self.timeout,
            banner_timeout=self.timeout,
            auth_timeout=self.timeout,
        )
        return client

    def exec(self, command: str) -> SSHResult:
        client = self._connect()
        try:
            _, stdout, stderr = client.exec_command(command, timeout=self.timeout)
            exit_code = stdout.channel.recv_exit_status()
            return SSHResult(
                stdout=stdout.read().decode("utf-8", errors="replace"),
                stderr=stderr.read().decode("utf-8", errors="replace"),
                exit_code=exit_code,
            )
        finally:
            client.close()

    def read_file(self, path: str) -> str:
        client = self._connect()
        try:
            with client.open_sftp().open(path, "r") as handle:
                return handle.read().decode("utf-8", errors="replace")
        finally:
            client.close()

    def write_file(self, path: str, content: str) -> None:
        client = self._connect()
        try:
            with client.open_sftp().open(path, "w") as handle:
                handle.write(content.encode("utf-8"))
        finally:
            client.close()

    def status(self) -> SSHResult:
        return self.exec("hostname; printf '\\n'; id -un; printf '\\n'; uname -a")
