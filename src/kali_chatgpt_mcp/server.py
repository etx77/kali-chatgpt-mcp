"""MCP server exposing controlled operations on Kali over SSH."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .ssh import KaliSSH

load_dotenv()

mcp = FastMCP("kali-chatgpt-mcp")

ssh = KaliSSH(
    host=os.getenv("KALI_SSH_HOST", "127.0.0.1"),
    port=int(os.getenv("KALI_SSH_PORT", "22")),
    username=os.getenv("KALI_SSH_USER", "kali"),
    key_path=os.getenv("KALI_SSH_KEY", "~/.ssh/kali_chatgpt_mcp"),
    timeout=float(os.getenv("KALI_SSH_TIMEOUT", "10")),
)


@mcp.tool()
def kali_exec(command: str) -> str:
    """Execute a command on the authorized Kali host and return the real result."""
    result = ssh.exec(command)
    return f"exit_code={result.exit_code}\n--- stdout ---\n{result.stdout}--- stderr ---\n{result.stderr}"


@mcp.tool()
def kali_read_file(path: str) -> str:
    """Read a UTF-8 text file from Kali."""
    return ssh.read_file(path)


@mcp.tool()
def kali_write_file(path: str, content: str) -> str:
    """Write UTF-8 text content to Kali."""
    ssh.write_file(path, content)
    return f"wrote {len(content.encode('utf-8'))} bytes to {path}"


@mcp.tool()
def kali_status() -> str:
    """Check SSH connectivity and identify the remote Kali host."""
    result = ssh.status()
    return f"exit_code={result.exit_code}\n{result.stdout}{result.stderr}"


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
