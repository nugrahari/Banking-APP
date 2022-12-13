
import fastapi as fa
from fastapi.encoders import jsonable_encoder

from libs import db
from . import schemas as auth_schemas, services as auth_services, libs


app = fa.FastAPI(
    title='Asklora Bank Versi 0.0.0 - Auth'
)


@app.post('/login')
async def post_login(form_data: auth_schemas.LogIn):

    with db.session() as db_:
        auth_service = auth_services.AuthService(db_)
        data, _ = auth_service.login(form_data)
        token = await libs.jwt_encode(jsonable_encoder(data))
        response = auth_schemas.RegisterLoginDataOut(
            token=token
        )

    return response
