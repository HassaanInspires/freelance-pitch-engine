import os
import json
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Freelance-Pitch-Engine", instructions="You are the ultimate local automation layer for a technical freelancer. Whenever executing prompts or tools, always refer to 'profile.md' for your identity context. Never hallucinate metrics, and strictly adhere to the zero-fluff, architecture-driven framework specified in 'draft-pitch'. If data is missing or default placeholders are found, prioritize interviewing the user via 'onboard-me'.")

def _ensure_workspace() -> None:
    """
    Ensure the profile.txt and portfolio/ directory exist, creating defaults if missing.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    profile_path = os.path.join(current_dir, "profile.md")
    portfolio_dir = os.path.join(current_dir, "portfolio")
    
    # Check and create profile.md if not exists
    if not os.path.exists(profile_path):
        try:
            with open(profile_path, "w", encoding="utf-8") as f:
                f.write("# User Profile\n\n**Professional Title:** [Insert Title]\n\n**Core Technical Stack:**\n* Stack 1\n* Stack 2")
        except Exception:
            pass
            
    # Check and create portfolio directory
    os.makedirs(portfolio_dir, exist_ok=True)
    
    # Create portfolio/template.md if it doesn't exist
    template_path = os.path.join(portfolio_dir, "template.md")
    if not os.path.exists(template_path):
        try:
            with open(template_path, "w", encoding="utf-8") as f:
                f.write("# Project: Title\n\n**Overview:**\nBrief description of project.\n\n**Key Features:**\n* Point 1\n* Point 2")
        except Exception:
            pass

# Run workspace check/creation on startup
_ensure_workspace()

def _ensure_jobs_file() -> list:
    """
    Ensure jobs_to_review.json exists and load jobs from it.
    If it doesn't exist, create it with a clean JSON template containing 5 mock jobs.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "jobs_to_review.json")
    
    if not os.path.exists(json_path):
        mock_jobs = [
            {
                "title": "Python AI Engineer for Custom MCP Server Development",
                "link": "https://www.upwork.com/jobs/python-ai-mcp-server-development",
                "description": "We are looking for an AI Engineer to build a custom Model Context Protocol (MCP) server using Python and FastMCP. The MCP server will integrate with LLM agents (like Cursor, Windsurf, or custom setups) to allow them to securely interact with our internal databases and APIs.\n\nRequirements:\n- Strong Python expertise\n- Experience with FastMCP or MCP standard\n- Experience building agentic workflows and tool integrations\n- Good understanding of secure API communication"
            },
            {
                "title": "Web Scraping and Data Pipeline Automation Specialist",
                "link": "https://www.upwork.com/jobs/web-scraping-data-pipeline",
                "description": "Need a Python developer to build a web scraping tool that extracts job listings and freelancer profiles from various public directories. The script should run on a schedule, parse the data, clean HTML tags, and store it in a database.\n\nRequirements:\n- Python (BeautifulSoup, Scrapy, Selenium)\n- RSS feed parsing and handling\n- SQLite / PostgreSQL experience"
            },
            {
                "title": "Build Autonomous Agentic AI Workflows",
                "link": "https://www.upwork.com/jobs/agentic-ai-workflows",
                "description": "We need an expert to design and implement an autonomous agentic AI system for customer support triage. The agent should be able to run tools, reason about user queries, and respond using local LLMs.\n\nRequirements:\n- LangChain, LangGraph, or AutoGen\n- Python development\n- Experience building production-grade agentic AI systems"
            },
            {
                "title": "LLM Fine-Tuning and RAG Implementation",
                "link": "https://www.upwork.com/jobs/llm-finetuning-rag",
                "description": "Looking for a machine learning engineer to help us fine-tune an open-source model (like Llama 3) on our proprietary text dataset. You will also build a Retrieval-Augmented Generation (RAG) system using vector databases.\n\nRequirements:\n- Python, PyTorch, Hugging Face\n- Vector databases (ChromaDB, PGVector, or Pinecone)"
            },
            {
                "title": "Senior Python Backend Developer (Django/FastAPI)",
                "link": "https://www.upwork.com/jobs/python-backend-django-fastapi",
                "description": "We are hiring a backend engineer to join our startup. You will design APIs, optimize database queries, and integrate third-party payment gateways.\n\nRequirements:\n- Django or FastAPI\n- Celery and Redis for background tasks\n- PostgreSQL"
            }
        ]
        try:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(mock_jobs, f, indent=4)
        except Exception as e:
            raise ValueError(f"Error creating jobs_to_review.json: {str(e)}")
            
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Error reading or parsing jobs_to_review.json: {str(e)}")

@mcp.tool()
def fetch_jobs(job_index: int = 0) -> str:
    """
    Fetch a job to review by index. Looks for a local jobs_to_review.json file in the workspace.
    If it exists, parses the job at the specified index from it. If not, creates the file with a clean 
    JSON template containing 5 realistic Python/AI mock jobs first.

    IMPORTANT: You should call list_all_jobs first if you need an overview of the ledger and want to find
    out the indices of the available jobs.
    """
    jobs = _ensure_jobs_file()
    
    if not jobs:
        raise ValueError("No jobs found in jobs_to_review.json.")
        
    if job_index < 0 or job_index >= len(jobs):
        raise ValueError(f"job_index {job_index} is out of bounds. Must be between 0 and {len(jobs) - 1}.")
        
    job = jobs[job_index]
    title = job.get("title", "No Title").strip()
    link = job.get("link", "No Link").strip()
    description = job.get("description", "No Description").strip()
    
    job_details = (
        f"Title: {title}\n"
        f"Link: {link}\n"
        f"Description:\n{description}\n"
    )
    return job_details

