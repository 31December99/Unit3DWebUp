import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/services/services.dart';

class SettingProvider extends ChangeNotifier {
  /// Holds current setting values
  SettingItem? currentSetting;

  /// Default scan path #1
  /// TODO for the moment hardcoded
  String selectedScanpath01 = "/home/parzival/ts";

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

  Map<String, dynamic> envValues = {};

  /// update single env
  Future<void> setEnv(String key, String value) async {
    envValues[key] = value;
    await ApiService.setEnv(key, value);
    notifyListeners();
  }

  /// Load settings from backend
  Future<void> readSetting() async {
    currentSetting = await ApiService.fetchSettingFromBackend('all');
    envValues = currentSetting?.userPreferences ?? {};
    notifyListeners();
  }

  String getValue(String key, [String defaultValue = ""]) {
    final value = envValues[key];
    if (value == null) return defaultValue;
    return value.toString();
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
}
