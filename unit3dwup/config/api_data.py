# -*- coding: utf-8 -*-

# Same as the old code 08.21
from unit3dwup.config.settings import get_settings

settings = get_settings()

# Get data based on tracker name. For example itt e sis
trackers_api_data = {
    'ITT':
        {
            "url": settings.tracker.ITT_URL,
            "api_key": settings.tracker.ITT_APIKEY,
            "pass_key": settings.tracker.ITT_PID,
            "announce": f"{settings.tracker.ITT_URL}/announce/{settings.tracker.ITT_PID}",
            "source": "ItaTorrents",
        }
    ,
    'SIS':
        {
            "url": settings.tracker.SIS_URL,
            "api_key": settings.tracker.SIS_APIKEY,
            "pass_key": settings.tracker.SIS_PID,
            "announce": f"{settings.tracker.SIS_URL}/announce/{settings.tracker.SIS_PID}",
            "source": "ShareIsland",
        }

}
