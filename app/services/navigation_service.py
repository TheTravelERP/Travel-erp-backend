# app/services/navigation_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.menu_model import MenuMaster
from app.models.user_menu_permission_model import UserMenuPermission

async def get_user_navigation(db: AsyncSession, user_id: int, org_id: int):
    rows = await db.execute(
        select(MenuMaster, UserMenuPermission)
        .join(
            UserMenuPermission,
            UserMenuPermission.menu_id == MenuMaster.id
        )
        .where(
            UserMenuPermission.user_id == user_id,
            UserMenuPermission.can_view == True,
            MenuMaster.is_active == True
        )
        .order_by(MenuMaster.sort_order)
    )

    records = rows.all()

    # --- Build flat map ---
    node_map = {}
    for menu, perm in records:
        node_map[menu.id] = {
            "id": menu.key,
            "title": menu.title,
            "path": menu.path,
            "icon": menu.icon,
            "parent_id": menu.parent_id,
            "children": [],
            "permissions": {
                "can_view": perm.can_view,
                "can_create": perm.can_create,
                "can_edit": perm.can_edit,
                "can_delete": perm.can_delete,
                "can_export": perm.can_export,
                "can_import": perm.can_import,
                "can_print": perm.can_print,
                "data_scope": perm.data_scope,
            }
        }

    # --- Build tree ---
    tree = []
    for node in node_map.values():
        if node["parent_id"]:
            parent = node_map.get(node["parent_id"])
            if parent:
                parent["children"].append(node)
        else:
            tree.append(node)

    return tree
