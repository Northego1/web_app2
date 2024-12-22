from contextlib import asynccontextmanager
from typing import AsyncIterator
from redis.asyncio import Redis

from fastapi import Depends, FastAPI, Request
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
from fastapi_cache.coder import PickleCoder



@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # redis = Redis.from_url(settings.redis_DSN)
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache", coder=PickleCoder)
    yield 

    # await redis.close()

    

app = FastAPI(
    title='Travelia',
    lifespan=lifespan
)

# templates = Jinja2Templates(directory='templates')
# app.mount('/static', StaticFiles(directory='static'), name='static')



# fastapi_users = FastAPIUsers[User, int](
#     get_user_manager,
#     [auth_backend],
# )

# current_user = fastapi_users.current_user()

# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )

# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )

# app.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )


# @app.get('/')
# async def index(request: Request, user: User = Depends(optional_current_user)):
#     Routes = 'Routes' if user else None
#     auth = 'logout' if user else 'login'
    

#     data = {
#         'request': request,
#         'Routes': Routes,
#         'routes_link': Url.routes,
#         'auth': auth,
#         'url_logout': Url.auth_logout,
#         'url_login': Url.login
#     }
#     return templates.TemplateResponse('index.html', data)


# app.include_router(router=router_page_map)
# app.include_router(router=router_map)
# app.include_router(router=router_page_auth)
# app.include_router(router=about_the_router)