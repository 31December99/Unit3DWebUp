
/// Instance of a Setting object for the Settings page
class SettingItem {
  final Map<String, dynamic>? userPreferences;

  SettingItem({this.userPreferences});

  // Factory object from json
  factory SettingItem.fromJson(Map<String, dynamic> jsonData) {
    final data = jsonData['userPreferences'] as Map<String, dynamic>;
    if (data.isEmpty) return SettingItem();

    return SettingItem(userPreferences: data);
  }
}
