from fastapi import Depends,Request
from pathlib import Path
import requests
from app.core import config

# 確保憑證路徑正確
BASE_DIR = Path(__file__).resolve().parent.parent
CERT_PATH = BASE_DIR / "core" / config.CERT_PATH

if not CERT_PATH.exists():
    raise FileNotFoundError(f"找不到憑證文件: {CERT_PATH}")

# FastAPI 依賴 - 共享 requests.Session()
def get_session():
    """提供共享 requests.Session，避免每次請求都重新建立 session"""
    session = requests.Session()
    return session

def get_csrf_token(request: Request):
    """從 FastAPI app.state 取得最新 CSRF Token"""
    return request.app.state.ENO_CSRF_TOKEN

# FastAPI 依賴 - 提供 API 設定
def get_api_config(request: Request):
    """提供 API 相關的共用設定"""
    csrf_token = request.app.state.ENO_CSRF_TOKEN  # 取得最新 CSRF Token

def get_api_config(request: Request):
    """提供 API 相關的共用設定，確保 csrf_token 為最新的"""
    csrf_token = request.app.state.ENO_CSRF_TOKEN  # 取得最新 CSRF Token
    return {
        "base_url": config.BASE_URL,
        "login_url": config.LOGIN_URL,
        "csrf_url": config.CSRF_URL,
        "csrf_token": csrf_token,  # 確保 CSRF Token 為最新
        "cert": str(CERT_PATH),
        "infinite_ticket": config.INFINITE_TICKET,
        "security_context": config.SECURITY_CONTEXT
    }