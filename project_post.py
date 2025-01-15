import requests
import json
import subprocess

# URL setting

# url = "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/dsrt/routes/search" # GET
url = "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects" # POST



# Para setting
cert = "./3de24xplm.crt"

username = "nikki"
DSServiceName = "DemoService"
DSServiceSecret = "0bc65bcb-56df-45e9-b998-ab4f02c48eb8"


params = {}
headers = {
    "ENO_CSRF_TOKEN" :"YRUP-FUSW-JPN8-1R9D-43K6-VJ64-S8VE-BGYJ",
    "ticket" : "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw=" ,
    "SecurityContext" : "VPLMProjectLeader.Company Name.DEMO_CS",
    "Accept": "application/json;charset=UTF-8",
    "Content-Type": "application/json;charset=UTF-8",
    "DS-Service-Name": DSServiceName,
    "DS-Service-Secret": DSServiceSecret    
    
    # "user" : "nikki",
}

# Body setting
request_body = {
    'data': [
        {
            'id': '000000800000000C0000000000000000',
            'identifier': 'nikki',
            'source': 'https://3de24xplm.com.tw:443/3dspace',
            'relativePath': '/resources/v1/modeler/samples/000000800000000C0000000000000000',
            'cestamp': '857FEB80000045FC5994CC0A00000012',
            'dataelements': {
                'title': '121212121211 Project',
                'description': 'Sample project description.',
                'state': 'Active',
                'estimatedStartDate': '2025-01-15T00:00:00.000Z',
                'estimatedFinishDate': '2025-06-30T23:59:59.000Z',
                'actualStartDate': '2025-01-20T00:00:00.000Z',
                'actualFinishDate': '2025-07-01T12:30:00.000Z',
                'forecastStartDate': '2025-02-01T08:00:00.000Z',
                'forecastFinishDate': '2025-05-31T18:00:00.000Z',
                'constraintDate': '2025-01-10T00:00:00.000Z',
                'nlsType': 'Standard',
                'color': 'Blue',
                'pattern': 'Solid',
                'ganttConfig': 'Default',
                'kindofBaseline': 'Baseline',
                'kindofExperiment': 'Test',
                'kindofTemplate': 'Template',
                'kindofConcept': 'Concept',
                'routeId': 'R12345',
                'columns': 'Default',
                'estimatedDurationInputValue': '120',
                'estimatedDuration': '120 Days',
                'forecastDuration': '90 Days',
                'defaultConstraintType': 'Start No Earlier Than',
                'scheduleFrom': 'Project Start Date',
                'scheduleBasedOn': 'Estimated',
                'projectVisibility': 'Public',
                'currency': 'USD',
                'notes': 'This is a note for the project.',
                'status': 'In Progress'
            }
        }
    ]
}

# 發送 Post 請求
try:
    response = requests.post("https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects", headers=headers, data=request_body, verify=cert)
    # response = requests.get(url, headers=headers, verify=False)

    # 檢查請求是否成功
    if response.status_code == 200:
        # response.encoding = 'utf-8' 
        print("回應標頭：", response.headers)
        try:
            print(response.text)
            data = response.json()
            # data = json.loads(raw_text)  # 手動解析
            # print("解析成功，JSON 內容：", json.dumps(data, indent=4, ensure_ascii=False))
        except json.JSONDecodeError as e:
            print("JSON 解析錯誤：", e)
            # data = json.loads(response.text)
            # print("response.text : ",response.text)
    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)
    print("response.text : ",response.text)
