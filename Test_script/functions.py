import requests
from pathlib import Path
import  xmltodict
import json
login_url = "https://3de24xplm.com.tw/3dspace/ticket/login"
csrf_url = "https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF"
# cert = "./3de24xplm.crt"
infinite_ticket = "RTIyRkM2RjYxOEU3NEU2RkFDRkNEOTI0RUVGQUVFQTF8ZGVtb3x8fHwwfA=="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"


BASE_DIR = Path(__file__).resolve().parent
CERT_PATH = BASE_DIR / "app" / "core" / "3de24xplm.crt"
cert = str(CERT_PATH)


if not CERT_PATH.exists():
    raise FileNotFoundError(f"找不到憑證文件: {CERT_PATH}")

print(f" 憑證完整路徑: {cert}")

# ----------------------------------------- Login & Ticket
def request_ticket_login(session, url, ticket, cert):
    """執行 ticket_login 請求"""
    try:
        response = session.get(url, params={"ticket": ticket}, verify=cert)
        if response.status_code == 200:
            print("ticket_login 成功 : ", response.text)
            return {
                "status": "success",
                "response_text": response.text  # 轉換為 JSON 可序列化格式
            }
        else:
            print(f"ticket_login 失敗，狀態碼：{response.status_code}")
            return {
                "status": "error",
                "status_code": response.status_code,
                "response_text": response.text
            }
    except requests.exceptions.RequestException as e:
        print("ticket_login 發生錯誤：", e)
        return {
            "status": "error",
            "error_message": str(e)
        }

def request_csrf(session, url, cert):
    """執行 CSRF Token 請求""" 
    try:
        response = session.get(url, verify=cert)
        if response.status_code == 200:
            print("CSRF Token 請求成功")
            response_data = response.json()
            csrf_value = response_data.get("csrf", {}).get("value", None)
            if csrf_value:
                print("CSRF Token 取得成功:", csrf_value)
                return csrf_value
            else:
                print("CSRF Token 解析失敗，未找到有效值")
        else:
            print(f"CSRF Token 請求失敗，狀態碼：{response.status_code}, 返回內容：{response.text}")
    except requests.exceptions.RequestException as e:
        print("CSRF Token 請求發生錯誤：", e)
    return None

