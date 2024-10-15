from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import check_user_is_manager_or_superuser
from api.contact_requests_validators import check_contact_request_exist
from api.endpoints.contact_requests import create_contact_request
from core.db import get_async_session
from core.frontend import templates
from crud.contact_requests import contact_requests_crud
from models.contact_requests import ContactRequest
from models.user import User
from services.frontend import redirect_by_httpexeption

router = APIRouter(
    tags=['frontend_contact_requests'],
    prefix='/fr_contact_requests'
)


@router.get(
    '/list/{contact_request_type}',
    response_class=HTMLResponse,
    summary='Список заявок на обратную связь',
)
async def contact_requests_main(
    request: Request,
    contact_request_type: str,
    user: User = Depends(check_user_is_manager_or_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    managers = await contact_requests_crud.get_all(
        user=user,
        session=session,
        for_current_user=not user.is_superuser,
        in_progress=contact_request_type == 'work',
        is_processed=(
            contact_request_type == 'processed' and
            not contact_request_type == 'new'
        )
    )
    managers.sort(
        key=lambda manager: manager.created_at,
    )
    context = {
        'request': request,
        'user': user,
        'contact_requests': managers,
    }
    return templates.TemplateResponse(
        'contact_requests/contact_requests_list.html',
        context
    )


# @router.get(
#     '/add',
#     response_class=HTMLResponse,
#     summary='Страница добавления менеджера',
# )
# async def managers_add(
#     request: Request,
#     user: User = Depends(check_user_is_manager_or_superuser),
#     session: AsyncSession = Depends(get_async_session),
# ):
#     context = {
#         'request': request,
#         'user': user,
#         'update': False,
#         'manager': None
#     }

#     return templates.TemplateResponse(
#         'managers/manager_create_update.html', context
#     )


@router.get(
    '/{contact_request_id}',
    response_class=HTMLResponse,
    summary='Страница информации о заявке',
)
async def contact_request_details(
    request: Request,
    contact_request_id: int,
    user: User = Depends(check_user_is_manager_or_superuser),
    session: AsyncSession = Depends(get_async_session),
):
    # try:
    #     manager = await check_user_exist(user_id=manager_id, session=session)
    # except HTTPException:
    #     ...
    # context = {
    #     'request': request,
    #     'user': user,
    #     'manager': manager,
    #     'update': True,
    # }

    return templates.TemplateResponse(
        'managers/manager_create_update.html', context
    )




# @router.post(
#     '/add',
#     response_class=HTMLResponse,
#     summary='Метод добавления менеджера',
#     dependencies=[Depends(check_user_is_manager_or_superuser)]
# )
# async def start_manager_add(
#     request: Request,
#     email: str = Form(...),
#     name: str = Form(...),
#     password: str = Form(...),
#     telegram_user_id: str  = Form(...),
#     session: AsyncSession = Depends(get_async_session),
# ):
#     manager = await create_manager(
#         new_user=ManagerCreate(
#             name=name,
#             email=email,
#             password=password,
#             telegram_user_id=telegram_user_id
#         ),
#         session=session
#     )
#     await redirect_by_httpexeption(f'{router.prefix}/{manager.id}')


# @router.post(
#     '/{manager_id}',
#     response_class=HTMLResponse,
#     summary='Метод обновления менеджера',
#     dependencies=[Depends(check_user_is_manager_or_superuser)]
# )
# async def start_manager_update(
#     request: Request,
#     manager_id: int,
#     name: Optional[str] = Form(None),
#     telegram_user_id: Optional[str]  = Form(None),
#     session: AsyncSession = Depends(get_async_session),
# ):
#     await update_manager(
#         manager_id=manager_id,
#         manager=ManagerUpdate(
#             name=name,
#             telegram_user_id=telegram_user_id
#         ),
#         session=session
#     )
#     await redirect_by_httpexeption(f'{router.prefix}/{manager_id}/')


# @router.delete(
#     '/{manager_id}',
#     response_class=HTMLResponse,
#     summary='Удалить менеджера',
#     dependencies=[Depends(check_user_is_manager_or_superuser)]
# )
# async def manager_delete(
#     request: Request,
#     manager_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     await delete_manager(
#         user_id=manager_id,
#         session=session
#     )
#     return JSONResponse(
#         content={ 'url': str(request.url_for('managers_main')) }
#     )