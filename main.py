import requests
from fastapi import FastAPI
from functions import request_ticket_login, request_csrf, request_create_project

app = FastAPI()
session = requests.Session()

cert = "./3de24xplm.crt"
infinite_ticket = "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"
ENO_CSRF_TOKEN = ''

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




# 定義路由
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/login")
def ticket_login():
    """調用封裝函數，執行 ticket_login"""
    login_url = "https://3de24xplm.com.tw/3dspace/ticket/login"
    response = request_ticket_login(session, login_url, infinite_ticket, cert)
    return response 

@app.get("/csrf")
def csrf_token():
    """調用封裝函數，獲取 CSRF Token"""
    csrf_url = "https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF"
    ENO_CSRF_TOKEN = request_csrf(session, csrf_url, cert)
    return {"csrf_token": ENO_CSRF_TOKEN}

@app.post("/project/create")
def request_create_project():
    """調用封裝函數，新增 project"""
    create_project_url = "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/"
    response = request_create_project(session, create_project_url, infinite_ticket, security_context, ENO_CSRF_TOKEN, body_create_project, cert)
    return response  # 回應請求