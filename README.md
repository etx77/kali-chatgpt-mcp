# kali-chatgpt-mcp

MCP server that exposes a controlled SSH connection to a Kali Linux VM.

The project is split into two layers:
- MCP layer: exposes tools to an AI client.
- SSH layer: connects to Kali and returns real command/file results.

Initial milestone: MCP -> SSH -> Kali.

Network access (reverse tunnel, VPN, or router NAT) will be added separately.

Planned tools:
- kali_exec — execute a command and return stdout/stderr/exit code
- kali_read_file — read a text file
- kali_write_file — write a text file
- kali_status — verify SSH connectivity

Copy .env.example to .env and configure the Kali SSH endpoint.

Use this project only on systems you are authorized to access. Use SSH keys and a restricted account.

Development:
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python -m kali_chatgpt_mcp.server

The network/tunnel design is deliberately not part of the first milestone.