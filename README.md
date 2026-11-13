# JARVIS — Personal AI Assistant / Voice OS

JARVIS is a personal assistant project exploring a voice-first interface backed by Python and a local large language model (LLM). The goal is to build a practical, modular assistant that can understand spoken requests, reason locally, and respond naturally.

> **Project status:** Early planning stage. This repository currently contains this README; the application, integrations, and setup process have not been implemented yet. Sections marked as planned describe the intended direction, not working features.

## Project goals

- Build a voice-first personal assistant.
- Use OpenWhispr for the voice interaction layer, subject to confirming the exact integration and supported platforms.
- Use Python for application orchestration and assistant logic.
- Use a local LLM for language understanding and response generation.
- Keep components modular so speech, model, and assistant logic can evolve independently.

## Planned architecture

The intended request path is:

1. The user speaks through the OpenWhispr voice interface.
2. The voice layer provides the recognized request to the Python application.
3. Python prepares the conversation context and sends a prompt to the configured local LLM.
4. The model response returns to Python for handling and formatting.
5. The assistant responds through the available text or voice output.

User voice ↔ OpenWhispr voice interface ↔ Python assistant orchestration ↔ Local LLM response generation

This is a design outline. The transport between components, model runtime, audio formats, and supported operating systems are still to be selected and documented.

## Technology direction

| Component | Intended role | Current decision |
|---|---|---|
| OpenWhispr | Voice interaction | Proposed; integration details to be confirmed |
| Python | Application and assistant logic | Planned |
| Local LLM | On-device language model | Planned; model and runtime not selected |

No model name, hardware requirement, package list, or install command is specified yet. These will be added once the first implementation choices are made and tested.

## Development roadmap

1. Confirm the OpenWhispr integration path and target operating system.
2. Choose a local model runtime and define how Python will call it.
3. Build a minimal request-and-response loop and document verified setup steps.
4. Add voice input and output, including clear handling for unavailable devices or services.
5. Explore assistant capabilities such as conversation context and optional tools, documenting permissions and limitations before enabling them.
6. Add tests, configuration guidance, and troubleshooting notes as each feature becomes available.

## Privacy and configuration

Local model inference is the intended direction. Complete privacy behavior will depend on the selected voice interface and other integrations; it should be verified before describing the system as fully offline. Do not commit passwords, API keys, access tokens, or other secrets. Future configuration examples should use placeholders and explain where local settings belong.

## Repository contents

- README.md — project overview, current status, and planned direction.

Application code and installation instructions will be added as they are implemented.

## Contributing

This project is at the planning stage. Issues and pull requests can help shape the architecture. Please describe the proposed change, its intended behavior, and any external services or permissions it needs.

## License

No license has been selected yet. Until one is added, the repository does not grant general permission to reuse or redistribute its contents.
