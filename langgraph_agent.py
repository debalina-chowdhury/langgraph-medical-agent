import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
print("hello")
load_dotenv()

# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Define tools using LangChain @tool decorator
@tool
def find_provider(specialty: str) -> str:
    """Find available providers by medical specialty."""
    return (
        f"Found providers for {specialty}: "
        f"Dr. Sarah Johnson (ID: DR001) - available Mon 9am, Wed 2pm. "
        f"Dr. Michael Chen (ID: DR002) - available Tue 11am, Fri 3pm."
    )

@tool
def verify_patient_eligibility(patient_id: str, provider_id: str) -> str:
    """Verify if a patient is eligible to see a specific provider."""
    return f"Patient {patient_id} is eligible for provider {provider_id} — insurance verified, no referral required."

@tool
def book_appointment(patient_id: str, provider_id: str, appointment_time: str, reason: str = "General consultation") -> str:
    """Book an appointment for a patient with a provider."""
    return f"Appointment confirmed for patient {patient_id} with {provider_id} at {appointment_time} for {reason}. SMS confirmation sent."

@tool
def process_referral(referral_text: str, patient_id: str = "unknown") -> str:
    """Process an incoming referral document and extract key information."""
    return f"Referral processed for patient {patient_id} — urgent specialist consult needed, insurance pre-auth required, follow-up within 48 hours."

# Set up tools and model
tools = [find_provider, verify_patient_eligibility, book_appointment, process_referral]

model = ChatAnthropic(
    model="claude-sonnet-4-5",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
).bind_tools(tools)

# Define agent node
def agent_node(state: State):
    system_message = {
        "role": "system",
        "content": (
            "You are a medical scheduling assistant. "
            "Always use find_provider first to get provider IDs — never ask users for internal IDs. "
            "Keep responses concise and patient-friendly."
        )
    }
    messages = [system_message] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

# Build graph
def build_graph():
    graph = StateGraph(State)
    
    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))
    
    # Add edges
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        tools_condition,
    )
    graph.add_edge("tools", "agent")
    
    return graph.compile()

app_graph = build_graph()

# Run function
def run_agent(user_query: str):
    result = app_graph.invoke({
        "messages": [{"role": "user", "content": user_query}]
    })
    return result["messages"][-1].content


if __name__ == "__main__":
    print("Testing LangGraph agent...")
    result = run_agent("Check patient P001's insurance and book a cardiology appointment Monday")
    print(f"Result: {result}")