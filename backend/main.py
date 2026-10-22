"""
FastAPI application for ai-agent-fullstack-hub.
Provides REST API endpoints for agent execution, tool registry, and database schema introspection.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from agent import run_agent, AgentResponse
from tools import TOOL_DEFINITIONS, dispatch_tool
from database import get_schema, execute_query, init_db

app = FastAPI(
    title="AI Agent Fullstack Hub API",
    description="Backend API powering Next.js + Python autonomous tool-calling agent with Gemini & Hermes support",
    version="1.0.0"
)

# Enable CORS for Next.js development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRunRequest(BaseModel):
    prompt: str = Field(..., description="Natural language prompt for the AI agent")
    model: str = Field(default="gemini-1.5-pro", description="Model name (e.g. 'gemini-1.5-pro', 'hermes-3')")
    api_key: Optional[str] = Field(default=None, description="Optional API key for Gemini or Hermes")
    api_base: Optional[str] = Field(default=None, description="Optional custom base URL for Hermes/OpenAI-compatible server")

class DirectSQLRequest(BaseModel):
    query: str = Field(..., description="Direct SQL query for testing")

@app.on_event("startup")
def startup_event():
    # Ensure database is created and seeded
    init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-agent-fullstack-hub-backend",
        "supported_models": ["gemini-1.5-pro", "gemini-1.5-flash", "hermes-3", "hermes-2-pro"],
        "tools_count": len(TOOL_DEFINITIONS)
    }

@app.get("/api/agent/tools")
def list_tools():
    """Returns available tools and their JSON schemas."""
    return {
        "tools": TOOL_DEFINITIONS
    }

@app.get("/api/db/schema")
def database_schema():
    """Returns database tables, column definitions, row counts, and sample data."""
    try:
        schema = get_schema()
        return {"success": True, "schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/db/query")
def run_direct_query(req: DirectSQLRequest):
    """Executes a direct SQL query against the database."""
    result = execute_query(req.query)
    return result

@app.post("/api/agent/run", response_model=AgentResponse)
def execute_agent_task(req: AgentRunRequest):
    """
    Main endpoint: receives user task in natural language, invokes agent,
    triggers Tool Calling (SQL, external API, etc.), and returns structured result.
    """
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
    try:
        response = run_agent(
            prompt=req.prompt,
            model=req.model,
            api_key=req.api_key,
            api_base=req.api_base
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
