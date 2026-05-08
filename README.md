# LangGraph Medical Scheduling Agent

A production-grade medical scheduling AI agent built with LangGraph StateGraph, Anthropic Claude, and Streamlit. Uses a state machine architecture with conditional edge routing to handle complex multi-step scheduling workflows.

## Architecture

Built with LangGraph StateGraph pattern:

- StateGraph manages conversation state across tool calls
- ToolNode handles tool execution with automatic routing
- Conditional edges route between agent reasoning and tool execution
- Claude powers natural language understanding and decision making

## Tools

- find_provider: Find available providers by medical specialty
- verify_patient_eligibility: Check insurance and eligibility
- process_referral: Extract key info from referral documents
- book_appointment: Schedule and confirm appointments

## Why LangGraph over a manual loop

- Explicit state management with TypedDict
- Declarative graph structure instead of imperative while loop
- Built-in support for checkpointing and persistence
- Production-ready patterns used in enterprise AI deployments

## Tech Stack

- LangGraph StateGraph with conditional edge routing
- Anthropic Claude (claude-sonnet-4-5) via LangChain Anthropic
- Streamlit web interface
- Python 3.9

## Setup

1. Clone the repo
2. Run: pip install -r requirements.txt
3. Add your API key: echo "ANTHROPIC_API_KEY=your-key-here" > .env
4. Run: streamlit run app.py
5. Open http://localhost:8501

## Example Queries

- Book patient P001 with a cardiologist on Monday
- Process referral for P002: chest pain, urgent cardiology needed
- Find an orthopedic surgeon for P003 and verify eligibility
- Patient P001 has chest pain, find a cardiologist and book urgent appointment

## Project Structure

- langgraph_agent.py - LangGraph StateGraph agent with tool definitions
- app.py - Streamlit frontend
- requirements.txt - Dependencies
- .env - API key not pushed to GitHub
- .gitignore - Ignores .env
- README.md - This file

## Future Improvements

- Add LangGraph checkpointing for conversation persistence
- Connect to real EHR APIs
- Add multi-agent coordination with CrewAI
- Deploy to Streamlit Cloud

## Author

Debalina Chowdhury
github.com/debalina-chowdhury
