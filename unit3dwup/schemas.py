# -*- coding: utf-8 -*-
from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    path: str = Field(..., description="Filesystem path to scan")


class ProcessAllRequest(BaseModel):
    job_list_id: str = Field(..., description="ID of the job list")


class JobRequest(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")


class UpdatePosterRequest(BaseModel):
    job_id: str
    field_id: str
    new_id: str


class ClearJobListRequest(BaseModel):
    job_list_id: str


class SetEnvRequest(BaseModel):
    key: str
    value: str


class FilterRequest(BaseModel):
    title: str
