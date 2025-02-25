from fastapi import APIRouter, Depends, Request
import requests
import asyncio
from app.models.task_model import UpdateTaskRequest,CreateTaskRequest
from app.core.dependencies import get_session, get_api_config,get_csrf_token
from app.services.task_service import (
    request_search_task_by_id,
    request_create_task,
    request_update_task,
    request_delete_task_by_id,
    request_search_assignees_by_id,
)
from app.services.project_service import (
    request_search_project,
)

router = APIRouter(
    prefix="/task",
    tags=["Task Management"]
)

@router.get("/search/{project_id}", summary="Retrieve tasks for a project (returns only direct subtasks)")
async def search_task_by_project_id(
    request: Request,  # 加入 Request 物件
    project_id: str,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)

):
    """
    根據任務 ID (`Project_id`) 查詢該專案的詳細資訊，並返回該任務的 **直接子任務 (subtasks)**，  
    但不會遞迴查找更深層的子任務。

    ---
    
    ### **請求參數**
    - `Project_id` (**str**): 目前專案的 ID，將作為查詢的起點。

    ### **處理邏輯**
    1. 透過 API 取得 **該專案 (`Project_id`) 的詳細資訊**。
    2. 查找該任務的 **第一層直接關聯的 subtasks**，但不會進一步遞迴查找 deeper subtasks。
    3. 返回的 `subTasks` 屬性僅包含該專案的直接子任務，而非所有層級的子任務。

    - **回應內容**:
    - **成功時**:
        - 返回該專案的完整結構，包括所有 **tasks**。
    - **失敗時**:
        - 若 `Project_id` 不存在，返回錯誤訊息。
        - 若 API 請求失敗，返回錯誤代碼。
        
    ### **適用場景**
    - 當前端只需要查詢 **單一任務及其直接關聯的子任務**。
    - 當不需要完整的遞迴結構，只關心當前專案的第一層子任務。
    - 用於快速獲取任務概覽，而不載入完整的專案結構。
    """
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    
    return await request_search_task_by_id(request,api_config, project_id, nested=False)

@router.get("/search/{project_id}/nested", summary="Retrieve all tasks and subtasks for a project")
async def search_all_tasks_by_project_id(
    request: Request,  # 加入 Request 物件
    project_id: str,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
    ):
    """
    根據專案 ID (`Project_id`) 查詢該專案下的 **所有任務 (tasks) 及子任務 (subtasks)**，
    直到所有層級的 subtasks 都被找到。

    - **請求參數**:
        - `Project_id` (str): 目標專案的 ID。

    - **處理邏輯**:
        - 透過 API 遞迴搜尋該專案下的所有任務。
        - 若某個任務包含子任務，則繼續深入查找，直到所有 subtasks 都被解析完成。

    - **回應內容**:
        - **成功時**:
            - 返回該專案的完整任務結構，包括所有 **tasks** 和 **subtasks**。
        - **失敗時**:
            - 若 `Project_id` 不存在，返回錯誤訊息。
            - 若 API 請求失敗，返回錯誤代碼。

    - **適用場景**:
        - 當需要查詢某專案內部的所有工作結構時，例如顯示完整的專案進度圖 (Gantt Chart) 或任務層級關聯時。
    """
    # 確保最新 CSRF Token
    api_config["csrf_token"] = csrf_token  
    
    # **檢查 `ASSIGNEES_LIST_2` 是否可用**
    if not hasattr(request.app.state, "ASSIGNEES_LIST_1") or not isinstance(request.app.state.ASSIGNEES_LIST_1, list):
        raise ValueError("ASSIGNEES_LIST_1 is not properly initialized") 
    
    # **獲取 ASSIGNEES_LIST_1**
    assignees_list = request.app.state.ASSIGNEES_LIST_1
    
    # **檢查 project_id 是否存在於 ASSIGNEES_LIST_1，若不存在則重新執行 `request_search_project`**
    if not any(item["id"] == project_id for item in assignees_list):
        print(f"Project {project_id} not found in ASSIGNEES_LIST_1. Fetching data...")
        await asyncio.to_thread(request_search_project, request, api_config, detail=False)
    
   # **嘗試獲取任務數據**
    try:
        response = await request_search_task_by_id(request, api_config, project_id, nested=True)
    except Exception as e:
        return {"error": f"Failed to fetch tasks for project {project_id}", "details": str(e)}
    
    # **啟動異步任務來查找 assignees，不影響 API 回應時間**
    asyncio.create_task(request_search_assignees_by_id(request, api_config, project_id))
    
    return response

