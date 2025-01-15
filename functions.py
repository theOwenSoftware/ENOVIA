import requests
import  xmltodict
import json


# def request_ticket_login(session, url, ticket, cert):
#     """執行 ticket_login 的邏輯"""
#     params = {"ticket": ticket}
#     try:
#         response = session.get(url, params=params, verify=cert)
#         if response.status_code == 200:
#             return response.json()
#     except requests.exceptions.RequestException as e:
#         print("ticket_login 發生錯誤：", e)
#     return None


# def request_csrf(session, url, cert):
#     """執行 CSRF Token 的邏輯"""
#     try:
#         response = session.get(url, verify=cert)
#         if response.status_code == 200:
#             response_data = response.json()
#             return response_data.get("csrf", {}).get("value", None)
#     except requests.exceptions.RequestException as e:
#         print("CSRF Token 請求發生錯誤：", e)
#     return None






def request_ticket_login(session, url, ticket, cert):
    """執行 ticket_login 請求"""
    params = {"ticket": ticket}
    try:
        response = session.get(url, params=params, verify=cert)
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
                print("ENO_CSRF_TOKEN 取得成功:", csrf_value)
                return csrf_value
            else:
                print("CSRF Token 解析失敗，未找到有效值")
        else:
            print(f"CSRF Token 請求失敗，狀態碼：{response.status_code}")
            print("返回內容：", response.text)
    except requests.exceptions.RequestException as e:
        print("CSRF Token 請求發生錯誤：", e)


def request_create_project(session, url, ticket, security_context, csrf_token, req_body, cert):
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
            else:
                print(f"Project 創建失敗，狀態碼：{response.status_code}")
                print("返回內容：", response.text)
        else:
            print("錯誤：尚未取得有效的 ENO_CSRF_TOKEN，無法創建項目")
    except requests.exceptions.RequestException as e:
        print("Project 創建請求發生錯誤：", e)


