from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_async_session
from src.core.user import current_user, user_or_anon
from src.crud.link import create_link, get_full_link, hide_link, update_link
from src.schemas.link import LinkCreate, LinkDB, LinkUpdate
from src.schemas.user import UserDB
from src.services.link import increase_counter

router = APIRouter()


@router.post('/',
             response_model=LinkDB,
             response_model_exclude={
                 'user_id',
                 'is_hidden',
                 'is_private',
                 'link_id',
                 'number_of_uses'
             }, )
async def create_new_link(
        link: LinkCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
):
    """Создание новой записи"""
    new_link = await create_link(link, session, user)
    return new_link


@router.get('/{short_link}',
            response_class=RedirectResponse
            )
async def get_full_link_by_short_link(
        short_link: str,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(user_or_anon)
):
    """
    Получение объекта по короткой ссылке и перенаправление по адресу
    для всех видов пользователей
    """
    link = await get_full_link(short_link, session, user)
    await increase_counter(link, session)
    return RedirectResponse(
        url=link.original_link,
        status_code=HTTPStatus.TEMPORARY_REDIRECT
    )


@router.delete('/{short_link}',
               response_model=LinkDB,
               response_model_exclude={
                   'user_id',
                   'link_id'
               })
async def delete_link(
        short_link: str,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
):
    """Скрытие записи с сохранением в БД"""
    link = await get_full_link(short_link, session, user)
    link = await hide_link(link, session)
    return link


@router.get('/{short_link}/status',
            response_model=LinkDB,
            response_model_exclude={
                'user_id',
                'is_hidden',
                'link_id',
            })
async def get_link_status(
        short_link: str,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
):
    """Получение количества использований короткой ссылки"""
    link = await get_full_link(short_link, session, user)
    return link


@router.patch('/{short_link}',
              response_model=LinkDB,
              response_model_exclude={
                  'user_id',
                  'is_hidden',
                  'link_id',
              })
async def change_privacy_status(
        short_link: str,
        obj_in: LinkUpdate,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user)
):
    """
    Изменение видимости ссылки
    Редактирование возможно только для автора ссылки
    """
    link = await get_full_link(short_link, session, user)
    link = await update_link(link, obj_in, session)
    return link
