# -*- coding: utf-8 -*-

from config.settings import Load

config_settings = Load().load_config()

# Same as the old 0.8.21. Set the priority based on the config file
# TODO : host rotation on failure is not implemented yet
master_uploaders = ['ImgBB', 'PtScreens', 'LensDump', 'ImgFi', 'PassIMA', 'ImaRide', 'Freeimage']

upload_hosts = {
    "ImgBB": {
        "url": "https://api.imgbb.com/1/upload",
        "data": {"key": config_settings.tracker_config.IMGBB_KEY, "fieldname": "name"},
        "fieldname": "image"
    },
    "Freeimage": {
        "url": "https://freeimage.host/api/1/upload",
        "data": {"key": config_settings.tracker_config.FREE_IMAGE_KEY, "fieldname": "name"},
        "fieldname": "image"
    },
    "PtScreens": {
        "url": "https://ptscreens.com/api/1/upload",
        "data": {"key": config_settings.tracker_config.PTSCREENS_KEY, "fieldname": "title"},
        "fieldname": "source"
    },
    "LensDump": {
        "url": "https://lensdump.com/api/1/upload",
        "data": {"key": config_settings.tracker_config.LENSDUMP_KEY, "fieldname": "title"},
        "fieldname": "source"
    },
    "ImgFi": {
        "url": "https://imgfi.com/api/1/upload",
        "data": {"key": config_settings.tracker_config.IMGFI_KEY, "fieldname": "title"},
        "fieldname": "source"
    },
    "PassIMA": {
        "url": "https://passtheima.ge/api/1/upload",
        "data": {"key": config_settings.tracker_config.PASSIMA_KEY, "title": "name"},
        "fieldname": "source"
    },
    "ImaRide": {
        "url": "https://www.imageride.net/api/1/upload",
        "data": {"key": config_settings.tracker_config.IMARIDE_KEY, "fieldname": "title"},
        "fieldname": "source"
    }
}

priority_map = {
    'ImgBB': config_settings.user_preferences.IMGBB_PRIORITY,
    'PtScreens': config_settings.user_preferences.PTSCREENS_PRIORITY,
    'LensDump': config_settings.user_preferences.LENSDUMP_PRIORITY,
    'ImgFi': config_settings.user_preferences.IMGFI_PRIORITY,
    'PassIMA': config_settings.user_preferences.PASSIMA_PRIORITY,
    'ImaRide': config_settings.user_preferences.IMARIDE_PRIORITY,
    'Freeimage': config_settings.user_preferences.FREE_IMAGE_PRIORITY,
}
