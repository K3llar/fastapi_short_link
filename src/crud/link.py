from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.link import Link
from src.schemas.link import LinkCreate
from src.schemas.user import UserDB
from src.services.link import get_unique_short_link, regex_validation
import src.services.constants as cst


async def create_link(
        new_link: LinkCreate,
        session: AsyncSession,
        user: UserDB
) -> Link:
    new_link_data = new_link.dict()
    new_link_data['user_id'] = user.id
    if new_link_data.get('short_link') != '':
        if await check_unique_short_link(
                new_link_data['short_link'],
                session
        ):
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail=cst.NAME_BUSY.format(new_link_data['short_link'])
            )
        if not regex_validation(new_link_data['short_link']):
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail=cst.BAD_NAMING.format(new_link_data['short_link'])
            )
    else:
        short_link = get_unique_short_link()
        new_link_data['short_link'] = short_link
    db_link = Link(**new_link_data)
    session.add(db_link)
    await session.commit()
    await session.refresh(db_link)
    return db_link


async def check_unique_short_link(
        short_link: str,
        session: AsyncSession
):
    link = await session.execute(select(Link).where(
        Link.short_link == short_link
    )
    )
    link = link.scalars().first()
    if link:
        return True
    return False
