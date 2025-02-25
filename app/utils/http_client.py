from typing import Optional
from fastapi import Request
import requests
import time
from app.core.config import LOGIN_URL, CSRF_URL, CERT_PATH, INFINITE_TICKET

class HttpClient:
    """處理 HTTP 請求、驗證 (登入 & CSRF)、錯誤重試"""

    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.ticket = INFINITE_TICKET
        self.last_login_time = 0  # 記錄最後一次登入時間
        self.last_ticket_response = None  # 儲存最後一次登入成功的回應

    def request_ticket_login(self):
        """執行 ticket_login"""
        """5分鐘內避免重複登入"""
        current_time = time.time()
         # 5 分鐘內，不重複登入，直接返回上次的結果
        if current_time - self.last_login_time < 180:
            print("3 分鐘內已登入，返回上次的 Ticket")
            return self.last_ticket_response
        
        # 重置 session
        print(" 清空 requests.Session ....")
        self.session = requests.Session()

        try:
            response = self.session.get(LOGIN_URL, params={"ticket": self.ticket}, verify=CERT_PATH)
            if response.status_code == 200:
                print("ticket_login 成功 : ", response.text)
                self.last_login_time = current_time  # 更新最後登入時間
                data = {
                "status": "success",
                "response_text": response.text  # 轉換為 JSON 可序列化格式
                }
                self.last_ticket_response = data # 儲存這次的登入回應
                return data
            else:
                print(f"ticket_login 失敗，狀態碼：{response.status_code}")
        except requests.exceptions.RequestException as e:
            print("ticket_login 發生錯誤：", e)
        return None

    def request_csrf(self, request: Optional[Request] = None):
        """執行 CSRF Token 請求"""
        try:
            headers = {"ticket": self.ticket}
            response = self.session.get(CSRF_URL, headers=headers, verify=CERT_PATH)

            if response.status_code == 200:
                self.csrf_token = response.json().get("csrf", {}).get("value", None)
                if request is not None:
                    print(" CSRF Token 請求成功：", self.csrf_token)
                    request.app.state.ENO_CSRF_TOKEN = self.csrf_token  # **全域存取 CSRF Token**
                return self.csrf_token
            else:
                print(f" CSRF Token 請求失敗，狀態碼: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(" CSRF Token 請求發生錯誤：", e)

            return None  # **返回 None，讓 perform_request_with_retries 正確判斷**

    
    

    def reset(self,request: Request,):
        """重置 session 並重新執行登入與 CSRF 設置"""
        print(" 重新初始化 session 與驗證...")
        self.session = requests.Session()  # **重設 session**
        self.csrf_token = None
        self.ticket = INFINITE_TICKET  # 重新使用初始 ticket

        # **執行 ticket 登入**
        if not self.request_ticket_login():
            print(" ticket_login 仍然失敗，放棄重試")
            return None

        if not self.request_csrf(request):  # **改為傳入 request**
            print(" CSRF Token 仍然無法獲取，放棄重試")
            return None

        print(" Reset 完成，嘗試重新執行請求")
        return True  # 表示 reset 成功，可再次發送請求

    def perform_request_with_retries(self, request: Request, url, headers, method="GET", data=None, json=None, max_retries=2):
        """執行帶有錯誤重試機制的 HTTP 請求"""
        for attempt in range(max_retries):
            try:
                response = self.session.request(method=method, url=url, headers=headers, verify=CERT_PATH, data=data, json=json)
                
                # **檢查是否為 JSON 格式**
                try:
                    response_json = response.json()
                except requests.exceptions.JSONDecodeError:
                    print(f" JSON 解析錯誤，可能是登入過期，嘗試重新登入...")
                    self.ticket = self.request_ticket_login()
                    headers["ticket"] = self.ticket
                    continue  # **重新發送請求**
                    
                # **正常返回 JSON 時，檢查狀態碼**
                if response.status_code == 200:
                    return response

                elif response.status_code == 403:
                    print(f"⚠️ 403 錯誤：嘗試更新 CSRF Token")
                    self.csrf_token = self.request_csrf(request)  # **改為傳入 request**
                    if self.csrf_token:
                        headers["ENO_CSRF_TOKEN"] = self.csrf_token
                        request.app.state.ENO_CSRF_TOKEN = self.csrf_token  # **全域更新 CSRF Token**
                        continue  # **重新發送請求**

                elif response.status_code == 500 and attempt == 0:
                    print(f"500 錯誤：嘗試重新登入")
                    self.ticket = self.request_ticket_login()
                    if self.ticket:
                        headers["ticket"] = self.ticket

            except requests.exceptions.RequestException as e:
                print(f"請求錯誤（第 {attempt + 1} 次）：", e)

        # **所有重試均失敗，執行 reset**
        print("所有重試均失敗，執行 reset")
        if self.reset(request):
            print(" Reset 完成，嘗試最後一次請求...")
            return self.session.request(method=method, url=url, headers=headers, verify=CERT_PATH, data=data, json=json)

        return {"error": "所有重試均失敗，無法執行請求"}


# 初始化 HttpClient
http_client = HttpClient()
