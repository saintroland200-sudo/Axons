# Agent Instructions

This repository follows a strict multi-agent architecture.

## Guidelines

- **Communication:** All agents MUST communicate via the ACP Bus. Direct function calls between agents are prohibited.
- **Security:** Every request must pass through the Security Grid.
- **Memory:** Use the 4-layer memory system for all persistence needs.
- **File Access:** Only `OpenCode` should perform file operations in the `workspace/` directory.
- **Design:** Follow the modular structure in `src/`.
