from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Link
from src.schemas.user import UserDB


async def get_links_by_user(
        session: AsyncSession,
        user: UserDB
) -> List[Link]:
    all_links = await session.execute(
        select(Link).where(
            Link.user_id == user.id
        ).where(
            Link.is_hidden == False
        )
    )
    all_links = all_links.scalars().all()
    return all_links
