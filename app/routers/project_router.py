from fastapi import APIRouter, Depends
import requests
from fastapi import APIRouter, Depends, Request

from app.models.project_model import CreateProjectRequest, UpdateProjectRequest
from app.core.dependencies import get_session, get_api_config,get_csrf_token
from app.services.project_service import (
    request_search_project,
    request_search_project_by_id,
    request_create_project,
    request_update_project,
    request_delete_project_by_id,
)

router = APIRouter(
    prefix="/project",
    tags=["Project Management"]
)

@router.get("/search", summary="Retrieve filtered project list")
def search_projects(
    request: Request,  # 加入 Request 物件
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
    ):
    """取得經過過濾的專案列表，返回關鍵項目資訊"""
    
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    response =  request_search_project(request, api_config, detail=False) 
    return response

@router.get("/search/detail", summary="Retrieve full project list")
def search_projects(
    request: Request,  # 加入 Request 物件
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
    ):
    """取得完整的專案列表，包含所有細節資訊"""
    
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    return request_search_project(request, api_config,detail=True) 

@router.get("/search/{project_id}", summary="Retrieve project details by ID")
def search_project_by_id(
    request: Request,  # 加入 Request 物件
    project_id: str,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
):
    """根據專案 ID 查詢詳細資訊，返回完整專案數據"""
    
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    return request_search_project_by_id(request,api_config, project_id)

@router.post("/create", summary="Create a new project")
async def create_project(
    request: Request,  # 加入 Request 物件
    request_body: CreateProjectRequest,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
):
    """建立新的專案，根據請求的數據創建專案並回傳結果"""
    
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    return request_create_project(request,api_config, request_body.model_dump())


@router.put("/update", summary="Update an existing project")
def update_project(
    request: Request,  # 加入 Request 物件
    request_body: UpdateProjectRequest,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)

):
    """
    更新指定專案的詳細資訊。

    此請求會根據提供的專案 ID 和數據，更新專案的標題、描述、狀態等屬性。
    
    回應:
    - 成功時返回更新後的專案資料。
    - 失敗時返回錯誤訊息。
    """
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    return request_update_project (request, api_config, request_body.model_dump())

@router.delete("/delete/{project_id}", summary="Delete project by ID")
def delete_project_by_id(
    request: Request,  # 加入 Request 物件
    project_id: str,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
):
    """
    根據專案 ID 刪除專案。

    回應:
    - 成功時返回刪除確認資訊。
    - 若專案 ID 不存在，則返回錯誤訊息。

    """    
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    return request_delete_project_by_id(request,  api_config, project_id)
