from pathlib import Path

# 設定 BASE_DIR 指向 app 目錄
BASE_DIR = Path(__file__).resolve().parent.parent

# API 端點
BASE_URL = "https://3de24xplm.com.tw/3dspace"
LOGIN_URL = f"{BASE_URL}/ticket/login"
CSRF_URL = f"{BASE_URL}/resources/v1/application/CSRF"
# 憑證與安全配置
CERT_PATH = (BASE_DIR / "core" / "3de24xplm.crt").resolve()  # 使用 .resolve() 轉換為絕對路徑
INFINITE_TICKET = "RTIyRkM2RjYxOEU3NEU2RkFDRkNEOTI0RUVGQUVFQTF8ZGVtb3x8fHwwfA=="
SECURITY_CONTEXT = "VPLMProjectLeader.Company Name.DEMO_CS"

# 確保憑證檔案存在
if not CERT_PATH.exists():
    raise FileNotFoundError(f"憑證檔案不存在: {CERT_PATH}")

print(f"憑證完整路徑: {str(CERT_PATH)}")
