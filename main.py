import logging
import asyncio
import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.routers.project_router import router as project_router
from app.routers.task_router import router as task_router
from app.routers.auth_router import router as auth_router

from app.core.config import LOGIN_URL, CSRF_URL, CERT_PATH, INFINITE_TICKET
from app.core.dependencies import get_session, get_api_config
from app.utils.http_client import http_client


# 設置日誌記錄，忽略 `ConnectionResetError`
logging.getLogger("uvicorn.error").addFilter(
    lambda record: "ConnectionResetError" not in record.getMessage()
)

# 共享狀態管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """應用啟動時的初始化邏輯"""
    
    login_success = http_client.request_ticket_login()
    if not login_success:
        raise RuntimeError("Ticket 登入失敗，請檢查INFINITE_TICKET:",INFINITE_TICKET)
    
    csrf_token = http_client.request_csrf(None)  # **傳入 None**
    if not csrf_token:
        raise RuntimeError("CSRF Token取得失敗，請檢查登入狀態")
    
    app.state.LOGIN = csrf_token  
    app.state.ENO_CSRF_TOKEN = csrf_token  # 儲存 CSRF Token
    app.state.LAST_PROJECT_ID = []  # 初始化專案 ID 清單
    app.state.ASSIGNEES_LIST_1 = [] 
    app.state.ASSIGNEES_LIST_2 = [] 
    print("Application startup")
    yield  # 讓應用繼續運行
    print("Application shutdown")


# 建立 FastAPI 應用
app = FastAPI(lifespan=lifespan)

# 設置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加入 Routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(project_router, tags=["Project Management"])
app.include_router(task_router, tags=["Task Management"])

# 入口測試
@app.get("/", summary="測試 API")
async def root():
    """測試 FastAPI 是否正常運行"""
    return {"message": "FastAPI 服務正常運行"}

# Windows 平台上顯式設定 `SelectorEventLoop`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",  # 指定應用程式的 module:instance
        host="192.168.50.145",
        port=8100,
        # log_level="critical",  # 只顯示嚴重錯誤，忽略連線中斷
        ssl_keyfile="./r2024x.key",  # SSL 私鑰
        ssl_certfile="./r2024x.crt"  # SSL 憑證
    )