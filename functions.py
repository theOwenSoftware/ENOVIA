import requests
import  xmltodict
import json
login_url = "https://3de24xplm.com.tw/3dspace/ticket/login"
csrf_url = "https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF"
cert = "./3de24xplm.crt"
infinite_ticket = "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"

# ----------------------------------------- Login & Ticket
def request_ticket_login(session, url, ticket, cert):
    """執行 ticket_login 請求"""
    try:
        response = session.get(url, params={"ticket": ticket}, verify=cert)
        if response.status_code == 200:
            print("ticket_login 成功 : ", response.text)
            return response
        else:
            print(f"ticket_login 失敗，狀態碼：{response.status_code}")
            # print("返回內容：", response.text)
    except requests.exceptions.RequestException as e:
        print("ticket_login 發生錯誤：", e)
    return None

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
            # 發送動態 HTTP 請求
            response = session.request(method=method, url=url, headers=headers, verify=cert, data=data, json=json)
            
            # 處理 200 成功狀態碼
            if response.status_code == 200:
                print("請求成功，返回內容：", response.json())
                return response
            
            # 特定錯誤處理
            if response.status_code == 403:
                print(f"403 錯誤：缺少 CSRF Token，第 {attempt + 1} 次重試")
                headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)
            elif response.status_code == 500:
                print(f"500 錯誤：服務端錯誤，第 {attempt + 1} 次重試")
                # print(response.data)
                # print(response.data.json())
                request_ticket_login(session, login_url, headers.get("ticket"), cert)
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

# ----------------------------------------- Get Request (project)

def request_search_project(session, url, ticket, security_context, csrf_token, cert):
    """執行 create_search 請求"""
    headers = {
        "ticket": ticket,
        "SecurityContext": security_context,
        "ENO_CSRF_TOKEN": csrf_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    print("11111")
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

# ----------------------------------------- Update Request (project)



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
    print("step2")
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
