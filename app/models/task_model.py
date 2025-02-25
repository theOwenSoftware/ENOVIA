from pydantic import BaseModel, Field,field_validator
from typing import List, Optional,Dict

# Task Data Model 
class TaskData(BaseModel):
    """ Task data model containing essential attributes. """
    title: Optional[str] = Field("New Task", description="Task title.")
    description: Optional[str] = Field("This is a new task.", description="Task description.")
    percentComplete: Optional[float] = Field(0.0, description="Completion percentage (0-100).")
    estimatedStartDate: Optional[str] = Field(None, description="Estimated start date (ISO 8601).")
    dueDate: Optional[str] = Field(None, description="Due date (ISO 8601).")
    estimatedDuration: Optional[float] = Field(None, description="Estimated duration (hours).")
    
    @field_validator("title", "description", mode="before")
    @classmethod
    def set_default_if_empty(cls, value, info):
        """
        If the input is an empty string, replace it with the default value.
        """
        if value == "":
            field_name = info.field_name  # 獲取欄位名稱
            return cls.model_fields[field_name].default  # 取得該欄位的預設值
        return value

# **DPMProject Model** (Mandatory Project ID)
class DPMProject(BaseModel):
    """Represents the related project. The `id` field is required."""
    id: str = Field(..., description="Project ID that this task belongs to.")
    
# Task Item for Creation (ID Not Included, System-Assigned)
class TaskItem(BaseModel):
    """Task item for creating a new task. Task ID is system-assigned."""
    dataelements: TaskData
    # relateddata: Dict[str, List[DPMProject]] = Field(
    #     ...,
    #     description="Related project in format {'DPMProject': [{'id': 'project_id'}]}."
    # )

# **CreateTaskRequest**: No Task ID Needed (Auto-Assigned)
class CreateTaskRequest(BaseModel):
    """Request model for creating new tasks. The system assigns the task ID automatically."""
    data: List[TaskItem]

# **UpdateTaskRequest**: Requires Task ID (For Modifications)
class UpdateTaskRequest(BaseModel):
    """Request model for updating an existing task. Task ID is required."""
    task_id: str = Field(..., description="Task ID to update.")  # Required
    dataelements: TaskData  # Only send the fields that need updates