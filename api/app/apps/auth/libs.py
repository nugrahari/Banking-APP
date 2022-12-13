import jwt
from uuid import UUID
from copy import deepcopy
from datetime import datetime

from typing import Optional
from typing import Any, Dict
from pydantic import BaseModel

import fastapi as fa
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from settings import settings
from apps.users import models as users_models


async def jwt_encode(data: Dict[str, Any]) -> str:
    data_copy = deepcopy(data)
    data_copy.update({
        'iss': settings.JWT.ISSUER,
        'iat': datetime.utcnow(),
    })
    return jwt.encode(data_copy, settings.JWT.SECRET)


def jwt_decode(token) -> Dict[str, Any]:
    return jwt.decode(token, settings.JWT.SECRET, ["HS256"])


class JWTBearer(HTTPBearer):
    pass


security = JWTBearer()


class UserJWT(BaseModel):
    id: UUID
    role: Optional[users_models.RoleEnum]


class AuthUser:
    def __init__(self, token: HTTPAuthorizationCredentials = fa.Depends(security)):
        try:
            current_jwt = jwt_decode(token.credentials)
            self.user = UserJWT(**current_jwt.get('user'))
        except jwt.exceptions.DecodeError as err:
            raise fa.HTTPException(status_code=fa.status.HTTP_403_FORBIDDEN,
                                   detail="Invalid authentication credentials") from err


class AuthAdmin(AuthUser):
    def __init__(self, token: HTTPAuthorizationCredentials = fa.Depends(security)):
        super().__init__(token)

        if self.user.role != users_models.RoleEnum.administrator:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_403_FORBIDDEN, detail="You are not administrator")
