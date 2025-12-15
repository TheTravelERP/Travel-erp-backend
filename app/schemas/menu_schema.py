# app/schemas/menu_schema.py
from pydantic import BaseModel
from typing import List, Optional

class MenuPermissionOut(BaseModel):
    can_view: bool
    can_create: bool
    can_edit: bool
    can_delete: bool
    can_export: bool
    can_import: bool
    can_print: bool
    data_scope: str

class MenuNodeOut(BaseModel):
    id: str
    title: str
    path: Optional[str]
    icon: Optional[str]
    children: List["MenuNodeOut"] = []
    permissions: MenuPermissionOut

MenuNodeOut.model_rebuild()
