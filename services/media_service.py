# -*- coding: utf-8 -*-
from datetime import datetime

from repositories.interfaces import MovieRepositoryInterface
from services.utility import ManageTitles


# based on old code unit3dup 0.8.21
class MediaService:
    def __init__(self, repository: MovieRepositoryInterface):
        self.repo = repository

    async def fetch(self, media):
        async def get_keyword() -> str | None:
            keywords = await self.repo.keywords(movie_id=show.get_id(), category=media.category)
            return " ".join([key.name for key in keywords]) if keywords else None

        async def get_trailer() -> str | None:
            trailers = await self.repo.videos(movie_id=show.get_id(), category=media.category)
            if trailers:
                trailer = next((video.key for video in trailers.results if video.type.lower() == 'trailer'  # .results
                                and video.site.lower() == 'youtube'), None)
                return trailer if trailer else None
            return None

        results = await self.repo.search(query=media.guess_title, category=media.category)
        for show in results:
            if show.get_date() and media.guess_filename.guessit_year:
                if not datetime.strptime(show.get_date(), '%Y-%m-%d').year == media.guess_filename.guessit_year:
                    continue

            # Search for title
            if ManageTitles.fuzzyit(str1=media.guess_title, str2=ManageTitles.clean_text(show.get_title())) > 95:
                media.tmdb_id = show.get_id()
                media.imdb_id_from_tvdb = show.get_imdb()
                media.keyword = await get_keyword()
                media.trailer = await get_trailer()
                media.backdrop_path = show.get_poster_path()
                return True

            if ManageTitles.fuzzyit(str1=media.guess_title, str2=ManageTitles.clean_text(show.get_original())) > 95:
                media.tmdb_id = show.get_id()
                media.imdb_id_from_tvdb = show.get_imdb()
                media.keyword = await get_keyword()
                media.trailer = await get_trailer()
                media.backdrop_path = show.get_poster_path()
                return True

        for show in results:
            # # Search for alternative title
            alternative = await self.repo.alternative(movie_id=show.get_id(), category=media.category)
            if alternative:
                for alt in alternative.titles:
                    if ManageTitles.fuzzyit(str1=media.guess_title, str2=alt.title) > 95:
                        media.tmdb_id = show.get_id()
                        media.keyword = await get_keyword()
                        media.trailer = await get_trailer()
                        media.backdrop_path = show.get_poster_path()
                        return True
        return False


class MediaService2:
    def __init__(self, repository: MovieRepositoryInterface):
        self.repo = repository

    async def fetch(self, media):
        results = await self.repo.search(query=media.guess_title, category=media.category)

        for show in results:
            if show.get_date() and media.guess_filename.guessit_year:
                if not datetime.strptime(show.get_date(), '%Y-%m-%d').year == media.guess_filename.guessit_year:
                    continue

            # Search for title
            if ManageTitles.fuzzyit(str1=media.guess_title, str2=ManageTitles.clean_text(show.get_title())) > 95:
                media.imdb_id_from_tvdb = show.get_imdb()
                media.tvdb_id = show.get_id()
                return True

            if ManageTitles.fuzzyit(str1=media.guess_title, str2=ManageTitles.clean_text(show.get_original())) > 95:
                media.imdb_id_from_tvdb = show.get_imdb()
                media.tvdb_id = show.get_id()
                return True

            # Search for alternative title ( translations field)
            alternative = show.get_translations()
            title_ita = alternative.get('ita', None)
            title_eng = alternative.get('eng', None)

            if title_ita:
                if ManageTitles.fuzzyit(str1=media.guess_title, str2=ManageTitles.clean_text(title_ita)) > 95:
                    media.imdb_id_from_tvdb = show.get_imdb()
                    media.tvdb_id = show.get_id()
                    return True

            # The result is not always in english
            if title_eng:
                if ManageTitles.fuzzyit(str1=media.guess_title, str2=ManageTitles.clean_text(title_eng)) > 95:
                    media.imdb_id_from_tvdb = show.get_imdb()
                    media.tvdb_id = show.get_id()
                    return True

        return False
