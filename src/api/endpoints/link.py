from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.core.user import current_user, current_superuser, anonymous
from src.crud.link import create_link, get_full_link
from src.schemas.link import LinkCreate, LinkDB
from src.schemas.user import UserDB

router = APIRouter()


@router.post('/',
             response_model=LinkDB,
             response_model_exclude_none=True,
             response_model_exclude={
                 'user_id',
                 'is_hidden',
                 'is_private',
             }, )
async def create_new_link(
        link: LinkCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
):
    new_link = await create_link(link, session, user)
    return new_link


@router.get('/{short_link}',
            response_class=RedirectResponse)
async def get_link_by_short_link(
        short_link: str,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
):
    link = await get_full_link(short_link, session, user)
    return RedirectResponse(
        url=link.original_link,
        status_code=HTTPStatus.TEMPORARY_REDIRECT
    )
