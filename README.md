# GitHub Copilot SDK — Python Practical Learning

This repository contains hands-on Python examples developed while learning the Microsoft/GitHub Copilot SDK in VS Code.

The examples cover application setup, conversations, tools, authentication, customization, streaming, and session management.

## Development Environment

- Windows
- Visual Studio Code
- Python 3.12
- Python virtual environment
- GitHub Copilot CLI
- Microsoft Copilot SDK for Python
- Git and GitHub

## Topics Practiced

| Topic | Practical implementation |
| --- | --- |
| Basic SDK workflow | Started a client, created a session, sent a prompt, and printed the response |
| Client lifecycle | Practiced starting and stopping the Copilot client |
| Conversation context | Sent follow-up prompts within the same session |
| Streaming | Displayed response text as it arrived |
| Streaming events | Observed response and session lifecycle events |
| Custom tools | Created a Celsius-to-Fahrenheit conversion tool |
| Hooks | Observed session activity using hook callbacks |
| Custom agents | Configured an agent with specific instructions |
| MCP servers | Connected local servers exposing book and student lookup tools |
| Skills | Created reusable instructions for work updates and meeting summaries |
| Plugin directories | Loaded skills packaged in a local plugin directory |
| System messages | Customized response style and behavior |
| External CLI server | Connected a Python application to a separately running runtime |
| Telemetry | Generated and inspected local trace records |
| Session limits | Configured an execution limit |
| Image input | Sent an image with a prompt |
| Steering | Sent additional instructions while a response was in progress |
| Queueing | Queued follow-up requests |
| Session persistence | Saved a session ID and resumed the conversation in another run |
| GitHub OAuth | Authenticated a user and made a Copilot request through FastAPI |
| Fleet Mode | Observed sub-agent activity and combined results |

## Project Files

The repository includes the following learning examples:

| File or directory | Purpose |
| --- | --- |
| `main.py` | Basic client, session, and prompt workflow |
| `conversation.py` | Follow-up prompts and conversation context |
| `streaming_demo.py` | Streaming response text |
| `streaming_events_demo.py` | Streaming and session events |
| `temperature.py` | Custom temperature conversion tool |
| `hooks_demo.py` | Hook callbacks |
| `custom_agent_demo.py`, `custom_agent.py` | Custom agent examples |
| `book_server.py`, `mcp_demo.py` | Book lookup through a local MCP server |
| `student_server.py`, `student_app.py` | Student lookup through a local MCP server |
| `skills/` | Skill instructions stored in `SKILL.md` files |
| `skills_demo.py`, `meeting_skill_demo.py` | Skill usage examples |
| `plugins/` | Local plugin contents |
| `plugin_demo.py`, `plugin_directory_demo.py` | Plugin loading examples |
| `system_message.py`, `system_message_practice.py` | System message examples |
| `external_server_demo.py` | Connection to an external runtime |
| `telemetry_demo.py` | Local telemetry example |
| `session_limits_demo.py` | Session execution limit configuration |
| `steering_demo.py` | Additional instructions during processing |
| `queueing_demo.py` | Queued follow-up requests |
| `save_session.py`, `resume_session.py` | Session persistence examples |
| `remote_session.py` | Remote session export experiment |
| `cloud_session.py` | Cloud session experiment |
| `fleet.py` | Fleet Mode example |
| `oauth_demo.py` | GitHub OAuth and Copilot integration |
| `requirements.txt` | Python dependencies |

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/somunarendar1585/Agentic_AI.git
cd Agentic_AI
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

The virtual environment keeps this project's dependencies separate from other Python projects.

### 3. Activate the environment

In PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

In Git Bash:

