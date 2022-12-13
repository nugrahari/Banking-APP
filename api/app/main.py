import time
import fastapi as fa
from fastapi.middleware.cors import CORSMiddleware

import apps
from settings import settings
from libs import schemas,  db

db.Base.metadata.create_all(bind=db.engine)


app = fa.FastAPI(
    title='Asklora Banking APP Versi 0.0.0 Root'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.Middleware.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: fa.Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["Process-Time"] = str(process_time)
    return response


@app.get('/')
async def view_root():
    response = schemas.ResponseMessageDataItemOut(data={})
    return response

app.mount('/v1/auth', apps.auth_app)
app.mount('/v1/user', apps.user_app)
