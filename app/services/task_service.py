import requests
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
from fastapi import  Request

from app.utils.http_client import http_client


# ------------------------- 取得所有 Task -------------------------
async def request_search_task_by_id(request: Request, api_config: dict, entity_id: str, nested: bool, is_root=True):
    """
    查詢指定專案 (`project_id`) 或任務 (`task_id`) 的所有子任務，支援非同步請求，提高查詢效率。

    - **請求參數**:
        - `entity_id` (str): 目標專案或任務的 ID，可傳入 `project_id` 或 `task_id`。
        - `nested` (bool): 是否遞迴查找所有子任務。

    - **處理邏輯**:
        - 當 `nested=False` 時，僅查詢 **當前層級** 的任務列表。
        - 當 `nested=True` 時，透過 **非同步請求** 遞迴查找所有層級的 `subtasks`。

    - **回應內容**:
        - **成功時**:
            - 返回完整的 **tasks** 和 **subtasks** 層級結構。
        - **失敗時**:
            - 若 `entity_id` 無效，返回錯誤訊息。
            - 若 API 請求失敗，返回錯誤代碼。
    """

    
    url = f"{api_config['base_url']}/resources/v1/modeler/projects/{entity_id}?$include=tasks"

    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        response = await loop.run_in_executor(pool, lambda: http_client.perform_request_with_retries(request, url, headers, method="GET"))

    if not response or response.status_code != 200:
        return {"error": f"API request failed with status {response.status_code}", "details": response.text}

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f" JSON 解析錯誤：{e}")
        return {"error": "Invalid JSON response", "raw_response": response.text}

    # 當 `nested=False`，直接返回 task 資料
    if not nested:
        return data

    all_tasks = []
    all_assignees = []

    # 檢查是否有子任務
    if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
        first_data = data['data'][0]

        if 'relateddata' in first_data and 'tasks' in first_data['relateddata']:
            tasks = first_data['relateddata']['tasks']

            if tasks:
                target = [
                    {
                        "id": task.get('id', 'N/A'),
                        "type": task.get('type', 'N/A'),
                        "title": task.get('dataelements', {}).get("title", "N/A"),
                        "description": task.get('dataelements', {}).get("description", "N/A"),
                        "state": task.get('dataelements', {}).get("state", "N/A"),
                        "status": task.get('dataelements', {}).get("status", "N/A"),
                        "criticalTask": task.get('dataelements', {}).get("criticalTask", "N/A"),
                        "percentComplete": task.get('dataelements', {}).get("percentComplete", "N/A"),
                        "estimatedStartDate": task.get('dataelements', {}).get("estimatedStartDate", "N/A"),
                        "dueDate": task.get('dataelements', {}).get("dueDate", "N/A"),
                        "estimatedDuration": task.get('dataelements', {}).get("estimatedDuration", "N/A"),
                        "typeicon": task.get('dataelements', {}).get("typeicon", "N/A"),
                        "subTasks": []
                    }
                    
                    for task in tasks
                ]
                # # **`ASSIGNEES_LIST` 需要的部分資料**
                # target_assignees = [
                #     {
                #         "id": task.get('id', 'N/A'),
                #         "type": task.get('type', 'N/A'),
                #         "title": task.get('dataelements', {}).get("title", "N/A"),
                #         "description": task.get('dataelements', {}).get("description", "N/A"),
                #         "state": task.get('dataelements', {}).get("state", "N/A"),
                #         "status": task.get('dataelements', {}).get("status", "N/A"),
                #         "assignee": ""  # 預設為空
                #     }
                #     for task in tasks
                # ]

                # 使用 asyncio.gather() 同時發送多個請求，提高查詢效率
                subtask_ids = [task["id"] for task in target]
                subtask_requests = [request_search_task_by_id(request,api_config, sub_id, nested=True,  is_root=False) for sub_id in subtask_ids]
                
                # ⚠️ 使用 `await` 確保 `asyncio.gather()` 正確執行
                subtask_results = await asyncio.gather(*subtask_requests)

                # 將查詢結果填入 `subTasks`
                for idx, subtask_data in enumerate(subtask_results):
                    target[idx]["subTasks"] = subtask_data if subtask_data else []

                all_tasks.extend(target)

    if is_root:
        ASSIGNEES_LIST_1 = request.app.state.ASSIGNEES_LIST_1
        
        for project in ASSIGNEES_LIST_1:
            if project.get("id") == entity_id:
                # **清理 `tasks` 資料，只保留必要欄位**
                project["tasks"] = [clean_task_data(task) for task in all_tasks]
                break


        root_data = {
            "id": first_data.get("id", "N/A"),
            "title": first_data["dataelements"].get("title", "N/A"),
            "Tasks": all_tasks
        }
        
        return root_data
         
    else:
        return all_tasks  # 內層只顯示 `Tasks`
# ------------------------- 建立 Task -------------------------

def request_create_task(request: Request, api_config: dict, task_data: dict):
    """建立新的 Task"""
    url = f"{api_config['base_url']}/resources/v1/modeler/tasks"
    
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    
    # 發送請求
    response = http_client.perform_request_with_retries(request, url, headers, method="POST", json=task_data)

    # 若請求失敗，直接返回錯誤
    if response:
        try:
            return response.json()  # **正常回傳 JSON 資料**
        except requests.exceptions.JSONDecodeError as e:
            print(f" JSON 解析錯誤：{e}")
            return {"error": "Invalid JSON response", "raw_response": response.text}
    else:
        return {"error": "Task Create failed"}   
