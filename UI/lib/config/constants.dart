// Enumeration to declare poster status ( used in process bar)
enum JobStatus {
  indexed(0, 'INDEXED'),

  dbIdentified(1, 'DB_IDENTIFIED'),
  dbNotIdentified(10, 'DB_NOT_IDENTIFIED'),
  dbError(11, 'DB_ERROR'),

  videoReady(2, 'VIDEO_READY'),
  videoError(20, 'VIDEO_ERROR'),

  descriptionReady(3, 'DESCRIPTION_READY'),
  descriptionError(30, 'DESCRIPTION_ERROR'),

  torrentGenerated(4, 'TORRENT_GENERATED'),
  torrentError(40, 'TORRENT_ERROR'),

  trackerUploaded(5, 'TRACKER_UPLOADED'),
  trackerNotUploaded(50, 'TRACKER_NOT_UPLOADED'),

  torrentSeed(7, 'TORRENT_SEED'),
  torrentSeedError(70, 'TORRENT_SEED_ERROR');

  final int code;
  final String label;

  const JobStatus(this.code, this.label);

  /// num -> enum
  static JobStatus? fromCode(int code) {
    for (final status in JobStatus.values) {
      if (status.code == code) return status;
    }
    return null;
  }

  static String msg(String? code) {
    final int codeInt;
    if (code != null) {
      codeInt = int.parse(code);
      return fromCode(codeInt)?.label ?? 'UNKNOWN_STATUS';
    }
    return 'unknow_status';
  }
}
