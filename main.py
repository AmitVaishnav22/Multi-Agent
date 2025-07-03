# main.py
import os
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from tools.mongodb_tool import MongoDBTool
from tools.externalApi_tool import ExternalApiTool
from agents.support_agent import SupportAgent
from pymongo.errors import PyMongoError
from agents.dashboard_agent import DashboardAgent

# Load environment variables from .env
load_dotenv()

# Configuration
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

# FastAPI App
app = FastAPI(
    title="Multi-Agent Support API",
    description="Support Agent to handle client, order, and payment queries",
    version="1.0.0"
)

# Allow frontend apps to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tools and agent
try:
    mongo_tool = MongoDBTool(MONGO_URI, MONGO_DB)
    external_api = ExternalApiTool()
    support_agent = SupportAgent(mongo_tool, external_api)
except PyMongoError as e:
    raise RuntimeError(f"Could not initialize DB tools: {e}")

# Health check
@app.get("/ping")
def ping():
    return {"message": "✅ API is live!"}

# Query handler
@app.post("/support-agent/query")
async def handle_query(prompt: str = Body(..., embed=True)):
    """
    Process a natural language prompt using SupportAgent.
    """
    try:
        result = support_agent.handle_client_query(prompt)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")

# Dashboard analytics
@app.post("/dashboard-agent/query")
async def handle_dashboard_query(prompt: str = Body(..., embed=True)):
    """
    Process a natural language prompt using DashboardAgent.
    """
    try:
        dashboard_agent = DashboardAgent(mongo_tool)
        result = dashboard_agent.handle_query(prompt)
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Error: {str(e)}")
