/// Data model representing a poster item displayed on the page
class PosterItem {
  /// TMDB poster image URL
  String? posterUrl;

  /// Torrent display name shown on the tracker page
  String? displayName;

  /// TMDB API identifier
  String? tmdbId;

  /// TVDB API identifier
  String? tvdbId;

  /// IMDb identifier from the remote list
  String? imdbId;

  /// Current job or poster status
  String? status;

  /// Current torrent creation progress (percentage)
  String? progress;

  /// Result of a process
  String? process;

  /// Source origin: remote (tracker) or local (backend)
  final String? source;

  /// Hashed user path identifying the job folder or file
  final String? jobId;

  /// Log type received via websocket from the backend
  final String? log;

  /// Hashed user scan path identifying the job list or page
  final String? jobListId;

  /// List of video screenshot urls returned by the host (for example imgBB)
  List<dynamic>? screenshots;

  PosterItem({
    this.posterUrl,
    this.displayName,
    this.source,
    this.tmdbId,
    this.tvdbId,
    this.imdbId,
    this.jobId,
    this.log,
    this.jobListId,
    this.status,
    this.screenshots,
    this.progress,
    this.process,
  });

  @override
  String toString() {
    return 'PosterItem('
        'posterUrl: $posterUrl, '
        'displayName: $displayName, '
        'source: $source, '
        'tmdbId: $tmdbId, '
        'tvdbId: $tvdbId, '
        'imdbId: $imdbId, '
        'jobId: $jobId,'
        'jobListId: $jobListId,'
        'status: $status,'
        'screenshots: $screenshots,'
        ')';
  }
}
