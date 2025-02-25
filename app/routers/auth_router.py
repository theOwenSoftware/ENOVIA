from fastapi import APIRouter, Depends
from app.core.dependencies import get_session, get_api_config
from app.utils.http_client import http_client
router = APIRouter()

@router.get("/login", summary="Retrieve authentication ticket")
def login(session=Depends(get_session), api_config=Depends(get_api_config)):
    """
    取得身份驗證 Ticket，用於後續 API 請求的授權。
    - **回應內容**:
        - 成功時，返回 Ticket 的授權資訊。
        - 失敗時，返回錯誤訊息，可能是因為 Ticket 已過期或憑證錯誤。
    """
    response = http_client.request_ticket_login()
    return response

@router.get("/csrf", summary="Retrieve CSRF token")
def csrf_token(session=Depends(get_session), api_config=Depends(get_api_config)):
    """
    獲取 CSRF Token，以進行受保護的 API 請求。
    
    - **回應內容**:
        - 成功時，返回最新可用的 CSRF Token。
        - 失敗時，返回錯誤訊息，可能原因：
            - Ticket 無效或過期，導致 Token 無法獲取。
            - 需要重新登入以獲取新的 Ticket。
    """
    csrf_token = http_client.request_csrf()
    api_config["csrf_token"] = csrf_token  # 更新全域 Token
    return {"csrf_token": csrf_token}
