import os
import sys
import json

def register_server():
    """
    Auto-register the freelance-pitch-engine MCP server in Claude Desktop's config file.
    """
    # 1. Determine OS-specific path for Claude Desktop config
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            print("Error: APPDATA environment variable not found.", file=sys.stderr)
            sys.exit(1)
        config_path = os.path.join(appdata, "Claude", "claude_desktop_config.json")
    elif sys.platform == "darwin":
        config_path = os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    else:  # linux or other UNIX
        config_path = os.path.expanduser("~/.config/Claude/claude_desktop_config.json")
        
    print(f"Targeting Claude Desktop configuration at: {config_path}")
    
    # 2. Read existing configuration securely
    config_dir = os.path.dirname(config_path)
    os.makedirs(config_dir, exist_ok=True)
    
    config_data = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    config_data = json.loads(content)
        except Exception as e:
            print(f"Warning: Failed to load existing configuration: {e}. Starting fresh.")
            config_data = {}
            
    # 3. Ensure mcpServers key exists
    if "mcpServers" not in config_data:
        config_data["mcpServers"] = {}
        
    # 4. Insert our server settings
    config_data["mcpServers"]["freelance-pitch-engine"] = {
        "command": "uvx",
        "args": ["freelance-pitch-engine"]
    }
    
    # 5. Write updated configuration back
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2)
        print("Success: freelance-pitch-engine registered in Claude Desktop configuration!")
    except Exception as e:
        print(f"Error: Failed to write configuration to {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    register_server()
