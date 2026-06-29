import os
import sys
import json

def register_server():
    """
    Auto-register the freelance-pitch-engine MCP server across multiple AI clients:
    - Claude Desktop (OS-specific path)
    - Cursor (global config)
    - Generic fallback (user home directory)
    """
    # 1. Resolve OS-specific Claude Desktop config path
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            claude_path = None
        else:
            claude_path = os.path.join(appdata, "Claude", "claude_desktop_config.json")
    elif sys.platform == "darwin":
        claude_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:  # Linux / other Unix
        claude_path = os.path.expanduser("~/.config/Claude/claude_desktop_config.json")
        
    # Define targets
    targets = {
        "Claude Desktop": claude_path,
        "Cursor": os.path.expanduser("~/.cursor/mcp.json"),
        "Generic Fallback (OpenCode/Antigravity/Aider)": os.path.expanduser("~/mcp_config.json")
    }
    
    # Track results
    results = {}
    
    # Server settings to inject
    server_config = {
        "command": "uvx",
        "args": ["freelance-pitch-engine"]
    }
    
    print("Initializing Universal General Agent Auto-Installer...\n")
    
    # Loop through targets
    for client_name, config_path in targets.items():
        if not config_path:
            results[client_name] = "Skipped (APPDATA environment variable missing)"
            continue
            
        try:
            # Ensure the parent directory exists
            config_dir = os.path.dirname(config_path)
            os.makedirs(config_dir, exist_ok=True)
            
            # Load existing configuration safely
            config_data = {}
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            config_data = json.loads(content)
                except Exception as e:
                    print(f"Warning: Failed to load existing {client_name} configuration: {e}. Starting fresh.")
                    config_data = {}
            
            # Ensure mcpServers key exists
            if "mcpServers" not in config_data:
                config_data["mcpServers"] = {}
                
            # Inject our server configuration
            config_data["mcpServers"]["freelance-pitch-engine"] = server_config
            
            # Write updated configuration back
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2)
                
            results[client_name] = f"Successfully configured ({config_path})"
            
        except Exception as e:
            results[client_name] = f"Failed ({str(e)})"
            
    # Print clean summary to terminal
    print("=" * 80)
    print(f"{'CLIENT':<45} | STATUS")
    print("=" * 80)
    for client, status in results.items():
        print(f"{client:<45} | {status}")
    print("=" * 80)

if __name__ == "__main__":
    register_server()
