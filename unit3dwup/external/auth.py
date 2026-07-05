# -*- coding: utf-8 -*-

from unit3dwup.external.oauth import oauth2_scheme
from fastapi import Depends, HTTPException


# Create a function to get user data and verify the token
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:

    #TODO Search for user using receved token
    if token is None or token == "":
        raise HTTPException(status_code=401, detail="Invalid token")

    # esempio fake validation
    return token