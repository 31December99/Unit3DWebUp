import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/services/services.dart';

class SettingProvider extends ChangeNotifier {
  /// Holds current setting values
  SettingItem? currentSetting;

  /// Default scan path #1
  /// TODO for the moment hardcoded
  String selectedScanpath01 = "/home/parzival/itt/scan";

  /// Enable duplicate search
  bool duplicateOn = false;

  /// Enable skip duplicates
  bool duplicate = false;

  /// Enable anonymous uploader
  bool anon = false;

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

  /// Toggle duplicate search
  void searchDuplicate() {
    duplicateOn = !duplicateOn;
    notifyListeners();
  }

  /// Toggle skip duplicates
  void skipDuplicate() {
    duplicate = !duplicate;
    notifyListeners();
  }

  /// Toggle anonymous uploader
  void anonUser() {
    anon = !anon;
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
