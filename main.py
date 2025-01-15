import requests
import json

url_3dpassport = "https://3de24xplm.com.tw/3dpassport"
url_3dspace ="https://3de24xplm.com.tw/3dspace"
username = "nikki"
DSServiceName = "DemoService"
# print("DSServiceName :",DSServiceName)
DSServiceSecret = "0bc65bcb-56df-45e9-b998-ab4f02c48eb8"
# print("DSServiceSecret :",DSServiceSecret)

x3dsreauthurl = ""
x3ds_service_redirect_url = ""

# Routes Test
ServiceRoutes = "resources/v1/modeler/dsrt/routes/search" # (get)取得所有Route內容
ServiceRoutes_ID = "resources/v1/modeler/dsrt/routes/291727550000070065E9629B00000880"  # (get)透過ID，取得特定Route內容
ServiceRoutes_create = "resources/v1/modeler/dsrt/routes" # (post)
ServiceRoutes_delete = "resources/v1/modeler/dsrt/routes/delete" # (post)
ServiceRoutes_templates = "resources/v1/modeler/dsrt/routetemplates/search" # (get)

# Projest Test
ServiceProject = "resources/v1/modeler/projects"  # (get)
ServiceProject_ID = "resources/v1/modeler/projects/296466B0000025EC6784728500000172"  # (get)
ServiceProject_create = "resources/v1/modeler/projects"  # (post)

# Task Test
ServiceTasks = "resources/v1/modeler/tasks"

params = {
    "identifier": username,
    # "service": f"{url_3dspace}/{ServiceTasks}",
    # "service": f"{url_3dspace}/{ServiceProject}",
    # "service": f"{url_3dspace}/{ServiceProject_ID}",
    "service": f"{url_3dspace}/{ServiceProject_create}",
    # "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"
    # "service": f"{url_3dspace}/{ServiceRoutes}",
    # "service": f"{url_3dspace}/{ServiceRoutes_templates}",
    # "service": f"{url_3dspace}/{ServiceRoutes_ID}",
    # "service": f"{url_3dspace}/{ServiceRoutes_delete}",
}

headers = {
    "Accept": "application/json",         
    "DS-Service-Name": DSServiceName,
    "DS-Service-Secret": DSServiceSecret    

}



request_body = {
    "data": [
        {
            "type": "Project",                  # 專案類型
            "dataelements": {
                "title": "New Project Title",   # 替換為你的專案標題
                "description": "Project Description",  # 替換為描述
                "projectVisibility": "Public", # 專案可見性（Public 或 Members）
                "estimatedStartDate": "2025-01-15",  # 預計開始日期
                "estimatedFinishDate": "2025-06-30"  # 預計結束日期
            }
        }
    ]
}

cert = "3de24xplm.crt"
# Request_1
try:
    # 發送 GET 請求
    response = requests.get(f"{url_3dpassport}/api/v2/batch/ticket", params=params, headers=headers, verify=cert)
    # response = requests.get(f"{url_3dpassport}/api/v2/batch/ticket", params=params, headers=headers, json=request_body, verify=cert)

    response = requests.post(
        f"{url_3dpassport}/api/v2/batch/ticket", 
        params=params, 
        headers=headers, 
        json=request_body, 
        verify=cert
    )

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        x3dsreauthurl = data["x3ds_reauth_url"]
        # print("取得x3ds_reauth_url ：", x3dsreauthurl)
        print("Request_1 ：成功")
    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)


# Request_2
try:
    # 發送 GET 請求
    response = requests.get(x3dsreauthurl, headers=headers, json=request_body,verify=False)

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        x3ds_service_redirect_url = data["x3ds_service_redirect_url"]
        # print("取得x3ds_service_redirect_url：", x3ds_service_redirect_url)
        print("Request_2 ：成功")

    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)

# Request_3
try:
    # 發送 GET 請求
    response = requests.get(x3ds_service_redirect_url, headers=headers, json=request_body,verify=False)

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        json_data = json.dumps(data, indent=None, ensure_ascii=False)  # 格式化為 JSON 字串
        print("Request_3 ：成功")
        print("取得的資料：", json_data)
    else:
        print("請求失敗，狀態碼：", response.status_code)
        print("錯誤回應內容：", response.text)
except requests.exceptions.SSLError as e:
    print("SSL 憑證錯誤：", e)
except requests.exceptions.RequestException as e:
    print("請求錯誤：", e)

