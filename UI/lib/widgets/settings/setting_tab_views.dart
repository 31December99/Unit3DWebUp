import 'package:UI/widgets/settings/settings.dart';
import 'package:UI/providers/providers.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

/// Custom widget to represent TABS in SettingPage
class SettingTabViews extends StatelessWidget {
  const SettingTabViews({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<SettingProvider>();
    final setting = provider.currentSetting;

    if (setting == null) {
      return const Center(child: Text("Nessuna configurazione caricata"));
    }

    return TabBarView(
      /// I° TAB Paths
      children: [
        SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              SettingText(
                label: "PREFS__WATCHER_INTERVAL",
                value: provider.getValue('WATCHER_INTERVAL'),
              ),

              SettingText(
                label: "PREFS__WATCHER_PATH",
                value: provider.getValue('WATCHER_PATH'),
              ),

              SettingText(
                label: "PREFS__WATCHER_PATH",
                value: provider.getValue('WATCHER_PATH'),
              ),

              SettingText(
                label: "PREFS__WATCHER_DESTINATION_PATH",
                value: provider.getValue('WATCHER_DESTINATION_PATH'),
              ),

              SettingText(
                label: "PREFS__TORRENT_ARCHIVE_PATH",
                value: provider.getValue('TORRENT_ARCHIVE_PATH'),
              ),

              SettingText(
                label: "PREFS__SCAN_PATH",
                value: provider.getValue('SCAN_PATH'),
              ),

              SettingText(
                label: "PREFS__TORRENT_COMMENT",
                value: provider.getValue('TORRENT_COMMENT'),
              ),
            ],
          ),
        ),

        /// II° TAB Preference
        SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              SettingText(
                label: "PREFS__SKIP_YOUTUBE",
                value: provider.getValue('SKIP_YOUTUBE'),
              ),

              SettingText(
                label: "PREFS__DUPLICATE_ON",
                value: provider.getValue('DUPLICATE_ON'),
              ),

              SettingText(
                label: "PREFS__SIZE_TH",
                value: provider.getValue('SIZE_TH'),
              ),

              SettingText(
                label: "PREFS__SKIP_DUPLICATE",
                value: provider.getValue('SKIP_DUPLICATE'),
              ),

              SettingText(
                label: "PREFS__ANON",
                value: provider.getValue('ANON'),
              ),

              SettingText(
                label: "PREFS__PERSONAL_RELEASE",
                value: provider.getValue('PERSONAL_RELEASE'),
              ),

              SettingText(
                label: "PREFS__WEBP_ENABLED",
                value: provider.getValue('WEBP_ENABLED'),
              ),
            ],
          ),
        ),

        /// III° TAB Options
        SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              SettingText(
                label: "PREFS__NUMBER_OF_SCREENSHOTS",
                value: provider.getValue('NUMBER_OF_SCREENSHOTS'),
              ),

              SettingText(
                label: "PREFS__COMPRESS_SCSHOT",
                value: provider.getValue('COMPRESS_SCSHOT'),
              ),

              SettingText(
                label: "PREFS__PASSIMA_PRIORITY",
                value: provider.getValue('PASSIMA_PRIORITY'),
              ),

              SettingText(
                label: "PREFS__PTSCREENS_PRIORITY",
                value: provider.getValue('PTSCREENS_PRIORITY'),
              ),

              SettingText(
                label: "PREFS__LENSDUMP_PRIORITY",
                value: provider.getValue('LENSDUMP_PRIORITY'),
              ),

              SettingText(
                label: "PREFS__FREE_IMAGE_PRIORITY",
                value: provider.getValue('FREE_IMAGE_PRIORITY'),
              ),

              SettingText(
                label: "PREFS__IMGBB_PRIORITY",
                value: provider.getValue('IMGBB_PRIORITY'),
              ),

              SettingText(
                label: "PREFS__IMGFI_PRIORITY",
                value: provider.getValue('IMGFI_PRIORITY'),
              ),

              SettingText(
                label: "PREFS__IMARIDE_PRIORITY",
                value: provider.getValue('IMARIDE_PRIORITY'),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
