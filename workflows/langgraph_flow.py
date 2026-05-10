from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from agents.summary_agent import summary_agent
from agents.diagnosis_agent import diagnosis_agent
from agents.insurance_agent import insurance_agent
from agents.coding_agent import coding_agent

class AgentState(TypedDict):
    text: str
    summary: str
    diagnosis: Dict[str, Any]
    insurance: Dict[str, Any]
    codes: Dict[str, Any]
    metadata: Dict[str, Any]

def summary_node(state: AgentState):
    state["summary"] = summary_agent.process(state["text"])
    return state

def diagnosis_node(state: AgentState):
    state["diagnosis"] = diagnosis_agent.process(state["text"])
    return state

def insurance_node(state: AgentState):
    state["insurance"] = insurance_agent.process(state["text"])
    return state

def coding_node(state: AgentState):
    # Pass diagnosis details to coding agent
    diag_str = str(state["diagnosis"])
    state["codes"] = coding_agent.process(diag_str)
    return state

def create_workflow():
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("summarize", summary_node)
    workflow.add_node("diagnose", diagnosis_node)
    workflow.add_node("verify_insurance", insurance_node)
    workflow.add_node("generate_codes", coding_node)

    # Define edges
    workflow.set_entry_point("summarize")
    workflow.add_edge("summarize", "diagnose")
    workflow.add_edge("diagnose", "verify_insurance")
    workflow.add_edge("verify_insurance", "generate_codes")
    workflow.add_edge("generate_codes", END)

    return workflow.compile()

medical_workflow = create_workflow()
