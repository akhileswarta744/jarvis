# JARVIS — Personal AI Assistant / Voice OS

A small, local-first JARVIS starter for Windows. It combines OpenWhispr dictation, a Python chat loop, and a local language model served by Ollama. The starter is intentionally simple: dictate or type a request in the terminal and receive a text response from the local model.

## What works now

- Terminal chat with conversation context while the program is running.
- Local model requests through Ollama's HTTP API.
- OpenWhispr speech-to-text by dictating at the terminal prompt.
- `/reset` clears the current conversation; `/quit` exits.
- No Python packages are required; the program uses the Python standard library.

## What is not implemented yet

JARVIS does not yet speak responses aloud, listen for a wake word, control the computer, call external tools, or save conversation history between runs. Do not treat model output as an action. These are future project options, not current features.

## How the pieces fit together

1. OpenWhispr transcribes your speech and pastes the text at the active terminal cursor.
2. You press Enter to submit the text to JARVIS.
3. Python sends the conversation to Ollama at the local address in your configuration.
4. Ollama runs the selected model on your computer and returns a text response.
5. JARVIS prints the response in the terminal.

OpenWhispr dictation is a separate desktop app, not a Python dependency or direct API integration in this starter. Its transcription and cleanup settings control how audio is processed. Choose a local speech model in OpenWhispr if you want speech transcription to stay on-device; verify its current settings before using sensitive audio.

## Requirements

- Windows 10 or 11 (the commands below use PowerShell).
- Python 3.10 or newer.
- Git, to clone the repository.
- Ollama for Windows, with a local model downloaded.
- OpenWhispr for Windows, optional for voice input; typed chat works without it.

The model needs several gigabytes of disk space and enough available memory for your machine. Smaller models use fewer resources but may give simpler answers. Ollama's model page lists current sizes and variants.

## Setup on Windows

### 1. Install Ollama and download a model

Install Ollama from [ollama.com/download](https://ollama.com/download) and start the Ollama app. In PowerShell, download a small starter model:

~~~powershell
ollama pull qwen3.5:2b
~~~

Confirm the model runs:

~~~powershell
ollama run qwen3.5:2b
~~~

Type a short question, then enter `/bye` to leave Ollama's interactive chat. The JARVIS app uses Ollama's local `/api/chat` endpoint; Ollama normally listens at `http://127.0.0.1:11434`.

If the model is too slow or does not fit your available memory, choose a smaller variant from the [Ollama Qwen 3.5 model page](https://ollama.com/library/qwen3.5) and set that exact model name in `.env`.

### 2. Install OpenWhispr for voice input (optional)

Install OpenWhispr from [openwhispr.com](https://openwhispr.com/). Open its settings and check the dictation shortcut for Windows; shortcuts can vary by version or configuration. OpenWhispr's [dictation guide](https://docs.openwhispr.com/guides/dictation) explains the hotkey and paste behavior. For on-device speech recognition, open Settings > AI Models > Speech-to-Text > Dictation > Local in OpenWhispr, choose a local model such as Orukeet, and download it. The [local models guide](https://docs.openwhispr.com/guides/local-models) explains the current options.

### 3. Clone JARVIS and create a virtual environment

~~~powershell
git clone https://github.com/akhileswarta744/jarvis.git
cd jarvis
py -3.10 -m venv .venv
~~~

If you have a newer Python release, replace `-3.10` with its installed version, or use `py -m venv .venv`. Activate the environment:

~~~powershell
..venvScriptsActivate.ps1
~~~

If PowerShell blocks activation, you can run JARVIS using the environment's Python directly in the next step; changing the system execution policy is not required.

### 4. Configure the Ollama model

Create your local configuration file from the example:

~~~powershell
Copy-Item .env.example .env
~~~

The starter defaults are:

~~~text
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=qwen3.5:2b
OLLAMA_TIMEOUT_SECONDS=120
~~~

Edit `.env` if your Ollama address or model differs. `.env` is excluded from Git so local settings stay out of commits.

### 5. Start JARVIS

With the virtual environment activated:

~~~powershell
python jarvis.py
~~~

Or, without activating it:

~~~powershell
..venvScriptspython.exe jarvis.py
~~~

No `requirements.txt` install step is needed because the current starter has no third-party Python dependencies.

## Using voice input

1. Start JARVIS and leave the terminal focused at the `You:` prompt.
2. Press your configured OpenWhispr dictation shortcut, speak, and stop dictation.
3. Check the transcribed text in the terminal, then press Enter to send it to the local model.
4. Type `/reset` to clear conversation context or `/quit` to exit.

Dictation pastes text into whichever app has focus. Keep the JARVIS terminal focused while dictating.

## Configuration

| Setting | Default | Purpose |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Base address of the local Ollama service |
| `OLLAMA_MODEL` | `qwen3.5:2b` | Model tag installed in Ollama |
| `OLLAMA_TIMEOUT_SECONDS` | `120` | Maximum wait for each response |

Settings can be placed in the ignored `.env` file or supplied as environment variables. Do not add API keys, passwords, or personal secrets to this public repository.

## Project files

- `jarvis.py` — terminal conversation loop and Ollama API client.
- `.env.example` — safe sample settings; copy it to `.env`.
- `.gitignore` — excludes local settings, virtual environments, and Python cache files.
- `README.md` — setup and usage guide.

## Troubleshooting

- **Could not reach Ollama:** Open the Ollama app, confirm it is running, and check `OLLAMA_BASE_URL`. The default local endpoint is `http://127.0.0.1:11434`.
- **Model not found:** Run `ollama pull qwen3.5:2b`, or set `OLLAMA_MODEL` to the exact tag you installed.
- **Responses time out:** Give the model more time by increasing `OLLAMA_TIMEOUT_SECONDS`, or use a smaller model supported by your hardware.
- **Dictation goes to another window:** Refocus the terminal before using the OpenWhispr shortcut.
- **No dictation appears:** Check the OpenWhispr shortcut, microphone selection, transcription model, and Windows microphone permissions.

## Privacy notes

JARVIS sends prompts to the Ollama service at the configured address. With the default address and a local model, inference runs on your computer. Model downloads require an internet connection. Speech privacy depends on OpenWhispr's selected transcription and cleanup settings; cloud providers may process audio or text remotely. See OpenWhispr's [local model guide](https://docs.openwhispr.com/guides/local-models) and verify provider settings before dictating sensitive information.

## Roadmap

- Add spoken responses (text-to-speech).
- Add an optional wake-word flow.
- Add persistent memory with clear controls for what is saved and deleted.
- Add optional tools behind explicit confirmations and a reviewable permissions model.
- Add setup checks, tests, and platform-specific instructions as those features are implemented.

## License

No license has been selected. Until a license is added, this repository does not grant general permission to reuse or redistribute its contents.
