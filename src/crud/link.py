from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import src.services.constants as cst
from src.models.link import Link
from src.schemas.link import LinkCreate
from src.schemas.user import UserDB
from src.services.link import get_unique_short_link, regex_validation


async def create_link(
        new_link: LinkCreate,
        session: AsyncSession,
        user: UserDB
) -> Link:
    new_link_data = new_link.dict()
    new_link_data['user_id'] = user.id
    if new_link_data.get('short_link') != '':
        if await get_obj_by_short_link(
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


async def get_obj_by_short_link(
        short_link: str,
        session: AsyncSession
):
    link = await session.execute(select(Link).where(
        Link.short_link == short_link
    )
    )
    link = link.scalars().first()
    if link:
        return link


async def get_full_link(
        short_link: str,
        session: AsyncSession,
        user: UserDB
) -> Link:
    full_link = await get_obj_by_short_link(short_link, session)
    if not full_link:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=cst.NOT_FOUND.format(full_link)
        )
    if full_link.user_id != user.id:
        if full_link.is_private is True:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=cst.PRIVATE_URL
            )
    if full_link.is_hidden is True:
        raise HTTPException(
            status_code=HTTPStatus.GONE
        )
    return full_link


async def get_link_obj_by_id(
        link_id: int,
        session: AsyncSession
) -> Optional[Link]:
    db_link = await session.get(Link,
                                link_id)
    return db_link


async def hide_link(
        link_obj: Link,
        session: AsyncSession,
) -> Link:
    link_obj.is_hidden = True
    session.add(link_obj)
    await session.commit()
    await session.refresh(link_obj)
    return link_obj
