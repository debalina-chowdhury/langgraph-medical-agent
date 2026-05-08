import streamlit as st
from langgraph_agent import run_agent, app_graph

st.set_page_config(
    page_title="LangGraph Medical Agent",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .header-container {
        background: linear-gradient(135deg, #6a1b9a, #4a148c);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .tool-badge {
        background-color: #f3e5f5;
        border-left: 3px solid #7b1fa2;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.85em;
        margin: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 style="color:white; margin:0">🧠 LangGraph Medical Agent</h1>
    <p style="color:#e1bee7; margin:0">Production-grade agentic scheduling powered by LangGraph + Claude</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔧 Architecture")
    st.markdown("""
    Built with **LangGraph** state machine:
    
    - **StateGraph** manages conversation state
    - **ToolNode** handles tool execution
    - **Conditional edges** route between agent and tools
    - **Claude** powers reasoning and decisions
    """)
    st.markdown("---")
    st.markdown("### Try asking:")
    st.markdown("""
    - *"Book P001 with a cardiologist Monday"*
    - *"Process referral for P002: chest pain urgent"*
    - *"Find orthopedic surgeon for P003"*
    """)
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"],
        avatar="🧠" if message["role"] == "assistant" else "👤"):
        st.write(message["content"])

# Chat input
query = st.chat_input("Ask about scheduling, referrals, or patient eligibility...")

if query:
    with st.chat_message("user", avatar="👤"):
        st.write(query)
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("assistant", avatar="🧠"):
        with st.spinner("LangGraph agent processing..."):
            answer = run_agent(query)
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })