import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/services/services.dart';

class PosterProvider extends ChangeNotifier {
  PosterProvider();

  /// PosterItem list received from api endpoints
  List<PosterItem> posterItems = [];

  /// Il nuovo poster che deve sostituire il vecchio nella lista PosterItem
  // PosterItem newPosterItems = PosterItem();

  /// Use different name for PosterItem list for poster Popup
  List<PosterItem> posterPopUpItems = [];

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
  Future<String?> scan(String remotePath, String query) async {
    posterItems = await ApiService.scan(remotePath);

    /// Check for possible errors
    /// When there is only one item and the error attribute is not null
    if (posterItems.isNotEmpty) {
      if (posterItems[0].error != null) {
        return posterItems[0].error;
      }
    }

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
    return null;
  }

  /// Create torrents
  Future<String?> makeTorrent(String jobId, String? jobListId) async {
    final String? response = await ApiService.fetchTorrent(jobId, jobListId);
    if (response != null) return response;

    isLoading = false;
    notifyListeners();
    return null;
  }

  /// Request to start processing the entire job list (page)
  Future<String?> uploadList(String jobIdList) async {
    await ApiService.processList(jobIdList);
    isLoading = false;
    notifyListeners();
    return null;
  }

  /// Upload torrents
  Future<void> uploadTorrent(String jobId) async {
    posterPopUpItems = await ApiService.uploadTorrent(jobId);
    isLoading = false;
    notifyListeners();
  }

  /// Seed torrents
  Future<void> seedTorrent(String jobId) async {
    posterPopUpItems = await ApiService.seedTorrent(jobId);
    isLoading = false;
    notifyListeners();
  }

  /// Clicking a poster opens a new window with new functions
  ///
  ///
  /// Send to backend the new TMDB ID
  Future<void> updatePosterId(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();

    posterPopUpItems = await ApiService.fetchPosterId(jobId, fieldId, newId);
    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;
    if (poster != null) {
      poster.tmdbId = newId;
    }
    isLoading = false;
    notifyListeners();
  }

  /// Send to backend the new TVDB ID
  Future<void> updateTvdbId(String jobId, String fieldId, String newId) async {
    isLoading = true;
    notifyListeners();

    posterPopUpItems = await ApiService.fetchTvdbId(jobId, fieldId, newId);
    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;
    if (poster != null) {
      poster.tvdbId = newId;
    }
    isLoading = false;
    notifyListeners();
  }

  /// Send to backend the new IMDB ID
  Future<void> updateImdbId(String jobId, String fieldId, String newId) async {
    isLoading = true;
    notifyListeners();

    posterPopUpItems = await ApiService.fetchImdbId(jobId, fieldId, newId);
    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;
    if (poster != null) {
      poster.imdbId = newId;
    }
    isLoading = false;
    notifyListeners();
  }

  /// Send to backend the new Poster Url ( TMDB backdrop url)
  Future<void> updatePosterUrl(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();
    posterPopUpItems = await ApiService.fetchPosterUrl(jobId, fieldId, newId);

    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;
    if (poster != null) {
      poster.posterUrl = newId;
    }
    isLoading = false;
    notifyListeners();
  }

  /// Send to backend the new displayName
  Future<void> updatePosterDname(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    isLoading = true;
    notifyListeners();
    posterPopUpItems = await ApiService.fetchPosterDname(jobId, fieldId, newId);

    final poster = posterItems.where((p) => p.jobId == jobId).firstOrNull;
    if (poster != null) {
      poster.displayName = newId;
    }
    isLoading = false;
    notifyListeners();
  } /// End poster popup functions


  /// Request backend to search for torrents in the tracker
  Future<void> searchPoster(String title) async {
    isLoading = true;
    notifyListeners();

    posterItems = await ApiService.fetchFilteredItem(title);
    isLoading = false;
    notifyListeners();
  }

  // /// Azzera il poster selezionato
  // Future<void> clearSelectedPoster() async {
  //   selectedPosterUrl = null;
  //   notifyListeners();
  // }

  /// Aggiorna la stringa per NavigationRail 'remote' or 'local'
  /// non utilizzata
  // Future<void> switchSourcePoster() async {
  //   isLocal = !isLocal;
  //   selectedSource = isLocal ? 'Local' : 'Remote';
  //   notifyListeners();
  // }

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
