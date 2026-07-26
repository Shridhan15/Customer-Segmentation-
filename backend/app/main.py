from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import logging

from app.agent.graph import agent_graph


logger = logging.getLogger("main")
app = FastAPI(
    title="Customer Segmentation & Personalization Agent API",
    description="Backend API for the Retail Banking AI Agent",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None
    human_clarification_response: Optional[str] = None

class ChatResponse(BaseModel):
    thread_id: str
    needs_human_input: bool
    clarification_question: Optional[str] = None
    response_message: Optional[str] = None
    agent_reasoning: Optional[Dict[str, Any]] = None
    insights: Optional[str] = None
    data_payload: Optional[Dict[str, Any]] = None

@app.get("/")
def read_root():
    return {"message": "Retail Banking AI Agent API is running."}

@app.post("/api/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    try:
        thread_id = request.thread_id or str(uuid.uuid4())
        
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "raw_query": request.query,
            "thread_id": thread_id,
        }
        
        if request.human_clarification_response:
             initial_state["raw_query"] = request.human_clarification_response

        result_state = agent_graph.invoke(initial_state, config=config)

        requires_human_input = result_state.get("requires_human_input", False)
        
        if requires_human_input:
            return ChatResponse(
                thread_id=thread_id,
                needs_human_input=True,
                clarification_question=result_state.get("human_clarification")
            )

        final_output = result_state.get("final_output", {})

        logger.info(f"Final output for thread {thread_id}: {final_output}")

        return ChatResponse(
            thread_id=thread_id,
            needs_human_input=False,
            # Pull the response_message out of the root state here:
            response_message=result_state.get("response_message"),
            agent_reasoning=final_output.get("agent_reasoning",{}),
            insights=final_output.get("insights"),
            data_payload=final_output.get("data_payload")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))