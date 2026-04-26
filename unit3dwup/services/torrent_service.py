# -*- coding: utf-8 -*-
import asyncio
from threading import Thread
from multiprocessing import Manager

from unit3dwup.services.create_torrent_service import MyTorrentService
from unit3dwup.models.media import Media

from fastapi import FastAPI


class TorrentService:
    """
        Accept a list of Media objects and create torrents in batch mode
        TODO For the moment n° workers and batch_size are hardcoded
    """

    def __init__(self, app: FastAPI):
        """
        :param app: FastApi
        """

        # Process media
        self.media_list: list[Media] | None = None

        # FastApi instance app
        self.app = app

        # Torrent creation
        self.torr_service = MyTorrentService(app=app)

        # Use the queue to get the progress % during the torrent creation process
        self.manager = Manager()
        self.progress_queue = self.manager.Queue()
        self.result_queue = self.manager.Queue()

    def run_batch(self):
        """
             Try to process group of files to avoid ssd saturation
        :return:
        """

        # TODO: ha senso spingere con i workers se il mio ssd lavoro già al 100%?
        try:
            results = self.torr_service.start(self.media_list, batch_size=16, workers=4,
                                              progress_queue=self.progress_queue)
            self.result_queue.put(results)
        except Exception as e:
            print(e)

    async def start(self, media_list: list[Media]):
        """
            Start the torrent service
        :return:
        """
        self.media_list = media_list

        # Run run_batch() in background
        thread = Thread(target=self.run_batch)
        thread.start()

        # Keep looping while the thread is running or the queue is not empty
        all_progress = {}
        while thread.is_alive() or not self.progress_queue.empty():
            while not self.progress_queue.empty():
                # The worker fill the queue, here we consume it and forward the progress to the client
                update = self.progress_queue.get()

                # For each torrent send the current progress...
                all_progress[update['torrent']] = update['progress']
                await self.app.state.ws_manager.broadcast({
                    "type": "progress",
                    "level": "progress",
                    "job_id": update['job_id'],
                    "process": "Torrent",
                    "progress": update['progress'],
                    "message": f"[New torrent] {update['torrent']} - {round(update['progress'], 2)}",
                })

                print("log", "progress", update['job_id'], update['progress'],
                      f"[New torrent] {update['torrent']} - {round(update['progress'], 2)}")

            await asyncio.sleep(0.1)

        thread.join()
        results = self.result_queue.get()

        # Invio log finali
        for torrent in results:
            if torrent.get('status') == '200':
                await self.app.state.ws_manager.broadcast({
                    "type": "progress",
                    "level": "progress",
                    "job_id": torrent['job_id'],
                    "process": "Completed",
                    "progress": 100.0,
                    "message": f"[New torrent] {torrent['message'].name} from {torrent['message'].parent}"
                })

            if torrent.get('status') == '409':
                await self.app.state.ws_manager.broadcast({
                    "type": "progress",
                    "level": "progress",
                    "job_id": torrent['job_id'],
                    "process": "Error",
                    "progress": 100.0,
                    "message": f"[Reloaded] {torrent['message'].name} from {torrent['message'].parent}"
                })
