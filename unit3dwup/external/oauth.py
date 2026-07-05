# -*- coding: utf-8 -*-
from fastapi.security import (
    OAuth2PasswordBearer,
)


# Define /login as the login endpoint and return the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

