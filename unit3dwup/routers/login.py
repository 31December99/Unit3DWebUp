# -*- coding: utf-8 -*-

from typing import Annotated
from unit3dwup.external.oauth import oauth2_scheme
from fastapi import APIRouter, Depends
from fastapi.security import  OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login")
async def login(
    user_login_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return {
        "access_token": user_login_data.username,
        "token_type": "bearer",
    }


#TEST
@router.get("/status")
async def status(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    return {
        "token": token,
    }