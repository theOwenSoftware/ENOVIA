import requests
import json
from functions import request_ticket_login, request_csrf, request_create_project

# ---------------------------------------------------------------
# URLs 和用戶資訊
username = "nikki"
DSServiceName = "DemoService"
DSServiceSecret = "0bc65bcb-56df-45e9-b998-ab4f02c48eb8"
cert = "./3de24xplm.crt"
infinite_ticket = "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"

login_url = "https://3de24xplm.com.tw/3dspace/ticket/login"
csrf_url = "https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF"
create_project_url = "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/"

# ---------------------------------------------------------------
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

# ---------------------------------------------------------------
# 主程序
if __name__ == "__main__":
    session = requests.Session()

    # Step 1: 執行 ticket_login
    print("執行 ticket_login...")
    ticket_response = request_ticket_login(session, login_url, infinite_ticket, cert)

    # Step 2: 獲取 CSRF Token
    print("\n執行 CSRF Token 請求...")
    ENO_CSRF_TOKEN = request_csrf(session, csrf_url, cert)

    # Step 3: 創建項目
    print("\n執行 create_project 請求...")
    request_create_project(session, create_project_url, infinite_ticket, security_context, ENO_CSRF_TOKEN, body_create_project, cert)