@router.get("/search/{task_id}", summary="Retrieve task details (returns only direct subtasks)")
async def search_task_by_task_id(
    request: Request,  # 加入 Request 物件
    task_id: str,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)

):
    """
    根據任務 ID (`Task_id`) 查詢該任務的詳細資訊，並返回該任務的 **直接子任務 (subtasks)**，  
    但不會遞迴查找更深層的子任務。

    ---
    
    ### **請求參數**
    - `Task_id` (**str**): 目標任務的 ID，將作為查詢的起點。

    ### **處理邏輯**
    1. 透過 API 取得 **該任務 (`Task_id`) 的詳細資訊**。
    2. 查找該任務的 **第一層直接關聯的 subtasks**，但不會進一步遞迴查找 deeper subtasks。
    3. 返回的 `subTasks` 屬性僅包含該任務的直接子任務，而非所有層級的子任務。

    - **回應內容**:
    - **成功時**:
        - 返回該專案的完整任務結構，包括所有 **tasks**。
    - **失敗時**:
        - 若 `Task_id` 不存在，返回錯誤訊息。
        - 若 API 請求失敗，返回錯誤代碼。
        
    ### **適用場景**
    - 當前端只需要查詢 **單一任務及其直接關聯的子任務**。
    - 當不需要完整的遞迴結構，只關心當前任務的第一層子任務。
    - 用於快速獲取任務概覽，而不載入完整的專案結構。
    """
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    return await request_search_task_by_id(request, api_config, task_id, nested=False)

@router.get("/search/{task_id}/nested", summary="Retrieve all tasks and subtasks for a Task")
async def search_all_tasks_by_task_id(
    request: Request,
    task_id: str,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
    ):
    """
    根據 **專案 ID (`Task_id`)** 查詢該任務下的 **所有子任務 (`subtasks`)**，  
    透過遞迴方式，直到所有層級的 `subtasks` 都被完整獲取。


    - **請求參數**:
        - `Task_id` (str): 目標任務的 ID。

    - **處理邏輯**:
        - 透過 API 遞迴搜尋該任務下的所有任務。
        - 若某個任務包含子任務，則繼續深入查找，直到所有 subtasks 都被解析完成。

    - **回應內容**:
        - **成功時**:
            - 返回該任務的完整結構，包括所有**subtasks**。
        - **失敗時**:
            - 若 `Task_id` 不存在，返回錯誤訊息。
            - 若 API 請求失敗，返回錯誤代碼。

    - **適用場景**:
        - 當需要查詢某任務內部的所有工作結構時，例如顯示完整的專案進度圖 (Gantt Chart) 或任務層級關聯時。
    """
   
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    return await request_search_task_by_id(request, api_config, task_id, nested=True)

@router.post("/create/{project_id}", summary="Create a new task") 
async def create_task(
    project_id: str,
    request: Request,  # 加入 Request 物件
    request_body: CreateTaskRequest,
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
):
    """
    創建新任務。

    - **請求內容**:
        - `title` (str | 必填): 任務標題。
        - `description` (str | 選填): 任務描述。
        - `percentComplete` (float | 選填): 完成度 (0-100)。
        - `estimatedStartDate` (str | 選填): 預計開始日期 (ISO 8601)。
        - `dueDate` (str | 選填): 任務到期日 (ISO 8601)。
        - `estimatedDuration` (float | 選填): 預計工時 (小時)。
      

    - **處理邏輯**:
        1. 直接從 URL 參數 `project_id` 取得專案 ID。
        2. 自動將 `project_id` 填入 `relateddata.DPMProject.id`，用戶無需手動填寫。        
        3. 使用最新的 CSRF Token 進行驗證。
        4. 發送請求至 API 伺服器， 將任務新增至該專案中。
        . 返回建立結果。

    - **回應內容**:
        - **成功**: 返回新建任務的詳細資訊 (任務 ID、專案 ID)。
        - **失敗**: 
            - `403 Forbidden` - CSRF Token 過期。
            - `400 Bad Request` - 請求格式錯誤。
            - `500 Internal Server Error` - API 內部錯誤。

    - **適用場景**:
        - 用戶在專案管理系統內新增任務。
        - 適用於多層級任務結構的專案管理需求。
    """
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    
    # 取得請求數據並自動補充 `relateddata.DPMProject.id`
    task_data = request_body.model_dump()
    
    for item in task_data["data"]:
        item["relateddata"] = {"DPMProject": [{"id": project_id}]}  

    return request_create_task(request,api_config, task_data)   

