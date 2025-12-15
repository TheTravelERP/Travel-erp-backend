# app/utils/data_scope.py
from sqlalchemy.orm import Query
from app.models.user_menu_permission_model import UserMenuPermission

def apply_data_scope(query: Query, model, user, scope: str):
    if scope == "GLOBAL":
        return query

    if scope == "ORG":
        return query.filter(model.org_id == user.org_id)

    if scope == "TEAM":
        return query.filter(model.created_by.in_(user.team_user_ids))

    # OWN
    return query.filter(model.created_by == user.id)
