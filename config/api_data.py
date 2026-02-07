# -*- coding: utf-8 -*-

# Same as the old code 08.21
from config.settings import Load

config_settings = Load.load_config()

# Get data based on tracker name. For example itt e sis
trackers_api_data = {
    'ITT':
        {
            "url": config_settings.tracker_config.ITT_URL,
            "api_key": config_settings.tracker_config.ITT_APIKEY,
            "pass_key": config_settings.tracker_config.ITT_PID,
            "announce": f"{config_settings.tracker_config.ITT_URL}/announce/{config_settings.tracker_config.ITT_PID}",
            "source": "ItaTorrents",
        }
    ,
    'SIS':
        {
            "url": config_settings.tracker_config.SIS_URL,
            "api_key": config_settings.tracker_config.SIS_APIKEY,
            "pass_key": config_settings.tracker_config.SIS_PID,
            "announce": f"{config_settings.tracker_config.SIS_URL}/announce/{config_settings.tracker_config.SIS_PID}",
            "source": "ShareIsland",
        }

}
