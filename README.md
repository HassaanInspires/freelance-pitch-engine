# Freelance Pitch Engine 🚀

An installable local Model Context Protocol (MCP) server that acts as a **Ban-Proof Local Sandbox** for drafting freelance proposals. By keeping the proposal-generation process completely offline and decoupled from direct browser-scraping or live API submissions on Upwork, it guarantees account safety and protects against automated action bans.

## Key Concept: Ban-Proof Local Sandbox

Automated scraping and programmatic bot proposals violate Upwork’s Terms of Service and can result in permanent account bans. The **Freelance Pitch Engine** avoids this completely:
1. **No Bot Submissions:** Proposals are generated, tailored, and previewed in a sandboxed local environment. You retain final control over what is submitted.
2. **Local Data Feeds:** Job postings are loaded locally from a curated `jobs_to_review.json` ledger, ensuring zero trace of automated scraper activity on the platform.
3. **Privacy First:** Your profile skills and client proposals never leave your system unless you copy and paste them yourself.

---

## Native MCP Capabilities

The server exposes resources, tools, and prompts conforming to the Model Context Protocol standard:

### 1. Resource: `portfolio://projects`
* **Description:** An aggregated, read-only data stream that recursively pulls and compiles all project markdown files under the `portfolio/` directory.
* **Purpose:** Serves as the raw contextual backing for LLMs to pull case study evidence, architecture details, and project metrics.

### 2. Tools
* **`list_all_jobs()`**: Displays a bulleted ledger showing the Index and Title of all active jobs in `jobs_to_review.json`.
* **`fetch_jobs(job_index: int)`**: Retrieves raw details (Title, Link, and Description) for a specific job in the ledger.
* **`read_profile()`**: Reads the freelancer's identity, title, and skillset from `profile.md`.
* **`write_file(filename: str, content: str)`**: Safely writes or updates any workspace file (e.g. `profile.md`, `proposal.md`, or new portfolio projects) to the directory.

### 3. Prompts
* **`onboard-me`**: Guide for the AI client to interview the user about their skillset, set up their `profile.md`, and draft their initial portfolio projects.
* **`draft-pitch(job_id: int)`**: A high-impact, zero-fluff system prompt that instructs the AI to pull the profile context, parse the portfolio projects, evaluate the selected job, and save a tailored proposal.

---

## Setup & Running

### 💻 Supported Operating Systems
This framework is fully cross-platform. The automated setup script natively supports:
* **Windows** (`%APPDATA%` configurations)
* **macOS** (`~/Library/Application Support` configurations)
* **Linux** (`~/.config` configurations)

### 📥 Step-by-Step Installation

**1. Clone the Official Repository**
Open your terminal (Command Prompt, PowerShell, or bash) and download the engine:
```bash
git clone https://github.com/HassaanInspires/freelance-pitch-engine.git
cd freelance-pitch-engine
```

**2. Install Dependencies & Auto-Configure**
Install the package locally and run the automated registration script to configure Claude Desktop:
```bash
uv pip install -e .
pitch-engine-setup
```

### Running Locally
To launch the MCP server:
```bash
freelance-pitch-engine
```
