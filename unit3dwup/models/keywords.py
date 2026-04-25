# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass(slots=True)
class Keyword:
    """
        Dataclass help to manage data from the TMDB ID
        These keywords must be sent to the tracker
    """

    id: int
    name: str
