Multi-Agent Technical Blog Generator (Human-in-the-Loop)

An agentic content generation pipeline built using LangGraph, LangChain, and Groq (Llama 3.3). Unlike standard text generators, this project features interactive Human-in-the-Loop (HITL) checkpoints that pause execution to let you inspect, approve, or steer the output at every stage before proceeding.

🏗️ Architecture & Workflow

[ START ]
│
▼
┌──────────────────┐
│ Researcher Agent │ ◄─── (Regenerates if revised)
└────────┬─────────┘
│
▼
🛑 [Human Review: Research Outline] ──► (Feedback/Approve)
│
▼
┌──────────────────┐
│ Writer Agent │ ◄─── (Regenerates if revised)
└────────┬─────────┘
│
▼
🛑 [Human Review: Blog Draft] ───────► (Feedback/Approve)
│
▼
┌──────────────────┐
│ Editor Agent │
└────────┬─────────┘
│
▼
[ END ]

🚀 Features

State Graph Orchestration: Uses langgraph.StateGraph with state persistence for clean step-by-step processing.

Human-in-the-Loop Gatekeepers: Pauses graph execution at research and draft stages to prompt for human review and feedback.

Dynamic Routing: Loop back to previous nodes automatically if revision feedback is provided, or proceed forward upon approval.

Powered by Groq: Ultra-fast inference with Llama 3.3 models.

📁 Project Structure

├── state.py # Pydantic state definition (BlogState)
├── agent.py # Prompts, LLM initialization, and agent functions
├── graph.py # LangGraph workflow, nodes, and conditional edges
├── main.py # Terminal runner script handling stream and interrupts
├── .env # Environment configuration (API keys)
└── README.md # Setup documentation

🛠️ Getting Started

1. Prerequisites

Python 3.10 or higher installed on your system.

A Groq API Key (Get one for free at console.groq.com).

2. Clone & Setup Virtual Environment

# Clone the repository (or navigate to your project directory)

cd multiagent-blog-generator

# Create a virtual environment

python -m venv env

# Activate the virtual environment

# On Windows (PowerShell):

.\env\Scripts\Activate.ps1

# On macOS / Linux:

source env/bin/activate

3. Install Dependencies

pip install langgraph langchain-groq langchain-core pydantic python-dotenv

4. Configure Environment Variables

Create a .env file in the root directory:

touch .env # On macOS/Linux

# Or create it manually on Windows

Add your Groq API Key to .env:

GROQ_API_KEY=your_actual_groq_api_key_here

🏃 Running the Pipeline

To start the interactive multi-agent pipeline:

python main.py

How to Interact with the Pipeline:

Research Gate: The Researcher Agent builds a high-density bulleted outline. The graph pauses and asks for your review:

Type approve (or press Enter) to send the outline directly to the Writer.

Type specific feedback (e.g., "Focus more on benchmark accuracy comparisons") to force the researcher to regenerate the outline.

Draft Gate: The Writer Agent drafts the article. The graph pauses again for your approval or specific editing instructions.

Editor Gate: Once approved, the Editor Agent polishes the markdown formatting and prints the final output directly to your terminal.

🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.
