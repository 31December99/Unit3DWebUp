# -*- coding: utf-8 -*-
import os
from multiprocessing import Pool, cpu_count, Manager
from pathlib import Path

from services.interfaces import TorrentServiceInterface
from config.api_data import trackers_api_data
from config.constants import MediaStatus
from config.settings import get_settings
from models.media import Media

from fastapi import FastAPI
import torf

settings = get_settings()


def worker(args) -> dict:
    torrent_path, torrent_name, torrent_archive, trackers_list, progress_queue, job_id = args
    archive = torrent_archive or '.'
    os.makedirs(archive, exist_ok=True)
    torrent_filepath: Path = (Path(archive) / trackers_list[0] / f"{torrent_name}.torrent")

    announces = [
        trackers_api_data[t.upper()]['announce']
        for t in (trackers_list or []) if t.upper() in trackers_api_data
    ]

    mytorr = torf.Torrent(path=torrent_path, trackers=announces)
    mytorr.comment = settings.prefs.TORRENT_COMMENT
    mytorr.name = torrent_name
    mytorr.created_by = ""
    mytorr.private = True
    mytorr.source = trackers_list[0] if trackers_list else None
    mytorr.segments = 16 * 1024 * 1024

    # The callback
    def callback_progress(torrent, filepath, pieces_done, pieces_total):
        progress = pieces_done / pieces_total * 100
        progress_queue.put({'torrent': torrent_name, 'progress': progress, 'job_id': job_id})

    mytorr.generate(callback=callback_progress, interval=1)
    mytorr.write(torrent_filepath)
    return {'status': '200', 'message': torrent_filepath, 'job_id': job_id}


class MyTorrentService(TorrentServiceInterface):
    def __init__(self, app: FastAPI):
        self.app = app

    def start(self, media_list: list[Media], batch_size=16, workers: int = 4, progress_queue=None):
        """
        :param media_list: list of Media objects to process
        :param batch_size: numer of item per batch
        :param workers: number of workers
        :param progress_queue: a safe queue where put the progress
        :return:
        """
        results = []
        # Sort by Size ( start with the smallest)
        media_list.sort(key=lambda m: m.size)

        # Create one or more batch list and call the function
        for i in range(0, len(media_list), batch_size):
            batch = media_list[i:i + batch_size]
            batch_results = self._create_batch(batch, trackers=['ITT'], workers=workers, progress_queue=progress_queue)
            results.extend(batch_results)
        return results

    def _create_batch(self, media_list: list[Media], trackers: list[str] = None, workers: int = None,
                      progress_queue=None):

        with Manager() as manager:
            if progress_queue is None:
                progress_queue = manager.Queue()

            # Create a list of task only for Media with description and video status positive
            archive_path = self.app.state.torrent_archive_path or '.'
            jobs = [
                (m.torrent_path, m.torrent_name, archive_path, trackers, progress_queue, m.job_id)
                for m in media_list if m.status not in (MediaStatus.DESCRIPTION_ERROR, MediaStatus.VIDEO_ERROR)
            ]

            # Go
            workers = workers or cpu_count()
            with Pool(workers) as pool:
                results = pool.map(worker, jobs)

            # Wait for the end
            while not progress_queue.empty():
                progress_update = progress_queue.get()
                print(f"Torrent {progress_update['torrent']}: {progress_update['progress']:.2f}%")

        return results
