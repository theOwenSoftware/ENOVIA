import requests
from fastapi import FastAPI
from time import time
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

class DataElements(BaseModel):
    title: str
    description: Optional[str]
    state: str

class DataItem(BaseModel):
    id: str
    dataelements: DataElements

class CreateProjectRequest(BaseModel):
    data: List[DataItem]
    data: List[DataItem]

# ---------------------------------

class DataElements_update(BaseModel):
    title: str
    name: str
    description: Optional[str]
    state: str
    project: str
    percentComplete: str

class DataItem_update(BaseModel):
    id: str
    dataelements: DataElements_update

class UpdateProjectRequest(BaseModel):
    data: List[DataItem_update]


from flask import Flask
from flask_cors import CORS
from functions import (
    request_ticket_login, request_csrf,
    request_create_project,
    request_search_project,
    request_search_project_by_id,
    request_fetch_project_issues_by_id,
    request_delete_project_by_id,
    request_update_project,
    request_update_project_by_id
)
from router import path

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

session = requests.Session()
login_url = "https://3de24xplm.com.tw/3dspace/ticket/login"
csrf_url = "https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF"

cert = "./3de24xplm.crt"
infinite_ticket = "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"

app = FastAPI()

# Body 定義
body_create_project = {
    "data": [
        {
            "id": "000000800000000C0000000000000000",
            "identifier": "nikki",
            "source": "https://3de24xplm.com.tw:443/3dspace",
            "relativePath": "/resources/v1/modeler/samples/000000800000000C0000000000000000",
            "cestamp": "857FEB80000045FC5994CC0A00000012",
            "dataelements": {
                "title": "211111 Project",
                "description": "Sample project description.",
                "state": "Active",
                "estimatedStartDate": "2025-01-15T00:00:00.000Z",
                "estimatedFinishDate": "2025-06-30T23:59:59.000Z",
                "actualStartDate": "2025-01-20T00:00:00.000Z",
                "actualFinishDate": "2025-07-01T12:30:00.000Z",
                "forecastStartDate": "2025-02-01T08:00:00.000Z",
                "forecastFinishDate": "2025-05-31T18:00:00.000Z",
                "constraintDate": "2025-01-10T00:00:00.000Z",
                "nlsType": "Standard",
                "color": "Blue",
                "pattern": "Solid",
                "ganttConfig": "Default",
                "kindofBaseline": "Baseline",
                "kindofExperiment": "Test",
                "kindofTemplate": "Template",
                "kindofConcept": "Concept",
                "routeId": "R12345",
                "columns": "Default",
                "estimatedDurationInputValue": "120",
                "estimatedDuration": "120 Days",
                "forecastDuration": "90 Days",
                "defaultConstraintType": "Start No Earlier Than",
                "scheduleFrom": "Project Start Date",
                "scheduleBasedOn": "Estimated",
                "projectVisibility": "Public",
                "currency": "USD",
                "notes": "This is a note for the project.",
                "status": "In Progress",
            },
        }
    ]
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialization logic (e.g., setting up shared state)
    app.state.ENO_CSRF_TOKEN = ""  # 初始化為空字符串或其他有效值

    app.state.LAST_PROJECT_ID = []  # Initialize as an empty list
    print("Application startup")
    yield  # This allows the app to run
    # Cleanup logic (e.g., closing connections)
    print("Application shutdown")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# 定義路由
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/login")
def ticket_login():
    """調用封裝函數，執行 ticket_login"""
    current_time = time()
    if hasattr(app.state, "last_login_time") and (current_time - app.state.last_login_time < 60):
        return {"error": "Please wait before making another login request."}
    
    url = login_url
    response = request_ticket_login(session, url, infinite_ticket, cert)
    app.state.last_login_time = current_time  # 更新上次請求時間
    return response

@app.get("/csrf")
def csrf_token():
    """調用封裝函數，獲取 CSRF Token"""
    url = csrf_url
    current_time = time()
    if hasattr(app.state, "last_CSRF_time") and (current_time - app.state.last_CSRF_time < 300):
        return {"error": "Please wait before making another login request.",
                "ENO_CSRF_TOKEN": app.state.ENO_CSRF_TOKEN}

    app.state.ENO_CSRF_TOKEN = request_csrf(session, url, cert)
    return {"csrf_token":  app.state.ENO_CSRF_TOKEN}

@app.get("/project")
def search_project():
    """Search for existing projects and store IDs."""
    csrf_token = app.state.ENO_CSRF_TOKEN  # Get CSRF Token from shared state
    url = "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/"
    
    # Make the request
    response = request_search_project(session, url, infinite_ticket, security_context, csrf_token, cert)
    
    # Extract project IDs
    if isinstance(response, dict) and 'data' in response:
        last_project_ids = [item['id'] for item in response['data'] if 'id' in item]
        app.state.LAST_PROJECT_ID = last_project_ids
        print("project Id list have been update")
        return {"project_ids": last_project_ids}
    
    # return response  # 回應請求

@app.get("/project/all")
def search_project_all():
    """Search for existing projects and store IDs."""
    csrf_token = app.state.ENO_CSRF_TOKEN  # Get CSRF Token from shared state
    url = "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/"
    print("in main")
    # Make the request
    response = request_search_project(session, url, infinite_ticket, security_context, csrf_token, cert)
    
    return response  # 回應請求

@app.get("/project/{ID}")
def search_project_by_id(ID: str):
    """Search for a specific project by ID."""

    csrf_token = app.state.ENO_CSRF_TOKEN  # Get CSRF Token from shared state
    last_project_id = app.state.LAST_PROJECT_ID  # Get last accessed project IDs
    
    # Validate ID existence
    if ID not in last_project_id:
        return {"Error":"Project ID not found."}
    # Construct URL and make the request
    url = f"https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/{ID}"
    response = request_search_project_by_id(session, url, infinite_ticket, security_context, csrf_token, cert)
    return response

@app.get("/project/{ID}/issues")
def search_project_issues_by_id(ID: str):
    """Feach project issues by ID."""

    csrf_token = app.state.ENO_CSRF_TOKEN  # Get CSRF Token from shared state
    last_project_id = app.state.LAST_PROJECT_ID  # Get last accessed project IDs
    
    # Validate ID existence
    if ID not in last_project_id:
        return {"Error":"Project ID not found."}
    # Construct URL and make the request
    url = f"https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/{ID}/issues"
    response = request_fetch_project_issues_by_id(session, url, infinite_ticket, security_context, csrf_token, cert)
    return response

@app.delete("/project/delete/{ID}") 
def delete_project_by_id(ID: str):
    """Delete project by ID."""
    csrf_token = app.state.ENO_CSRF_TOKEN  # Get CSRF Token from shared state
    search_project()
    last_project_id = app.state.LAST_PROJECT_ID  # Get last accessed project IDs

    # Validate ID existence
    if ID not in last_project_id:
        return {
            "error": "Project ID not found.",
            "details": {
                "project_id": ID,
                "available_project_ids": last_project_id,
            },
        }
    
    # Construct URL and make the request
    url = f"https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/{ID}"
    response = request_delete_project_by_id(
        session, url, infinite_ticket, security_context, csrf_token, cert
    )
    return response

@app.put("/project/update") 
def update_project(request: UpdateProjectRequest):
    """ 更新 project內容 """
    csrf_token = app.state.ENO_CSRF_TOKEN  # Get CSRF Token from shared state
    url = f"https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects"
    req_body = request.model_dump()
    response = request_update_project(
        session, url, infinite_ticket, security_context, csrf_token, req_body,cert
    )
    return response


@app.post("/project/create")
async def create_project(request: CreateProjectRequest):
    """調用封裝函數，新增 project"""
    print("1111")
    csrf_token = app.state.ENO_CSRF_TOKEN  # 從共享狀態獲取 CSRF Token
    url = "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/"
    req_body = request.model_dump()

    response = request_create_project(
        session, url, infinite_ticket, security_context, csrf_token, req_body, cert
    )
    return response  # 回應請求


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# app.include_router(ws_server.router)
# app.include_router(path.router, prefix="/path")