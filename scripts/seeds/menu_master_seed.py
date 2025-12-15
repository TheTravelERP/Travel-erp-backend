# scripts/seeds/menu_master_seed.py

import json
import asyncio
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.models.menu_model import MenuMaster

SEED_FILE = Path(__file__).parent / "menu_master.json"


async def seed_menu_master():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            menus = json.load(f)

        key_to_id = {}

        async def insert_menu(item, parent_id=None, order=0):
            # Skip pure subheaders
            if item.get("type") == "subheader":
                return

            key = item["id"]

            # Check if exists
            result = await session.execute(
                select(MenuMaster).where(MenuMaster.key == key)
            )
            exists = result.scalar_one_or_none()
            if exists:
                key_to_id[key] = exists.id
                return

            menu = MenuMaster(
                key=key,
                title=item["title"],
                path=item.get("path"),
                icon=item.get("icon"),
                parent_id=parent_id,
                sort_order=order,
                is_active=True,
            )
            session.add(menu)
            await session.flush()  # get ID

            key_to_id[key] = menu.id
            print(f"+ Added menu {key}")

            # Insert children
            for idx, child in enumerate(item.get("children", [])):
                await insert_menu(child, parent_id=menu.id, order=idx)

        for idx, item in enumerate(menus):
            await insert_menu(item, parent_id=None, order=idx)

        await session.commit()
        print("✅ Menu master seeding completed")


if __name__ == "__main__":
    asyncio.run(seed_menu_master())
