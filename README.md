# Backend Rebuild - FastAPI

此專案使用 **FastAPI** 作為後端框架，提供一個可拓充、易維護的後端基礎結構。以下說明專案目錄與各檔案功能。

---

## 專案結構

```plaintext
Backend_rebuild/
├── app/
│   ├── core/
│   │   ├── 3de24xplm.crt        # SSL 憑證檔，可搭配 HTTPS/驗證使用
│   │   ├── config.py            # 放置設定參數, e.g. DB連線、API金鑰等
│   │   └── dependencies.py      # FastAPI 依賴注入 (Dependency Injection) 相關函式
│   ├── models/
│   │   ├── project_model.py     # Project 相關的資料庫模型定義
│   │   └── task_model.py        # Task 相關的資料庫模型定義
│   ├── routers/
│   │   ├── auth_router.py       # 使用者驗證/登入/權限相關的路由
│   │   ├── project_router.py    # Project 模組對外 API 路由
│   │   └── task_router.py       # Task 模組對外 API 路由
│   ├── services/
│   │   ├── project_service.py   # Project 資料處理邏輯(商業邏輯)
│   │   └── task_service.py      # Task 資料處理邏輯(商業邏輯)
│   ├── utils/
│   │   └── http_client.py       # HTTP請求輔助函式（e.g. 對外部API呼叫）
├── TestScript                   # 測試用腳本，開發時測試功能（可忽略）
├── venv                         # Python 虛擬環境 (Virtual Environment)
├── main.py                      # FastAPI 入口檔，啟動後端服務
├── r2024x.crt                   # SSL 憑證檔
├── r2024x.key                   # SSL 金鑰檔
├── README.md                    # 專案說明文件 (你現在看到的文件)
├── requirements.txt             # Python 套件相依列表
```

## 安裝與使用
### 1.Clone 專案
```bash
git clone https://github.com/<YourRepo>/Backend_rebuild.git
```
### 2.建立並啟用虛擬環境
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3.安裝相依套件
```bash
pip install -r requirements.txt
```
### 4.啟動服務
```bash
uvicorn main:app --reload
```


### 5.瀏覽 API 文件
啟動後，瀏覽器開啟 http://127.0.0.1:8000/docs
可使用 Swagger UI 進行 API 測試。

## SSL 憑證檔

- **3de24xplm.crt** / **r2024x.crt** / **r2024x.key**
  - 這些是 HTTPS 或與特定服務安全連線所需的憑證檔與金鑰檔，如果部署需要 HTTPS，請設定伺服器端 (例如 Nginx 或其他) 使用。

> **注意**：若不需要 HTTPS，或在開發階段，你可以先忽略這些檔案；  
> 如果要正式上線，請確保正確安裝與設定 SSL 憑證與金鑰。
