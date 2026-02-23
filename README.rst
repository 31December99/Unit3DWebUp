
**Hi ! 2**
===============================================
|version| |online| |status| |python| |ubuntu| |debian| |windows|

.. |version| image:: https://img.shields.io/pypi/v/unit3dupWeb.svg
.. |online| image:: https://img.shields.io/badge/Online-green
.. |status| image:: https://img.shields.io/badge/Status-Active-brightgreen
.. |python| image:: https://img.shields.io/badge/Python-3.12+-blue
.. |ubuntu| image:: https://img.shields.io/badge/Ubuntu-22+-blue
.. |debian| image:: https://img.shields.io/badge/Debian-12+-blue
.. |windows| image:: https://img.shields.io/badge/Windows-11-blue

Auto Torrent Generator and Uploader
===================================

Reworked from the original Unit3Dup:
https://github.com/31December99/Unit3Dup

now including an async backend and a web frontend

.. image:: images/home.png
   :alt: Uni3D webUp home
   :width: 600
   :align: center

|

.. image:: images/settings1.png
   :alt: Uni3D webUp home
   :width: 600
   :align: center

|

.. image:: images/settings2.png
   :alt: Uni3D webUp home
   :width: 600
   :align: center

|

.. image:: images/settings3.png
   :alt: Uni3D webUp home
   :width: 600
   :align: center

|

.. image:: images/jobs.png
   :alt: Uni3D webUp home
   :width: 600
   :align: center


|

It performs the following tasks:

- Scan folder and subfolders
- Compiles various metadata information to create a torrent
- Extracts a series of screenshots directly from the video
- Add webp to your torrent description page
- Searches for the corresponding ID on TMDB, IGDB, IMDB,TVDB
- Add trailer from TMDB or YouTube
- Seeding in qBittorrent
- Generates meta-info derived from the video
- Create and upload individual torrents or the page


*NOT YET TESTED*

- Extracts cover from the PDF documents
- Reseeding one or more torrents at a time
- Seed your torrents across different OS
- Add a custom title to your seasons
- Generate info for a title using MediaInfo
- unit3dup can grab the first page, convert it to an image (using xpdf),
  and then the bot can upload it to an image host, then add the link to the torrent page description.

*NOT YET IMPLEMENTED*

- Generates meta-info derived from the game
- Seeding in Transmission or rTorrent


Install
===================

run
docker-compose pull

