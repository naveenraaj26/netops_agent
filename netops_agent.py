"""
Project: NetOps Sentinel
Track: Enterprise Agents
Description: An AI Agent for Network Troubleshooting using Google Gemini.
"""

import os
import subprocess
import platform
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# Ensure you set this environment variable before running!
# os.environ["GOOGLE_API_KEY"] = "YOUR_KEY_HERE"

if "GOOGLE_API_KEY" not in os.environ:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit(1)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- 2. CUSTOM TOOL DEFINITION ---
def ping_host(host_address: str):
    """
    Pings a specific network host (IP or Domain) to check reachability.
    
    Args:
        host_address: The IP address or domain name to ping (e.g., '8.8.8.8', 'google.com').
    """
    print(f"\n[SYSTEM TOOL] Executing Ping on: {host_address}...")
    
    # Detect OS to use correct ping parameter (-n for Windows, -c for Linux/Mac)
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    try:
        # Run the ping command (limit to 2 packets for speed)
        command = ['ping', param, '2', host_address]
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return f"SUCCESS: Host {host_address} is reachable.\nRaw Output:\n{result.stdout}"
        else:
            return f"FAILURE: Host {host_address} is NOT reachable.\nError Output:\n{result.stderr}"
            
    except Exception as e:
        return f"CRITICAL ERROR: Failed to execute tool. Details: {str(e)}"

tools_list = [ping_host]

# --- 3. AGENT SETUP ---
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    tools=tools_list,
    system_instruction=(
        "You are 'NetOps Sentinel', a Level 1 Network Operations Agent. "
        "Your goal is to help IT admins troubleshoot connectivity issues efficiently. "
        "RULES: "
        "1. When a user mentions a server, IP, or domain, ALWAYS use the 'ping_host' tool first to verify status. "
        "2. Do not hallucinate connectivity; rely strictly on the tool output. "
        "3. Summarize the tool output. If it succeeds, say 'Online'. If it fails, suggest checking firewalls or routing. "
        "4. Keep responses professional and concise."
    )
)

# --- 4. SESSION LOOP (MAIN) ---
def main():
    chat_session = model.start_chat(enable_automatic_function_calling=True)
    
    print("=============================================")
    print("   NETOPS SENTINEL - ENTERPRISE AGENT v1.0   ")
    print("=============================================")
    print("Agent: Ready. Which host or IP should I check?")
    
    while True:
        try:
            user_input = input("\nAdmin: ")
            
            if user_input.lower() in ['exit', 'quit', 'stop']:
                print("Agent: Session ended. Goodbye!")
                break
                
            response = chat_session.send_message(user_input)
            print(f"Agent: {response.text}")
            
        except Exception as e:
            print(f"Error during session: {e}")

if __name__ == "__main__":
    main()
