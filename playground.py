# 請求 A 的參數
params_a = {
    "identifier": username,
    "service": f"{url_3dspace}/resources/v1/modeler/tasks",
}

headers_a = {
    "Accept": "application/json",
    "DS-Service-Name": DSServiceName,
    "DS-Service-Secret": DSServiceSecret,
}

try:
    response_a_1 = session.get(
        f"{url_3dpassport}/api/v2/batch/ticket",
        params=params_a,
        headers=headers_a,
        verify=cert,  # 在測試環境下禁用 SSL 驗證
    )
    if response_a_1.status_code == 200:
        data = response_a_1.json()

        x3dsreauthurl = data["x3ds_reauth_url"]
        print("Request A 成功，Cookie 已儲存至 Session")

        print("返回內容：", response_a_1.json())
    else:
        print("Request A 失敗，狀態碼：", response_a_1.status_code)
        print("返回內容：", response_a_1.text)
except requests.exceptions.RequestException as e:
    print("Request A 發生錯誤：", e)

# 檢查 Session 中的 Cookie
print("Session Cookies:", session.cookies)



# Request_2
try:
    # 發送 GET 請求
    response = session.get(x3dsreauthurl,    
    headers=headers_a, 
    verify=cert)

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

# 請求 B：使用請求 A 的 Cookie
try:
    response_b = session.post(
        "https://3de24xplm.com.tw/3dspace/resources/v1/modeler/projects",
        headers=headers_b,
        params=params_b,
        json=request_body_b,
        verify=cert, 
    )
    # print("Session Cookies After POST:", session.cookies)
    if response_b.status_code == 200:
        print("Request B 成功")
        print("返回內容：", response_b.json())
    else:
        print("Request B 失敗，狀態碼：", response_b.status_code)
        print("返回內容：", response_b.text)
except requests.exceptions.RequestException as e:
    print("Request B 發生錯誤：", e)
    print("返回內容：", response_b.text)

