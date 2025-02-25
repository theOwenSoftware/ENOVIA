from pydantic import BaseModel
from typing import List, Optional

class ProjectData(BaseModel):
    """Project data model for creating a project"""
    title: str
    description: Optional[str] = None
    state: str

class ProjectItem(BaseModel):
    """Project item containing project data"""
    id: str
    dataelements: ProjectData

class CreateProjectRequest(BaseModel):
    """Request model for creating a project"""
    data: List[ProjectItem]

class ProjectUpdateData(BaseModel):
    """Project update model for modifying an existing project"""
    title: Optional[str] = None
    description: Optional[str] = None
    state: Optional[str] = None
    project: Optional[str] = None
    percent_complete: Optional[float] = None  

class ProjectUpdateItem(BaseModel):
    """Project update item containing project update data"""
    id: str
    dataelements: ProjectUpdateData

class UpdateProjectRequest(BaseModel):
    """Request model for updating a project"""
    data: List[ProjectUpdateItem]
