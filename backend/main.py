"""
Aplicação FastAPI para ai-agent-fullstack-hub.
Fornece endpoints REST para execução do agente autônomo, registro de ferramentas e introspecção do banco de dados relacional.
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
    description="API de backend com suporte a Agente Autônomo com Tool Calling baseado em DeepSeek V4 e Nous Hermes",
    version="1.0.0"
)

# Habilitar CORS para o servidor Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentRunRequest(BaseModel):
    prompt: str = Field(..., description="Instrução em linguagem natural para o agente de IA")
    model: str = Field(default="deepseek-v4", description="Nome do modelo (ex: 'deepseek-v4', 'hermes-3')")
    api_key: Optional[str] = Field(default=None, description="Chave de API opcional para DeepSeek ou Hermes")
    api_base: Optional[str] = Field(default=None, description="URL base personalizada opcional para o servidor compatível com OpenAI")

class DirectSQLRequest(BaseModel):
    query: str = Field(..., description="Consulta SQL direta para testes")

@app.on_event("startup")
def startup_event():
    # Garantir que o banco de dados seja criado e populado
    init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-agent-fullstack-hub-backend",
        "supported_models": ["deepseek-v4", "deepseek-chat", "hermes-3", "hermes-2-pro"],
        "tools_count": len(TOOL_DEFINITIONS)
    }

@app.get("/api/agent/tools")
def list_tools():
    """Retorna ferramentas disponíveis e seus esquemas JSON."""
    return {
        "tools": TOOL_DEFINITIONS
    }

@app.get("/api/db/schema")
def database_schema():
    """Retorna tabelas do banco de dados, definições de colunas, contagem de linhas e dados de amostra."""
    try:
        schema = get_schema()
        return {"success": True, "schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/db/query")
def run_direct_query(req: DirectSQLRequest):
    """Executa uma consulta SQL direta no banco de dados."""
    result = execute_query(req.query)
    return result

@app.post("/api/agent/run", response_model=AgentResponse)
def execute_agent_task(req: AgentRunRequest):
    """
    Endpoint principal: recebe a instrução do usuário em linguagem natural, aciona o agente,
    dispara o Tool Calling (SQL, API externa, etc.) e retorna um resultado estruturado.
    """
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="A instrução (prompt) não pode estar vazia")
        
    try:
        response = run_agent(
            prompt=req.prompt,
            model=req.model,
            api_key=req.api_key,
            api_base=req.api_base
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha na execução do agente: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