# ----------------------------------------- Error handle
def perform_request_with_retries(session, url, headers, cert, max_retries=2, method="GET", data=None, json=None):
    """
    執行帶有重試邏輯的請求，支持多種 HTTP 方法。
    
    :param session: 請求的會話對象 (requests.Session)
    :param url: 請求的 URL
    :param headers: 請求頭部
    :param cert: 驗證證書
    :param max_retries: 最大重試次數
    :param method: HTTP 方法 (如 "GET", "POST", "DELETE")
    :param data: 請求的表單數據 (適用於 "POST")
    :param json: 請求的 JSON 數據 (適用於 "POST")
    """
    for attempt in range(max_retries):
        try:
            print(f"發送請求：{url}（第 {attempt + 1} 次嘗試）")
            response = session.request(method=method, url=url, headers=headers, verify=cert, data=data, json=json)
            
            # 成功請求
            if response.status_code == 200:
                print("請求成功，狀態碼：200")
                return response

            # 403 錯誤，更新 CSRF Token
            elif response.status_code == 403:
                print(f"403 錯誤：缺少 CSRF Token，第 {attempt + 1} 次重試")
                new_csrf = request_csrf(session, csrf_url, cert)
                if new_csrf:
                    headers["ENO_CSRF_TOKEN"] = new_csrf
                else:
                    print("CSRF Token 獲取失敗，停止重試")
                    return None

            # 500 錯誤，嘗試重新登入 **但最多只登入一次**
            elif response.status_code == 500:
                if attempt == 0:  # 只在第一次 500 錯誤時嘗試登入
                    print(f"500 錯誤：嘗試重新登入（第 {attempt + 1} 次）")
                    new_ticket = request_ticket_login(session, login_url, headers.get("ticket"), cert)
                    if new_ticket:
                        headers["ticket"] = new_ticket
                    else:
                        print("ticket_login 失敗，停止重試")
                        return None
                else:
                    print(f"500 錯誤：已嘗試重新登入但仍失敗，停止重試")
                    return None

            else:
                print(f"請求失敗，狀態碼：{response.status_code}, 返回內容：{response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"請求發生錯誤（第 {attempt + 1} 次）：", e)

    print("所有重試均失敗，操作失敗")
    return None

# ----------------------------------------- Post Request (project)

def request_create_project(session, url, ticket, security_context, csrf_token, req_body, cert):
    """執行 create_project 請求"""
    headers = {
        "ENO_CSRF_TOKEN": csrf_token,
        "ticket": ticket,
        "SecurityContext": security_context,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    print(req_body)
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="POST", json=req_body)
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

# ----------------------------------------- Get Request (project / task)

def request_search_project(session, url, ticket, security_context, csrf_token, cert):
    """執行 create_search 請求"""
    headers = {
        "ticket": ticket,
        "SecurityContext": security_context,
        "ENO_CSRF_TOKEN": csrf_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
   # 確保 CSRF Token 存在
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="GET")    
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

def request_search_project_by_id(session, url, ticket, security_context, csrf_token, cert):
    headers = {
        "ticket": ticket,
        "SecurityContext": security_context,
        "ENO_CSRF_TOKEN": csrf_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # 確保 CSRF Token 存在
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="GET")    
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

def request_search_allTask_by_id(session, url, ticket, security_context, csrf_token, cert):
    headers = {
        "ticket": ticket,
        "SecurityContext": security_context,
        "ENO_CSRF_TOKEN": csrf_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # 確保 CSRF Token 存在
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    all_tasks = []
    
    response = perform_request_with_retries(session, url, headers, cert, method="GET")
    
    if response:
            try:
                data = response.json()
                if 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0:
                    first_data = data['data'][0]
                    if 'relateddata' in first_data and 'tasks' in first_data['relateddata']:
                        tasks = first_data['relateddata']['tasks']
                        if tasks:
                            target = []
                            
                            for index, task in enumerate(tasks):
                                temp = {
                                    "index": index,
                                    "id": task.get('id', 'N/A'),
                                    "type": task.get('type', 'N/A'),
                                    "title": task.get('dataelements', {}).get("title", "N/A"),
                                    "description": task.get('dataelements', {}).get("description", "N/A"),
                                    "state":  task.get('dataelements', {}).get("state", "N/A"),
                                    "status": task.get('dataelements', {}).get("status", "N/A"),
                                    "criticalTask": task.get('dataelements', {}).get("criticalTask", "N/A"),
                                    "percentComplete": task.get('dataelements', {}).get("percentComplete", "N/A"),
                                    "estimatedStartDate":task.get('dataelements', {}).get("estimatedStartDate", "N/A"),
                                    "dueDate":task.get('dataelements', {}).get("dueDate", "N/A"),
                                    "estimatedDuration":task.get('dataelements', {}).get("estimatedDuration", "N/A"),
                                    "subTasks": []
                                }
                                print(f"索引 {index}: {temp}")
                                target.append(temp)
                            
                            # 修正 URL 組成方式，確保正確請求子任務
                            for subindex, subtask in enumerate(target):
                                subtask_url = f"https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects/{subtask['id']}?$include=tasks"
                                sub_tasks = request_search_allTask_by_id(session, subtask_url, ticket, security_context, csrf_token, cert)
                                if sub_tasks:
                                    target[subindex]["subTasks"] = sub_tasks  # 直接賦值，確保子任務正確存入
                            
                            all_tasks.extend(target)
                    else:
                        print("該Tasks 不存在subTasks，內容如下")
                        return ("該Tasks 不存在subTasks，內容如下",)

            except ValueError:
                print("返回的內容無法解析為 JSON")
    return all_tasks


def request_fetch_project_issues_by_id(session, url, ticket, security_context, csrf_token, cert):
    headers = {
        "ticket": ticket,
        "SecurityContext": security_context,
        "ENO_CSRF_TOKEN": csrf_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # 確保 CSRF Token 存在
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="GET")    
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

# ----------------------------------------- Delete Request (project)

def request_delete_project_by_id(session, url, ticket, security_context, csrf_token, cert):
    headers = {
        "ticket": ticket,
        "SecurityContext": security_context,
        "ENO_CSRF_TOKEN": csrf_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # 確保 CSRF Token 存在
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="DELETE")    
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

# ----------------------------------------- Update Request (project/task)

def request_update_project(session, url, ticket, security_context, csrf_token, req_body, cert):
    """執行 create_project 請求"""
    headers = {
        "ENO_CSRF_TOKEN": csrf_token,
        "ticket": ticket,
        "SecurityContext": security_context,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="PUT", json=req_body)
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

def request_update_task(session, url, ticket, security_context, csrf_token, req_body, cert):
    """執行 create_project 請求"""
    headers = {
        "ENO_CSRF_TOKEN": csrf_token,
        "ticket": ticket,
        "SecurityContext": security_context,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="PUT", json=req_body)
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

def request_update_project_by_id(session, url, ticket, security_context, csrf_token, req_body, cert):
    """執行 create_project 請求"""
    headers = {
        "ENO_CSRF_TOKEN": csrf_token,
        "ticket": ticket,
        "SecurityContext": security_context,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    print(req_body)
    if not headers.get("ENO_CSRF_TOKEN"):
        print("尚未取得有效的 CSRF Token，嘗試重新登入")
        request_ticket_login(session, login_url, ticket, cert)
        headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)

    # 執行請求
    response = perform_request_with_retries(session, url, headers, cert, method="POST", json=req_body)
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None