```bash
source .venv/Scripts/activate
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

These examples were developed using `microsoft-copilot-sdk==2.0.0rc2`. SDK APIs and runtime compatibility can vary between releases.

### 5. Verify Copilot CLI authentication

```powershell
copilot --version
copilot
```

Inside the interactive CLI, use `/login` if authentication is required.

Copilot access depends on the signed-in account's subscription and organization policies.

## Run the Basic Application

```powershell
python main.py
```

The application:

1. Creates a Copilot client.
2. Starts the runtime connection.
3. Creates a conversation session.
4. Sends a prompt.
5. Prints the response.
6. Stops the client.

Other examples can be run individually:

```powershell
python conversation.py
python streaming_demo.py
python temperature.py
python hooks_demo.py
python student_app.py
python skills_demo.py
python fleet.py
```

Review each script before running it. Some examples need additional files, configuration, or permissions.

## MCP Server Examples

The MCP examples expose local Python functions as tools that Copilot can call.

For example, the student application connects to `student_server.py` and requests student information.

```powershell
python student_app.py
```

When the application is configured to launch its MCP server through stdio, it starts the server automatically.

## GitHub OAuth Example

The OAuth example uses FastAPI to sign in with GitHub and make a Copilot request using the authenticated user's access token.

### Configuration

Register a GitHub OAuth application with:

- Homepage URL: `http://127.0.0.1:8000`
- Authorization callback URL: `http://127.0.0.1:8000/auth/callback`

Create a local `.env` file:

```dotenv
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
```

Do not commit this file.

### Start the application

```powershell
python -m uvicorn oauth_demo:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/login
```

### Authentication flow

1. The application redirects the browser to GitHub.
2. The user authorizes the application.
3. GitHub redirects to the callback with an authorization code.
4. The backend validates the login state and exchanges the code for an access token.
5. The backend retrieves the GitHub username.
6. The application uses the token to make a Copilot request.
7. FastAPI returns the username and generated answer.

The access token is not included in the browser response.

This is a local learning example, rather than a production authentication implementation.

## Session Persistence

Run:

```powershell
python save_session.py
python resume_session.py
```

The first application saves the session ID locally. The second uses that ID to resume the conversation.

The session ID file is a reference to the session; it does not contain the complete conversation.

## External Runtime Example

For the external server exercise, start the runtime in one terminal:

```powershell
copilot --headless --port 4321
```

In another terminal, activate the virtual environment and run:

```powershell
python external_server_demo.py
```

The client script must be configured to connect to the same host and port.

## Validation Completed

- Received responses from a Python application through the SDK.
- Verified follow-up conversation context.
- Observed streamed text and session events.
- Executed a custom temperature conversion tool.
- Retrieved information through local MCP tools.
- Tested custom agents, skills, and plugin directories.
- Completed GitHub OAuth login and returned a Copilot response through FastAPI.
- Resumed a conversation across separate application runs.
- Observed Fleet Mode sub-agent activity and combined results.
- Generated local telemetry records.

## Limitations and Pending Work

- **Remote sessions:** Export was blocked because remote sessions were not enabled for the account or organization.
- **Cloud sessions:** Session creation returned `JSON-RPC Error -32601: Unhandled method session.create`. Successful cloud execution has not been verified.
- **Session limits:** Configuration was practiced; limit exhaustion was not verified.
- Some examples approve permission requests automatically for local exercises. Review their permission settings before reusing them with other tools or data.
- Prompts can produce different wording across runs.

## Files Excluded from Git

Keep local credentials, environments, and generated session data out of version control.

Suggested `.gitignore` entries:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
traces.jsonl
saved_session_id.txt
```

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `ModuleNotFoundError` | Activate `.venv` and install the required dependencies |
| Cannot find a Python file | Run the command from the project folder and confirm the file is saved |
| Pylance warns about `response.data.content` | Check that the response data is `AssistantMessageData` before accessing `content` |
| MCP tool is unavailable | Check the server path, Python interpreter, installed dependencies, and registered tool name |
| GitHub authentication fails | Verify CLI login or the OAuth application configuration |
| Remote session URL is missing | Inspect the returned warning and account or organization policies |
| JSON-RPC method is unhandled | Check SDK and runtime compatibility |

## References

- [Copilot SDK repository](https://github.com/microsoft/copilot-sdk)
- [SDK documentation](https://github.com/microsoft/copilot-sdk/blob/main/docs/README.md)
- [Platform feature documentation](https://github.com/microsoft/copilot-sdk/tree/main/docs/features)
