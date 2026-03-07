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

  /// Show Current job or poster status on the Poster when the mouse hovers
  String? status;

  /// Current torrent creation progress (percentage)
  String? progress;

  /// Show result of a process on the Poster
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

  /// Show an error message on the page using the snackBar
  String? snackBarError;

  /// Show a status message on the page using the snackBar
  String? snackBarStatus;

  /// The backend runs in the container if dockerStatus is true
  final String? dockerStatus;

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
    this.snackBarError,
    this.snackBarStatus,
    this.dockerStatus,
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
        'progress: $progress,'
        'process: $process,'
        'SnackBarError: $snackBarError,'
        'SnackBarStatus: $snackBarStatus,'
        'DockerStatus: $dockerStatus'
        ')';
  }
}
