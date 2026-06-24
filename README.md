# LAIS (Large Action Integration System) Clone

A multi-agent system built with a robust communication protocol, 4-layer memory, and extensive OSINT capabilities.

## Architecture

- **ACP Bus (Agent Communication Protocol):** JSON file-based message queue with `portalocker` file locking.
- **Agents:**
  - **OpenCode (CLI):** Handles file operations within `workspace/`.
  - **AI Engine (GUI):** Tkinter-based dashboard for orchestration and status.
  - **JARVIS (Voice):** Voice interaction via `speech_recognition` and `pyttsx3` (with mock fallback).
- **Memory System:**
  - **Hot:** In-memory RAM cache.
  - **Warm:** JSON-based persistent storage.
  - **Cold:** Archived data.
  - **Crystallized:** Knowledge Graph using `NetworkX`.
- **MCP Bridge:** Connector for tool discovery and execution via Model Context Protocol.
- **Security Grid:** 9-agent modular security service (Authentication, Permissions, I/O, Rate Limiting, Auditing, Anomaly, Incident Response).
- **Token Optimization:** 4 compression engines (Extractive, Keyword, Semantic, Query-Aware).
- **Obsidian Integration:** Bi-directional sync with `obsidian_vault/`.

## OSINT Capabilities

Integrated `osint-mcp-server` providing 37 tools across 12 data sources.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the system: `python src/main.py` (TBD)
