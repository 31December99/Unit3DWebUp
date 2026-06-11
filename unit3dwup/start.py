# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from unit3dwup.lifespan import lifespan

from unit3dwup.routers import scan, process, jobs, posters, settings, search, ws


# Initialize FastApi
app = FastAPI(lifespan=lifespan)

# TODO middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:PORT"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the routers (endpoints moved out of this file, behaviour unchanged)
app.include_router(scan.router)
app.include_router(process.router)
app.include_router(jobs.router)
app.include_router(posters.router)
app.include_router(settings.router)
app.include_router(search.router)
app.include_router(ws.router)


def main():
    print("Run -> uvicorn unit3dwup.start:app")


if __name__ == "__main__":
    main()