# ------------------------- 更新 Task -------------------------

def request_update_task(request: Request,session: requests.Session, api_config: dict, task_data: dict):
    """更新 Task 資訊"""
    url = f"{api_config['base_url']}/resources/v1/modeler/tasks"
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    
    response =  http_client.perform_request_with_retries(request, session, url, headers, api_config["cert_path"], method="PUT", json=task_data)
    if response:
        try:
            return response.json()  # **正常回傳 JSON 資料**
        except requests.exceptions.JSONDecodeError as e:
            print(f" JSON 解析錯誤：{e}")
            return {"error": "Invalid JSON response", "raw_response": response.text}
    else:
        return {"error": "Task Update failed"}   
# ------------------------- 刪除 Task -------------------------

def request_delete_task_by_id(request: Request, api_config: dict, task_id: str):
    """根據 ID 刪除 Task"""
    url = f"{api_config['base_url']}/resources/v1/modeler/tasks/{task_id}"
    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response =  http_client.perform_request_with_retries(request, url, headers, method="DELETE")
    
    # 若請求失敗，直接返回錯誤
    if response:
        try:
            return response.json()  # **正常回傳 JSON 資料**
        except requests.exceptions.JSONDecodeError as e:
            print(f" JSON 解析錯誤：{e}")
            return {"error": "Invalid JSON response", "raw_response": response.text}
    else:
        return {"error": "Task deletion failed"}    
# ------------------------- 取得/更改 Task 的 assignees -------------------------

async def request_search_assignees_by_id(request: Request, api_config: dict, entity_id: str):
    """
    遍歷所有 `tasks` 及 `subTasks`，查找並填入 `assignees`，直到沒有子任務為止。
    
    - **確保 `ASSIGNEES_LIST_2` 中的 `tasks` 存入指派人**
    - **遞迴處理所有子任務，直到該層沒有 `subTasks`**
    - **`ASSIGNEES_LIST_1` 保持不變**
    """

    headers = {
        "ticket": api_config["infinite_ticket"],
        "SecurityContext": api_config["security_context"],
        "ENO_CSRF_TOKEN": api_config["csrf_token"],
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    
    ASSIGNEES_LIST_1 = request.app.state.ASSIGNEES_LIST_1
    ASSIGNEES_LIST_2 = request.app.state.ASSIGNEES_LIST_2

    # **遍歷 `ASSIGNEES_LIST_1`，查找對應專案**
    for item in ASSIGNEES_LIST_1:
        if item["id"] == entity_id:
            # print(f"Processing project: {item['title']}")

            async def fetch_assignees_for_task(task):
                """ 查找指定 `task` (含 `subTasks`) 的 `assignees`，並遞迴處理所有子任務 """
                task_id = task["id"]
                url = f"{api_config['base_url']}/resources/v1/modeler/tasks/{task_id}?$include=tasks"
                
                loop = asyncio.get_running_loop()
                with ThreadPoolExecutor() as pool:
                    response = await loop.run_in_executor(pool, lambda: http_client.perform_request_with_retries(request, url, headers, method="GET"))

                if not response or response.status_code != 200:
                    return  # 若 API 失敗，跳過該任務

                try:
                    try:
                        data = response.json().get("data", [])
                    except requests.exceptions.JSONDecodeError as e:
                        print(f" JSON 解析錯誤：{e}")
                        return {"error": "Invalid JSON response", "raw_response": response.text}
                    
                    if isinstance(data, list) and len(data) > 0:
                        first_item = data[0]  # 取第一個任務數據

                        if "relateddata" in first_item and "assignees" in first_item["relateddata"]:
                            assignees = first_item["relateddata"]["assignees"]
                            task["assignees"] = [
                                {
                                    "person_id": person.get("id", ""),
                                    "person_name": person.get("dataelements", {}).get("name", ""),
                                    "person_firstname": person.get("dataelements", {}).get("firstname", ""),
                                    "person_lastname": person.get("dataelements", {}).get("lastname", ""),
                                }
                                for person in assignees
                            ]
                        else:
                            task["assignees"] = []  # 確保 `assignees` 欄位存在

                except ValueError:
                    print(f"Failed to parse JSON response for task: {task['id']}")

                # **遞迴處理所有子任務**
                if "subTasks" in task and isinstance(task["subTasks"], list):
                    await asyncio.gather(*(fetch_assignees_for_task(subtask) for subtask in task["subTasks"]))

            # **對 `tasks` 的每一項任務執行查詢**
            await asyncio.gather(*(fetch_assignees_for_task(task) for task in item["tasks"]))

            # **更新 `ASSIGNEES_LIST_2` 中對應的 `tasks`**
            for target in ASSIGNEES_LIST_2:
                if target["id"] == entity_id:
                    target["tasks"] = item["tasks"]  # **同步 `tasks`**
                    break  # **找到後立即停止迴圈**

            break  # **找到專案後，不再檢查後續專案**
# -------------------------                           -------------------------

def clean_task_data(task):
    """
    遞迴清理 `task` 資料:
    - 只保留 `id`, `title`, `description`, `state`, `status`, `subTasks`
    - 新增 `assignees=''`
    - 遞迴處理 `subTasks`
    """
    return {
        "id": task.get("id", ""),
        "title": task.get("title", ""),
        "description": task.get("description", ""),
        "state": task.get("state", ""),
        "status": task.get("status", ""),
        "assignees": "",  # 新增 assignees 欄位
        "subTasks": [clean_task_data(subtask) for subtask in task.get("subTasks", [])]  # 遞迴處理 subTasks
    }

 
