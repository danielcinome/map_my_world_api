import asyncio
import time

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.user import routers as user_routers
from app.api.login import routers as login_routers
from app.api.location import routers as location_routers
from app.api.category import routers as category_routers
from app.api.recommendation import routers as recommendation_routers


app = FastAPI(title='Map My World API')


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):

    # Time in seconds
    REQUEST_TIMEOUT_ERROR = 30

    try:
        start_time = time.time()
        return await asyncio.wait_for(call_next(request), timeout=REQUEST_TIMEOUT_ERROR)

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse({'detail': 'Request processing time excedeed limit',
                             'processing_time': process_time},
                            status_code=status.HTTP_504_GATEWAY_TIMEOUT)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    login_routers.router,
    prefix='/login',
    tags=['Login'],
)
app.include_router(
    user_routers.router,
    prefix='/user',
    tags=['User']
)
app.include_router(
    location_routers.router,
    prefix='/location',
    tags=['Location']
)
app.include_router(
    category_routers.router,
    prefix='/category',
    tags=['Category']
)
app.include_router(
    recommendation_routers.router,
    prefix='/recommendations',
    tags=['Recommendation']
)
