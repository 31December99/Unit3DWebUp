import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/services/services.dart';

class SettingProvider extends ChangeNotifier {
  /// Holds current setting values
  SettingItem? currentSetting;

  /// Default scan path #1
  /// TODO for the moment hardcoded
  String selectedScanpath01 = "/home/parzival/ts";

  /// Default scan path #2
  /// not used
  String selectedScanpath02 = 'no_path';

  /// Default scan path #3
  /// not used
  String selectedScanpath03 = 'no_path';

  /// Priority list for image hosts (0 = highest)
  List<String> priorityHostOption = ['0', '1', '2', '3', '4', '5', '6'];

  /// Default YouTube favorite channel ID
  /// like the old unit3dup
  String selectedYouTubeFavChannelId = 'UCGCbxpnt25hWPFLSbvwfg_w';

  /// Default duplicate size threshold
  String selectedSizeTh = '100';

  /// Default watcher interval (folder check time)
  String selectedWatcherInterval = '7';

  /// Default watcher source folder
  String selectedWatcherPath = 'no_path';

  /// Default watcher destination folder
  String selectedWatcherDestinationPath = 'no_path';

  /// Default torrent archive path
  String selectedTorrentArchivePath = 'no_path';

  /// Default cache folder path
  String selectedCachePath = 'no_path';

  /// Default torrent comment
  String selectedTorrentComment = 'no_comment';

  /// Default priority: Passima
  String selectedPriorityPassima = '0';

  /// Default priority: PTScreens
  String selectedPriorityPtScreens = '0';

  /// Default priority: LensDump
  String selectedPriorityLensDump = '0';

  /// Default priority: FreeImage
  String selectedPriorityFreeImage = '0';

  /// Default priority: IMGBB
  String selectedPriorityImgBB = '0';

  /// Default priority: ImgFi
  String selectedPriorityImgfi = '0';

  /// Default priority: Imaride
  String selectedPriorityImaride = '0';

  /// Default number of screenshots
  String selectedScrShot = '4';

  /// Screenshot compression level
  String selectedNumCompressShot = '4';

  /// Enable YouTube trailer
  bool youtubeChannelEnable = false;

  /// Enable duplicate search
  bool duplicateOn = false;

  /// Enable skip duplicates
  bool skipDuplicate = false;

  /// Enable skip TMDB
  bool skipTmdb = false;

  /// Enable screenshot resize
  bool resizeScshot = false;

  /// Enable anonymous uploader
  bool anon = false;

  /// Enable screenshot cache
  bool cacheScshot = false;

  /// Enable TMDB cache
  bool cacheDbonline = false;

  /// Enable personal release torrent
  bool personalRel = false;

  /// Enable WEBP screenshots
  bool webp = false;

  /// Set scan path #1
  void pathScan01(String value) {
    selectedScanpath01 = value;
    notifyListeners();
  }

  /// Set scan path #2
  /// not used
  void pathScan02(String value) {
    selectedScanpath02 = value;
    notifyListeners();
  }

  /// Set scan path #3
  /// not used
  void pathScan03(String value) {
    selectedScanpath03 = value;
    notifyListeners();
  }

  /// Set YouTube channel ID
  void youTubeFavChannelId(String value) {
    selectedYouTubeFavChannelId = value;
    notifyListeners();
  }

  /// Set duplicate size threshold
  void sizeTh(String value) {
    selectedSizeTh = value;
    notifyListeners();
  }

  /// Set watcher interval
  void watcherInterval(String value) {
    selectedWatcherInterval = value;
    notifyListeners();
  }

  /// Set watcher source path
  void watcherPath(String value) {
    selectedWatcherPath = value;
    notifyListeners();
  }

  /// Set watcher destination path
  void watcherDestinationPath(String value) {
    selectedWatcherDestinationPath = value;
    notifyListeners();
  }

  /// Set torrent archive path
  void torrentArchivePath(String value) {
    selectedTorrentArchivePath = value;
    notifyListeners();
  }

  /// Set cache path
  void cachePath(String value) {
    selectedCachePath = value;
    notifyListeners();
  }

  /// Set torrent comment
  void torrentComment(String value) {
    selectedTorrentComment = value;
    notifyListeners();
  }

  /// Set Pass_ima priority
  void Passima(String value) {
    selectedPriorityPassima = value;
    notifyListeners();
  }

  /// Set PTScreens priority
  void PtScreens(String value) {
    selectedPriorityPtScreens = value;
    notifyListeners();
  }

  /// Set LensDump priority
  void lensDump(String value) {
    selectedPriorityLensDump = value;
    notifyListeners();
  }

  /// Set FreeImage priority
  void freeImage(String value) {
    selectedPriorityFreeImage = value;
    notifyListeners();
  }

  /// Set IMGBB priority
  void imgBB(String value) {
    selectedPriorityImgBB = value;
    notifyListeners();
  }

  /// Set ImgFi priority
  void imgFi(String value) {
    selectedPriorityImgfi = value;
    notifyListeners();
  }

  /// Set Imaride priority
  void imaRide(String value) {
    selectedPriorityImaride = value;
    notifyListeners();
  }

  /// Set number of screenshots
  void numScsShot(String value) {
    selectedScrShot = value;
    notifyListeners();
  }

  /// Set screenshot compression level
  void numCompressScsShot(String value) {
    selectedNumCompressShot = value;
    notifyListeners();
  }

  /// Toggle YouTube trailer
  void youtube() {
    youtubeChannelEnable = !youtubeChannelEnable;
    notifyListeners();
  }

  /// Toggle duplicate search
  void duplicate() {
    duplicateOn = !duplicateOn;
    notifyListeners();
  }

  /// Toggle skip duplicates
  void dpSkip() {
    skipDuplicate = !skipDuplicate;
    notifyListeners();
  }

  /// Toggle skip TMDB
  void tmdbSkip() {
    skipTmdb = !skipTmdb;
    notifyListeners();
  }

  /// Toggle screenshot resize
  void rszScshot() {
    resizeScshot = !resizeScshot;
    notifyListeners();
  }

  /// Toggle anonymous uploader
  void anonUser() {
    anon = !anon;
    notifyListeners();
  }

  /// Toggle screenshot cache
  void cacheScreenshot() {
    cacheScshot = !cacheScshot;
    notifyListeners();
  }

  /// Toggle TMDB cache
  void cacheTmdb() {
    cacheDbonline = !cacheDbonline;
    notifyListeners();
  }

  /// Toggle personal release
  void personalRelease() {
    personalRel = !personalRel;
    notifyListeners();
  }

  /// Toggle WEBP screenshots
  void webpScshot() {
    webp = !webp;
    notifyListeners();
  }

  /// Load settings from backend
  Future<void> readSetting() async {
    currentSetting = await ApiService.fetchSettingFromBackend('all');
    notifyListeners();
  }
}