@router.delete("/delete/{task_id}", summary="Delete an existing task only if percentComplete is 0")
def delete_task(
    task_id: str,
    request: Request,  # 加入 Request 物件

    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
):
    """
    刪除指定的任務，但僅當 `percentComplete` 為 0 時允許刪除。

    - **請求參數**:
        - `task_id` (str | 必填): 需要刪除的任務 ID，該任務的 `percentComplete` 必須為 0。

    - **處理邏輯**:
        1. 透過 API 取得指定任務 (`task_id`) 的詳細資訊。
        2. 檢查該任務的 `percentComplete` 是否為 0：
            - 若為 0，則執行刪除請求。
            - 若 `percentComplete > 0`，則返回錯誤，拒絕刪除。
        3. 使用最新的 CSRF Token 進行請求驗證。

    - **回應內容**:
        - **成功時**:
            - 返回 `success: true`，表示任務已成功刪除。
        - **失敗時**:
            - 若 `task_id` 無效，返回 `404 Not Found`。
            - 若 `percentComplete > 0`，返回 `400 Bad Request`，不允許刪除。
            - 若 CSRF Token 過期，返回 `403 Forbidden`。
            - 若 API 內部錯誤，返回 `500 Internal Server Error`。

    - **適用場景**:
        - 當用戶需要刪除尚未開始 (`percentComplete = 0`) 的任務時，例如錯誤建立的任務。
    """
    api_config["csrf_token"] = csrf_token  # 確保最新 CSRF Token
    
    return request_delete_task_by_id(request,api_config, task_id)

@router.get("/search/assignees/{project_id}", summary="Retrieve task assignees by project ID")
async def search_task_assignees_by_id(
    request: Request,  # 加入 Request 物件
    project_id: str,  # 這裡修正名稱
    session: requests.Session = Depends(get_session),
    api_config: dict = Depends(get_api_config),
    csrf_token: str = Depends(get_csrf_token)
):
    """
    根據 `project_id` 查詢對應的 `ASSIGNEES_LIST_2` 內的數據。

    - **請求參數**:
        - `project_id` (str): 目標專案的 ID。

    - **處理邏輯**:
        - 檢查 `request.app.state.ASSIGNEES_LIST_2` 是否已初始化。
        - 查找 `ASSIGNEES_LIST_2` 內的對應 `id`，返回對應的數據。
        - 如果 `project_id` 尚未加入 `ASSIGNEES_LIST_2`，則觸發 `search_all_tasks_by_project_id()` 來獲取完整的 `tasks`。

    - **回應內容**:
        - **成功時**: 返回該 `project_id` 的 `assignees` 數據。
        - **失敗時**: 若 `project_id` 不存在，返回 `None`。

    """
    
    # **檢查 `ASSIGNEES_LIST_2` 是否可用**
    if not hasattr(request.app.state, "ASSIGNEES_LIST_2") or not isinstance(request.app.state.ASSIGNEES_LIST_2, list):
        raise ValueError("ASSIGNEES_LIST_2 is not properly initialized")
    
    # **獲取 ASSIGNEES_LIST_2**
    assignees_list = request.app.state.ASSIGNEES_LIST_2
    
    # **使用 `next()` 高效查找 `project_id`，找不到時回傳 `None`**
    project_data = next((item for item in assignees_list if item["id"] == project_id), None)

    # **如果 `project_id` 不在 `ASSIGNEES_LIST_2`，則先執行 `search_all_tasks_by_project_id()`**
    if not project_data:
        print(f"Project {project_id} not found in ASSIGNEES_LIST_2. Fetching data...")
        
        # **確保 `search_all_tasks_by_project_id()` 完成後再繼續執行**
        await search_all_tasks_by_project_id(
            request=request,
            project_id=project_id,
            session=session,
            api_config=api_config,
            csrf_token=csrf_token
        )

        # **再次嘗試查找 `project_id`**
        project_data = next((item for item in assignees_list if item["id"] == project_id), None)

        # **如果仍然找不到，回傳錯誤信息**
        if not project_data:
            return {"error": f"Project {project_id} not found even after fetching data."}

    # **執行 `request_search_assignees_by_id()` 來查找 `assignees`**
    await request_search_assignees_by_id(request, api_config, project_id)

    # **返回 `project_id` 的完整 `assignees` 數據**
    return project_data