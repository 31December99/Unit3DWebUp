import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/services/services.dart';

class PosterProvider extends ChangeNotifier {
  PosterProvider();

  /// PosterItem list received from api endpoints
  List<PosterItem> posterItems = [];

  /// PosterItem list received from api endpoints
  PosterItem posterItem = PosterItem();

  /// Use different name for PosterItem list for poster Popup
  List<PosterItem> posterPopUpItems = [];

  /// PosterPopUpItem list received from api endpoints
  PosterItem posterPopUpItem = PosterItem();

  /// URL corrente del poster selezionato
  String? selectedPosterUrl;

  /// Assume il valore in string della selezione source in locale o remoto
  // String selectedSource = 'Local';

  /// Switch icon from normal to loading
  bool isLoading = false;

  /// Tramite widget switch seleziona un source in locale o in remoto
  // bool isLocal = false;

  /// ENDPOINTS
  ///
  /// Request to scan the user path
  /// TODO same as -scan flag in unit3dup
  /// TODO Add creation torrent for -f and -u flag
  Future<void> scan(String query) async {
    posterItems = await ApiService.scan();

    isLoading = true;
    notifyListeners();

    /// Filter results based on the query string
    final filteredList = posterItems
        .where(
          (c) =>
              c.displayName?.toLowerCase().contains(query.toLowerCase()) ??
              false,
        )
        .toList();
    posterItems = filteredList;
    isLoading = false;
    notifyListeners();
    posterItem.snackBarStatus = "JobId not found";
  }

  /// Create torrents
  Future<PosterItem> makeTorrent(String jobId, String? jobListId) async {
    posterItem = await ApiService.fetchTorrent(jobId, jobListId);
    return posterItem;
  }

  /// Request to start processing the entire job list (page)
  Future<PosterItem> uploadList(String jobIdList) async {
    return await ApiService.processList(jobIdList);
  }

  /// Seed torrents
  Future<PosterItem> seedTorrent(String jobId) async {
    posterPopUpItem = await ApiService.seedTorrent(jobId);
    return posterPopUpItem;
  }

  /// Upload torrents
  Future<PosterItem> uploadTorrent(String jobId) async {
    posterPopUpItem = await ApiService.uploadTorrent(jobId);
    return posterPopUpItem;
  }

  /// Clicking a poster opens a new window with new functions
  ///
  ///
  /// Send to backend the new TMDB ID
  Future<PosterItem> updatePosterId(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();

    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;

    if (poster != null) {
      poster.tmdbId = newId;
      await ApiService.fetchPosterId(jobId, fieldId, newId, poster);
      isLoading = false;
      notifyListeners();
      return poster;
    }
    return posterItem;
  } // fetchTvdbId

  /// Send to backend the new TVDB ID
  Future<PosterItem> updateTvdbId(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();

    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;

    if (poster != null) {
      poster.tmdbId = newId;
      await ApiService.fetchTvdbId(jobId, fieldId, newId, poster);
      isLoading = false;
      notifyListeners();
      return poster;
    }
    return posterItem;
  }

  /// Send to backend the new IMDB ID
  Future<PosterItem> updateImdbId(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();

    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;

    if (poster != null) {
      poster.imdbId = newId;
      await ApiService.fetchImdbId(jobId, fieldId, newId, poster);
      isLoading = false;
      notifyListeners();
      return poster;
    }
    posterItem.snackBarStatus = "JobId not found";
    return posterItem;
  }

  /// Send to backend the new Poster Url ( TMDB backdrop url)
  Future<PosterItem> updatePosterUrl(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();

    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;

    if (poster != null) {
      poster.posterUrl = newId;
      await ApiService.fetchPosterUrl(jobId, fieldId, newId, poster);
      isLoading = false;
      notifyListeners();
      return poster;
    }
    posterItem.snackBarStatus = "JobId not found";
    return posterItem;
  }

  /// Send to backend the new displayName
  Future<String?> updatePosterDname(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();

    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;

    if (poster != null) {
      poster.displayName = newId;
      await ApiService.fetchPosterDname(jobId, fieldId, newId, poster);
      isLoading = false;
      notifyListeners();
      return poster.snackBarStatus;
    }
    return posterItem.snackBarStatus = "JobId not found";
  }

  /// Request backend to search for torrents in the tracker
  Future<void> searchPoster(String title) async {
    isLoading = true;
    notifyListeners();
    posterItems = await ApiService.fetchFilteredItem(title);
    isLoading = false;
    notifyListeners();
  }

  /// Request backend to delete the job list
  /// The SearchPage will be cleared
  /// user paths need to be rescanned
  Future<void> clearPosterItems() async {
    if (posterItems.isNotEmpty) {
      await ApiService.clearJobListId(posterItems[0].jobListId);
    }

    posterItems = [];
    notifyListeners();
  }

  /// Update the poster status in percentage progress
  /// The status bar at bottom of the image
  Future<void> updatePosterProgress(
    double progress,
    String jobId,
    String process,
  ) async {
    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;
    if (poster != null) {
      if (process == 'uploaded' && progress == 200) {
        poster.process = process;
      }

      if (process == 'error' && progress == 409) {
        poster.process = process;
      }

      if (process != 'completed') {
        poster.process = "$process ${progress.toStringAsFixed(2)}%";
      } else {
        poster.process = process;
      }
    }

    isLoading = false;
    notifyListeners();
  }

  /// Update the poster status
  /// The status bar at bottom of the image
  Future<void> updatePosterLogMessage(String message, String jobId) async {
    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;
    if (poster != null) {
      poster.process = message;
    }

    isLoading = false;
    notifyListeners();
  }
}
