# -*- coding: utf-8 -*-

from unit3dwup.external.oauth import oauth2_scheme
from fastapi import Depends, HTTPException

from unit3dwup.routers.dependencies import (
    get_job_repo,
)


# Create a function to get user data and verify the token
def get_current_user(token: str = Depends(oauth2_scheme),  job_repo=Depends(get_job_repo)) -> str:

    #TODO Search for user using receved token
    print("#############################################################################################")
    print(f"!{token}!")

    job = job_repo.job.get_job_repo(token)
    print(job)

    # if token is None or token == "":
    #     raise HTTPException(status_code=401, detail="Invalid token")

    return token