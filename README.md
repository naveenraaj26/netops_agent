NetOps Sentinel: AI-Powered Network Troubleshooting Agent
Track: Enterprise Agents
Course: Google 5-Day AI Agents Intensive (Capstone Project)
📖 Project Overview
NetOps Sentinel is an automated "Level 1 Network Analyst" designed to streamline the initial diagnosis of network connectivity issues. Powered by Google Gemini 1.5 and the Agent Development Kit (ADK) concepts, it bridges the gap between natural language requests and low-level system diagnostic tools.
Instead of manually running multiple CLI commands (ping, traceroute, etc.) and interpreting raw logs, IT administrators can simply ask the agent to "Check the status of the gateway" or "Verify connectivity to the backup server," receiving instant, synthesized reports in return.
🛑 The Problem
In modern Enterprise IT environments, "Time to Resolution" (TTR) is a critical metric. Network Engineers often face:
•	Alert Fatigue: Floods of alerts that require manual verification.
•	Context Switching: Constant shifting between ticketing systems (Jira/ServiceNow) and terminals to run basic diagnostics.
•	Repetitive Tasks: Level 1 troubleshooting (e.g., verifying if a host is up) consumes disproportionate time, distracting from complex root-cause analysis.
💡 The Solution
NetOps Sentinel acts as an intelligent command-line interface (CLI) assistant. It does not just "chat"; it has agency. It can execute real system subprocesses to gather ground-truth data from the network stack and use LLM reasoning to interpret the results.
Key Capabilities
•	Autonomous Tool Execution: Automatically runs ping (and extensible to other tools) based on user intent.
•	OS-Agnostic: Detects the operating system (Windows/Linux) to format commands correctly.
•	Result Synthesis: Translates technical error codes (e.g., "Request Timed Out", "Destination Host Unreachable") into plain English summaries.
🏗️ Technical Architecture
The agent follows a ReAct (Reason + Act) loop pattern. It receives a query, decides if a tool is needed, executes the Python function, and summarizes the output.
sequenceDiagram
    participant User
    participant Agent as NetOps Agent (Gemini)
    participant Tool as Custom Tool (Ping)
    participant OS as Operating System

    User->>Agent: "Is 8.8.8.8 reachable?"
    Note over Agent: Analysis: Intent requires<br/>connectivity check.
    Agent->>Tool: Call ping_host("8.8.8.8")
    Tool->>OS: subprocess.run(["ping", "8.8.8.8"])
    OS-->>Tool: Raw stdout (packets/latency)
    Tool-->>Agent: Return formatted string
    Note over Agent: Synthesis: 0% packet loss<br/>= "Online"
    Agent-->>User: "Success: 8.8.8.8 is online."

🚀 Key Features (Course Concepts)
This project demonstrates three core concepts from the Google AI Agents Intensive curriculum:
1. Custom Tools
I implemented a Python function ping_host() that interfaces directly with the subprocess module. This gives the agent "hands" to interact with the outside world (the OS network stack), moving beyond a passive text generator to an active agent.
2. Sessions & Memory
The agent utilizes a persistent chat_session object. This enables stateful interactions.
•	User: "Ping 192.168.1.1" -> Agent: "It's online."
•	User: "What about the secondary gateway?" -> Agent: (Understands context implies pinging the new IP).
3. Agent Context Engineering
The system_instruction is carefully crafted to define a "Network Operations Expert" persona. It includes strict guardrails:
•	Factuality: Never hallucinate connectivity; rely strictly on tool output.
•	Safety: Only execute commands on explicitly requested hosts.
•	Format: Provide professional, concise summaries suitable for IT logs.
💻 Installation & Usage
Prerequisites
•	Python 3.9+
•	A Google Cloud API Key (Gemini)
Steps
1.	Clone the repository:
2.	git clone <our repo>
3.	cd netops-sentinel

4.	Install dependencies:
5.	pip install google-generativeai

6.	Set your API Key:
o	Option A: Set as environment variable (Recommended):
o	export GOOGLE_API_KEY="your_api_key_here"

o	Option B: Edit netops_agent.py directly (for local testing only).
7.	Run the Agent:
8.	python netops_agent.py

Example Usage
NetOps Sentinel Online
Admin: Check if google.com is reachable.
Agent: [Tool Running] Pinging google.com...
       SUCCESS: Host google.com is reachable.
       
Admin: Try 192.168.55.55
Agent: [Tool Running] Pinging 192.168.55.55...
       FAILURE: Host is unreachable. Request timed out.
       Suggestion: Check local firewall rules or VPN connection.

🔮 Future Roadmap
•	Traceroute Integration: To identify exactly where a connection drops.
•	Log Parsing: Ability to read local syslog files for error patterns.
•	Jira Integration: Automatically create a ticket if a critical server is confirmed down.

