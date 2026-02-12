# -*- coding: utf-8 -*-

from config.settings import get_settings

settings = get_settings()

# Same as the old 0.8.21. Set the priority based on the config file
# TODO : host rotation on failure is not implemented yet
master_uploaders = ['ImgBB', 'PtScreens', 'LensDump', 'ImgFi', 'PassIMA', 'ImaRide', 'Freeimage']

upload_hosts = {
    "ImgBB": {
        "url": "https://api.imgbb.com/1/upload",
        "data": {"key": settings.tracker.IMGBB_KEY, "fieldname": "name"},
        "fieldname": "image"
    },
    "Freeimage": {
        "url": "https://freeimage.host/api/1/upload",
        "data": {"key": settings.tracker.FREE_IMAGE_KEY, "fieldname": "name"},
        "fieldname": "image"
    },
    "PtScreens": {
        "url": "https://ptscreens.com/api/1/upload",
        "data": {"key": settings.tracker.PTSCREENS_KEY, "fieldname": "title"},
        "fieldname": "source"
    },
    "LensDump": {
        "url": "https://lensdump.com/api/1/upload",
        "data": {"key": settings.tracker.LENSDUMP_KEY, "fieldname": "title"},
        "fieldname": "source"
    },
    "ImgFi": {
        "url": "https://imgfi.com/api/1/upload",
        "data": {"key": settings.tracker.IMGFI_KEY, "fieldname": "title"},
        "fieldname": "source"
    },
    "PassIMA": {
        "url": "https://passtheima.ge/api/1/upload",
        "data": {"key": settings.tracker.PASSIMA_KEY, "title": "name"},
        "fieldname": "source"
    },
    "ImaRide": {
        "url": "https://www.imageride.net/api/1/upload",
        "data": {"key": settings.tracker.IMARIDE_KEY, "fieldname": "title"},
        "fieldname": "source"
    }
}

priority_map = {
    'ImgBB': settings.prefs.IMGBB_PRIORITY,
    'PtScreens': settings.prefs.PTSCREENS_PRIORITY,
    'LensDump': settings.prefs.LENSDUMP_PRIORITY,
    'ImgFi': settings.prefs.IMGFI_PRIORITY,
    'PassIMA': settings.prefs.PASSIMA_PRIORITY,
    'ImaRide': settings.prefs.IMARIDE_PRIORITY,
    'Freeimage': settings.prefs.FREE_IMAGE_PRIORITY,
}
