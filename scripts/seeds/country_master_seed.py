# scripts/seeds/country_master_seed.py

import json
import asyncio
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.models.country_model import CountryMaster


SEED_FILE = Path(__file__).parent / "countries.json"


async def seed_country_master():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        with open(SEED_FILE, "r", encoding="utf-8") as f:
            countries = json.load(f)

        for c in countries:
            result = await session.execute(
                select(CountryMaster).where(
                    CountryMaster.iso_code == c["iso_code"]
                )
            )
            exists = result.scalar_one_or_none()

            if exists:
                print(f"✓ Country {c['iso_code']} already exists")
                continue

            country = CountryMaster(
                iso_code=c["iso_code"],
                name=c["name"],
                currency_code=c["currency_code"],
            )
            session.add(country)
            print(f"+ Added country {c['iso_code']}")

        await session.commit()
        print("✅ Country master seeding completed")


if __name__ == "__main__":
    asyncio.run(seed_country_master())
