from app.core import config
from app.utils.http_client import http_client
from fastapi import  Request
import requests



# ------------------------- 搜尋專案 -------------------------
def request_search_project(request: Request,api_config: dict, detail):
    """取得所有專案列表，並提取必要的欄位"""
    url = f"{api_config['base_url']}/resources/v1/modeler/projects"
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = http_client.perform_request_with_retries(request,url, headers, method="GET")
    # print ("assignees:",Request.app.state.ASSIGNEES_LIST)
    if not response:  # 如果請求失敗，直接返回錯誤訊息
        return {"error": "Request failed or no response"}

    try:
        data = response.json().get("data", [])
    except requests.exceptions.JSONDecodeError as e:
        print(f" JSON 解析錯誤：{e}")
        return {"error": "Invalid JSON response", "raw_response": response.text}
    
    if detail ==False:
        projects = [
            {
                "id": item.get("id", ""),
                "title": item.get("dataelements", {}).get("title", ""),
                "description": item.get("dataelements", {}).get("description", ""),
                "state": item.get("dataelements", {}).get("state", ""),
                "status": item.get("dataelements", {}).get("status", ""),
                "estimatedStartDate": item.get("dataelements", {}).get("estimatedStartDate", ""),
                "estimatedFinishDate": item.get("dataelements", {}).get("estimatedFinishDate", ""),
                "percentComplete": item.get("dataelements", {}).get("percentComplete", ""),
                "estimatedDuration": item.get("dataelements", {}).get("estimatedDuration", ""),
                "forecastDuration": item.get("dataelements", {}).get("forecastDuration", ""),
            }
            for item in data if item.get("id")  # 過濾掉沒有 ID 的專案
            
        ]
        # **取得 FastAPI 全域變數**
        assignees_list_1 = request.app.state.ASSIGNEES_LIST_1
        assignees_list_2 = request.app.state.ASSIGNEES_LIST_2

        # **使用 set() 快速查找現有專案 ID，避免重複插入**
        existing_ids = {entry["id"] for entry in assignees_list_1}

    # **過濾出尚未存在的專案**
        new_entries = [
            {
                "id": item.get("id", ""),
                "title": item.get("dataelements", {}).get("title", ""),
                "tasks": []
            }
            for item in data
            if item.get("id") and item.get("id") not in existing_ids
        ]

        # **如果有新的專案，則一次性更新 `ASSIGNEES_LIST_1`**
        if new_entries:
            assignees_list_1.extend(new_entries)
            assignees_list_2.extend(new_entries)
                

        if projects:
            api_config["last_project_ids"] = [proj["id"] for proj in projects]  # 更新 ID 列表
            print("Project list has been updated")
        return projects if projects else {"message": "No valid projects found"}
    else:
        return data

def request_search_project_by_id(request: Request,api_config: dict, project_id: str):
    """向 API 查詢特定專案的詳細資訊"""

    # 構建 API 請求 URL，根據專案 ID 查詢
    url = f"{api_config['base_url']}/resources/v1/modeler/projects/{project_id}"
    
    # 設定 API 認證標頭，包含 ticket、SecurityContext 及 CSRF Token
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # 執行 HTTP 請求，使用 `perform_request_with_retries` 進行錯誤重試
    response =  http_client.perform_request_with_retries(request,url, headers, method="GET")
    
    if response:
        try:
            return response.json()  # **正常回傳 JSON 資料**
        except requests.exceptions.JSONDecodeError as e:
            print(f" JSON 解析錯誤：{e}")
            return {"error": "Invalid JSON response", "raw_response": response.text}
    else:
        return {"error": "Request failed"}

# ------------------------- 建立專案 -------------------------
def request_create_project(request: Request,api_config: dict, project_data: dict):
    """向 API 發送請求以建立新專案"""

    url = f"{api_config['base_url']}/resources/v1/modeler/projects"
    
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response =  http_client.perform_request_with_retries(request, url, headers, method="POST", json=project_data)
    
    if response:
        try:
            return response.json()  # **正常回傳 JSON 資料**
        except requests.exceptions.JSONDecodeError as e:
            print(f" JSON 解析錯誤：{e}")
            return {"error": "Invalid JSON response", "raw_response": response.text}
    else:
        return {"error": "Request failed"}
# ------------------------- 更新專案 -------------------------
def request_update_project(request: Request,api_config: dict, project_data: dict):
    """
    向 API 發送請求以更新指定的專案。
    回應:
    - 成功時返回更新後的專案資訊。
    - 失敗時返回錯誤訊息。
    """

    # 構建 API 請求 URL，指向專案更新端點
    url = f"{api_config['base_url']}/resources/v1/modeler/projects"

    # 設定 API 認證標頭，包含 ticket、SecurityContext 及 CSRF Token
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # 執行 HTTP PUT 請求，使用 `perform_request_with_retries` 進行錯誤重試
    response = http_client.perform_request_with_retries(request,url, headers, method="PUT", json=project_data)
    
    if response:
        try:
            return response.json()  # **正常回傳 JSON 資料**
        except requests.exceptions.JSONDecodeError as e:
            print(f" JSON 解析錯誤：{e}")
            return {"error": "Invalid JSON response", "raw_response": response.text}
    else:
        return {"error": "Project update failed"}

# ------------------------- 刪除專案 -------------------------
def request_delete_project_by_id(request: Request,api_config: dict, project_id: str):
    """
    向 API 發送請求以刪除指定的專案。
    回應:
    - 成功時返回刪除確認資訊。
    - 若專案 ID 不存在，則返回錯誤訊息。
    """
    # 構建 API 請求 URL，指向專案刪除端點
    url = f"{api_config['base_url']}/resources/v1/modeler/projects/{project_id}"

    # 設定 API 認證標頭，包含 ticket、SecurityContext 及 CSRF Token
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    # 執行 HTTP DELETE 請求，使用 `perform_request_with_retries` 進行錯誤重試
    response = http_client.perform_request_with_retries(request,url, headers, method="DELETE")
    
    if response:
        try:
            return response.json()  # **正常回傳 JSON 資料**
        except requests.exceptions.JSONDecodeError as e:
            print(f" JSON 解析錯誤：{e}")
            return {"error": "Invalid JSON response", "raw_response": response.text}
    else:
        return {"error": "Project deletion failed"}    
