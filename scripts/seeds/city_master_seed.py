# scripts/seeds/city_master_seed.py

import json
import asyncio
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.models.city_model import CityMaster


SEED_FILE = Path(__file__).parent / "cities.json"


def generate_city_code(country_code: str, city_name: str) -> str:
    return f"{country_code}-{city_name[:3].upper()}"


async def seed_city_master():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            cities = json.load(f)

        for c in cities:
            city_code = generate_city_code(c["country_code"], c["name"])

            result = await session.execute(
                select(CityMaster).where(
                    CityMaster.country_code == c["country_code"],
                    CityMaster.name == c["name"],
                )
            )
            exists = result.scalar_one_or_none()

            if exists:
                print(f"✓ City {c['name']} already exists")
                continue

            city = CityMaster(
                country_code=c["country_code"],
                city_code=city_code,
                name=c["name"],
                is_active=True,
            )
            session.add(city)
            print(f"+ Added city {c['name']} ({city_code})")

        await session.commit()
        print("✅ City master seeding completed")


if __name__ == "__main__":
    asyncio.run(seed_city_master())