def test_tools_importable():
    """Test all tools can be imported"""
    from langgraph_agent import (
        find_provider,
        verify_patient_eligibility,
        book_appointment,
        process_referral
    )
    assert find_provider is not None
    assert verify_patient_eligibility is not None
    assert book_appointment is not None
    assert process_referral is not None

def test_find_provider_tool():
    """Test find provider returns provider data"""
    from langgraph_agent import find_provider
    result = find_provider.invoke({"specialty": "cardiology"})
    assert "DR00" in result
    assert len(result) > 0

def test_book_appointment_tool():
    """Test booking tool returns confirmation"""
    from langgraph_agent import book_appointment
    result = book_appointment.invoke({
        "patient_id": "P001",
        "provider_id": "DR001",
        "appointment_time": "Monday 9am"
    })
    assert "P001" in result
    assert "confirmed" in result.lower()

def test_graph_builds():
    """Test LangGraph graph compiles without errors"""
    from langgraph_agent import build_graph
    graph = build_graph()
    assert graph is not None