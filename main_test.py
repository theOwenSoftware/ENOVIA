import requests
import json
# ---------------------------------------------------------------
# URLs 和用戶資訊

username = "nikki"
DSServiceName = "DemoService"
DSServiceSecret = "0bc65bcb-56df-45e9-b998-ab4f02c48eb8"
cert = "./3de24xplm.crt"
ENO_CSRF_TOKEN =""
infinite_ticket = "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"
# ---------------------------------------------------------------
# headers / parms / body

#  (post) create_project 請求 
headers_create_project = {
    "ENO_CSRF_TOKEN": "",
    "ticket": infinite_ticket,
    "SecurityContext": security_context,
    "Accept": "application/json",
    "Content-Type": "application/json",
}
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
                "status": "In Progress"
            }
        }
    ]
}


#  (get) ticket_login 請求 
parms_ticket_login ={
     "ticket" : infinite_ticket
}

# ---------------------------------------------------------------
# Request 管理
session = requests.Session()


# (get) Request_ticket_login
try:
    response_ticket_login = session.get(
        url="https://3de24xplm.com.tw/3dspace/ticket/login", 
        params=parms_ticket_login, 
        verify=cert
    )

    # 檢查請求是否成功
    if response_ticket_login.status_code == 200:
        print("ticket_login 成功")
        
        try:
            # 嘗試解析為 JSON
            response_data = response_ticket_login.json()
            print("ticket_login 返回內容（JSON）：", response_data)
        except json.JSONDecodeError:
            # 若解析失敗，返回原始文本
            response_data = response_ticket_login.text
            print("ticket_login 返回內容（文本）：", response_data)
    else:
        # 請求失敗時的處理
        print(f"ticket_login 失敗，狀態碼：{response_ticket_login.status_code}")
        print("返回內容：", response_ticket_login.text)
except requests.exceptions.RequestException as e:
    # 捕獲請求異常
    print("ticket_login 發生錯誤：", e)

print("Session Cookies After login:", session.cookies)




# (get) Request_CSRF
try:
    response_get_csrf = session.get(
        url="https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF",
        verify=cert
    )

    # 檢查請求是否成功
    if response_get_csrf.status_code == 200:
        print("CSRF Token 請求成功")
        
        try:
            # 嘗試解析為 JSON
            response_data = response_get_csrf.json()

            # 提取 CSRF Token
            csrf_value = response_data.get('csrf', {}).get('value', None)
            if csrf_value:
                ENO_CSRF_TOKEN = csrf_value
                headers_create_project['ENO_CSRF_TOKEN'] = ENO_CSRF_TOKEN
                print("ENO_CSRF_TOKEN 取得成功:", ENO_CSRF_TOKEN)
            else:
                print("CSRF Token 解析失敗，未找到有效值")
        except json.JSONDecodeError:
            # 若 JSON 解析失敗，輸出原始文本
            print("CSRF Token 返回內容（文本）：", response_get_csrf.text)
    else:
        # 請求失敗處理
        print(f"CSRF Token 請求失敗，狀態碼：{response_get_csrf.status_code}")
        print("返回內容：", response_get_csrf.text)
except requests.exceptions.RequestException as e:
    # 捕獲請求異常
    print("CSRF Token 請求發生錯誤：", e)

print("Session Cookies After CSRF Request:", session.cookies)


# (post) Request_create_project
try:
    # 檢查是否已取得 ENO_CSRF_TOKEN
    if headers_create_project.get('ENO_CSRF_TOKEN'):
        # 發送 POST 請求以創建項目
        response_create_project = session.post(
            url="https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/",
            headers=headers_create_project,
            json=body_create_project,
            verify=cert
        )

        # 檢查請求是否成功
        if response_create_project.status_code == 200:
            try:
                # 嘗試解析返回內容為 JSON
                response_data = response_create_project.json()
                print("Project 創建成功，返回內容（JSON）：", response_data)
            except json.JSONDecodeError:
                # 若 JSON 解析失敗，輸出原始文本
                print("Project 創建成功，但 JSON 解析失敗，返回內容（文本）：", response_create_project.text)
        else:
            # 請求失敗處理
            print(f"Project 創建失敗，狀態碼：{response_create_project.status_code}")
            print("返回內容：", response_create_project.text)
    else:
        print("錯誤：尚未取得有效的 ENO_CSRF_TOKEN，無法創建項目")

except requests.exceptions.RequestException as e:
    # 捕獲請求異常
    print("Project 創建請求發生錯誤：", e)

# 打印 Session Cookies
print("Session Cookies After Create Project:", session.cookies)