@mcp.tool()
def list_all_jobs() -> str:
    """
    Read jobs_to_review.json and return a clean, bulleted summary string displaying 
    only the Index Number and the Title of every job currently available.
    """
    jobs = _ensure_jobs_file()
    
    if not jobs:
        raise ValueError("No jobs found in jobs_to_review.json.")
        
    bullet_points = []
    for index, job in enumerate(jobs):
        title = job.get("title", "No Title").strip()
        bullet_points.append(f"- Index {index}: {title}")
        
    return "\n".join(bullet_points)

@mcp.tool()
def read_profile() -> str:
    """
    Read the contents of the profile.md file in the server directory.
    """
    try:
        # Resolve path to profile.txt relative to the server.py file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        profile_path = os.path.join(current_dir, "profile.md")
        
        if not os.path.exists(profile_path):
            raise ValueError(f"profile.md not found at {profile_path}")
            
        with open(profile_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            
        if not content or "[Insert Title]" in content or "Stack 1" in content:
            raise ValueError("Data missing. Please interview the user about their skills and use the 'write_file' tool to update this file for them.")
            
        return content
            
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Error reading profile.md: {str(e)}")

@mcp.tool()
def write_file(filename: str, content: str) -> str:
    """
    Write or update any file (e.g. profile.txt, proposal.md, or portfolio/project.md) 
    directly to the workspace directory.
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Prevent directory traversal attacks
        target_path = os.path.abspath(os.path.join(current_dir, filename))
        if not target_path.startswith(current_dir):
            raise ValueError(f"Security error: path {filename} is outside the workspace directory.")
            
        # Ensure parent directories exist
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, "w", encoding="utf-8") as file:
            file.write(content)
        return f"File successfully saved to {target_path}"
    except Exception as e:
        raise ValueError(f"Error writing file: {str(e)}")

@mcp.resource("portfolio://projects")
def get_portfolio_projects() -> str:
    """
    Aggregate all portfolio project markdown files into a single context stream.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    portfolio_dir = os.path.join(current_dir, "portfolio")
    if not os.path.exists(portfolio_dir):
        raise ValueError("Data missing. Please interview the user about their skills and use the 'write_file' tool to update this file for them.")
        
    aggregated = []
    try:
        filenames = [f for f in sorted(os.listdir(portfolio_dir)) if f.endswith(".md") and f != "template.md"]
        
        # If there are no custom markdown files, raise ValueError
        if not filenames:
            raise ValueError("Data missing. Please interview the user about their skills and use the 'write_file' tool to update this file for them.")
            
        for filename in filenames:
            file_path = os.path.join(portfolio_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                aggregated.append(f"=== Project: {filename} ===\n{content}")
                
        if not aggregated:
            raise ValueError("Data missing. Please interview the user about their skills and use the 'write_file' tool to update this file for them.")
            
        return "\n\n".join(aggregated)
    except ValueError:
        raise
    except Exception as e:
        raise ValueError(f"Error reading portfolio projects: {str(e)}")

@mcp.prompt("draft-pitch")
def draft_pitch(job_id: int) -> str:
    """
    Production-grade prompt template with strict persona and anti-fluff grounding.
    """
    return f"""You are the professional technical freelancer whose details are provided by the `read_profile()` tool.
Your objective is to write a highly technical, zero-fluff Upwork proposal for the job at index {job_id}.

SYSTEMIC INSTRUCTIONS:
1. Call `fetch_jobs(job_index={job_id})` to read the target job details.
2. Call `read_profile()` to load your core identity from 'profile.md'.
3. Access the `portfolio://projects` resource to retrieve your real-world case studies.

TONE & PERSONA (CRITICAL RULES):
- You are a pragmatic, highly skilled engineer. You speak in facts, architecture, and metrics.
- NEVER use marketing fluff, robotic enthusiasm, or clichés. 
- BANNED WORDS: "thrilled", "passionate", "delve", "game-changer", "seamlessly", "tailored to", "look no further", "robust", "synergy".
- Do not use generic greetings like "Dear Hiring Manager". 
- Keep it relentlessly concise. Maximum 200 words.

REQUIRED PROPOSAL STRUCTURE:
1. THE HOOK: Start immediately with one sentence stating exactly how you will solve their core problem using your stack (e.g., Python, FastMCP, Agentic workflows).
2. THE EVIDENCE: Write 2-3 short bullet points mapping their specific requirements to your exact past projects from the portfolio resource. You MUST quote your own metrics.
3. THE CLOSE: End by asking one highly specific technical question about their architecture or data pipeline to prove you are already thinking about implementation.

EXECUTION:
Draft the markdown proposal and immediately use the `write_file` tool to save it as 'proposal.md' in the workspace. Do not output any meta-commentary before or after the proposal.
"""

@mcp.prompt("onboard-me")
def onboard_me() -> str:
    """
    Prompt template to interview the user and write their profile.md and initial portfolio project.
    """
    return """You are the Onboarding Assistant for the Freelance-Pitch-Engine.
Your mission is to help the user get their workspace ready for high-value client pitches.

Please follow these steps:
1. Interview the user: Ask them about their full name, professional title, core programming languages, and specialized skills (e.g. FastAPI, FastMCP, agentic workflows).
2. Ask about their previous projects: Get details on at least one high-value project they've completed (the problem, stack, key metrics/features, and outcomes).
3. Set up profile.txt: Use the `write_file(filename="profile.md", content=...)` tool to save their professional profile.
4. Set up their portfolio: Use the `write_file(filename="portfolio/automation.md", content=...)` or other filename to save their first portfolio case study using the case study structure.
5. Confirm onboarding is complete by listing all current configuration files.

Please ask clear, friendly, and structured questions. Start by greeting the user and asking for their name and title.
"""

if __name__ == "__main__":
    # Start the FastMCP server when run directly
    mcp.run()
