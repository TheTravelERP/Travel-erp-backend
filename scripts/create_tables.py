# # scripts/create_tables.py
# import asyncio
# from app.db.database import engine
# from app.db.base import Base

# # import all models here:
# import app.models.organization_model
# import app.models.user_model

# async def create_all():
#     async with engine.begin() as conn:
#         print("Creating tables...")
#         await conn.run_sync(Base.metadata.create_all)
#         print("Done creating tables.")

# if __name__ == "__main__":
#     asyncio.run(create_all())

# scripts/create_tables.py
import asyncio
from sqlalchemy import text
from app.db.database import engine
from app.db.base import Base
# import models so they are registered to metadata
import app.models.organization_model as org_m
import app.models.user_model as user_m

async def create():
    async with engine.begin() as conn:
        # create the Postgres enum types explicitly (if not exist)
        # using CREATE TYPE IF NOT EXISTS ... to be safe
        await conn.execute(text(
            "DO $$ BEGIN "
            "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'usertypeenum') THEN "
            "CREATE TYPE usertypeenum AS ENUM ('Agent', 'Employee', 'Admin'); "
            "END IF; "
            "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'statusenum') THEN "
            "CREATE TYPE statusenum AS ENUM ('Active', 'Inactive'); "
            "END IF; "
            "IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'planstatusenum') THEN "
            "CREATE TYPE planstatusenum AS ENUM ('Active', 'Inactive'); "
            "END IF; "
            "END $$;"
        ))
        # create all tables (will use existing types)
        await conn.run_sync(Base.metadata.create_all)
    print("Done creating tables.")

if __name__ == "__main__":
    asyncio.run(create())

