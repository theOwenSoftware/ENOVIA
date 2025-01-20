import requests
import  xmltodict
import json
login_url = "https://3de24xplm.com.tw/3dspace/ticket/login"
csrf_url = "https://3de24xplm.com.tw/3dspace/resources/v1/application/CSRF"
cert = "./3de24xplm.crt"
infinite_ticket = "NkM1OEY5NEY3MEYzNEJEN0I3MjZFNDc2MDY2RTRDRjl8bmlra2l8fHx8MHw="
security_context = "VPLMProjectLeader.Company Name.DEMO_CS"


def request_ticket_login(session, url, ticket, cert):
    """執行 ticket_login 請求"""
    try:
        response = session.get(url, params={"ticket": ticket}, verify=cert)
        if response.status_code == 200:
            print("ticket_login 成功 : ", response.text)
            return response.text
        else:
            print(f"ticket_login 失敗，狀態碼：{response.status_code}")
            print("返回內容：", response.text)
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

def perform_request_with_retries(session, url, headers, cert, max_retries=2):
    """執行帶有重試邏輯的請求"""
    for attempt in range(max_retries):
        try:
            response = session.get(url, headers=headers, verify=cert)
            if response.status_code == 200:
                print("請求成功，返回內容：", response.json())
                return response
            if response.status_code == 403:
                print(f"403 錯誤：缺少 CSRF Token，第 {attempt + 1} 次重試")
                headers["ENO_CSRF_TOKEN"] = request_csrf(session, csrf_url, cert)
            elif response.status_code == 500:
                print(f"500 錯誤：服務端錯誤，第 {attempt + 1} 次重試")
                request_ticket_login(session, login_url, headers.get("ticket"), cert)
            else:
                print(f"請求失敗，狀態碼：{response.status_code}, 返回內容：{response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"請求發生錯誤（第 {attempt + 1} 次）：", e)

    print("所有重試均失敗，操作失敗")
    return None

def request_project_create(session, url, ticket, security_context, csrf_token, req_body, cert, csrf_url):
    """執行 create_project 請求"""
    headers = {
        "ENO_CSRF_TOKEN": csrf_token,
        "ticket": ticket,
        "SecurityContext": security_context,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        if headers.get("ENO_CSRF_TOKEN"):
            response = session.post(url, headers=headers, json=req_body, verify=cert)
            
            if response.status_code == 200:
                print("Project 創建成功，返回內容（JSON）：", response.json())
                return response.json()

            elif response.status_code == 403:
                print("請求錯誤: 缺少 ENO_CSRF_TOKEN，嘗試重新獲取 CSRF Token")
                # 獲取新的 CSRF Token
                new_csrf_token = request_csrf(session, csrf_url, cert)
                if new_csrf_token:
                    headers['ENO_CSRF_TOKEN'] = new_csrf_token  # 更新 CSRF Token
                    print("重新嘗試創建項目...")
                    retry_response = session.post(url, headers=headers, json=req_body, verify=cert)
                    
                    if retry_response.status_code == 200:
                        print("重新嘗試成功，項目創建完成，返回內容（JSON）：", retry_response.json())
                        return retry_response.json()
                    else:
                        print(f"重新嘗試仍失敗，狀態碼：{retry_response.status_code}")
                        print("返回內容：", retry_response.text)
                        return None
                else:
                    print("無法重新獲取 CSRF Token，操作失敗")
                    return None
            

            else:
                print(f"Project 創建失敗，狀態碼：{response.status_code}")
                print("返回內容：", response.text)
                return None
        else:
            print("錯誤：尚未取得有效的 ENO_CSRF_TOKEN，無法創建項目")
            return None

    except requests.exceptions.RequestException as e:
        print("Project 創建請求發生錯誤：", e)
        return None

def request_project_search(session, url, ticket, security_context, csrf_token, cert):
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
    response = perform_request_with_retries(session, url, headers, cert)
                 
    if response:
        try:
            return response.json()
        except ValueError:
            print("返回的內容無法解析為 JSON")
            return  response.text()

    print("搜尋請求最終失敗")
    return None

def request_project_search_ID(session, url, ticket, security_context, csrf_token, cert):
    headers = {
        "ticket": ticket,
        "SecurityContext": security_context,
        "ENO_CSRF_TOKEN": csrf_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    # print(headers)
    try:
        if headers.get("ENO_CSRF_TOKEN"):
            response = session.get(url, headers=headers, verify=cert)
            if response.status_code == 200:
                print("Project 搜尋成功 ，返回內容（JSON）：", response.json())
                return response.json()
           
            elif response.status_code == 403:
                print(f"Project 搜尋失敗，狀態碼：{response.status_code}")
                print("請求錯誤: 缺少 ENO_CSRF_TOKEN，嘗試重新獲取 CSRF Token")
                
                # 獲取新的 CSRF Token
                new_csrf_token = request_csrf(session, csrf_url, cert)
                if new_csrf_token:
                    headers['ENO_CSRF_TOKEN'] = new_csrf_token  # 更新 CSRF Token
                    print("重新嘗試搜尋項目...")
                    retry_response = session.get(url, headers=headers, verify=cert)
                    
                    if retry_response.status_code == 200:
                        print("重新搜尋成功，返回內容（JSON）：", retry_response.json())
                        return retry_response.json()
                    else:
                        print(f"重新嘗試仍失敗，狀態碼：{retry_response.status_code}")
                        print("返回內容：", retry_response.text)
                        return None
                else:
                    print("無法重新獲取 CSRF Token，操作失敗")
                    return None
            else:
                print(f"Project 搜尋失敗，狀態碼：{response.status_code}")
                print("返回內容：", response.text)
        else:
            print("錯誤：尚未取得有效的 ENO_CSRF_TOKEN，無法搜尋項目")
    except requests.exceptions.RequestException as e:
        print("Project 搜尋請求發生錯誤：", e)

