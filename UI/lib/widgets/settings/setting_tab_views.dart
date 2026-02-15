import 'package:UI/widgets/settings/settings.dart';
import 'package:UI/providers/providers.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/widgets/widgets.dart';

/// Custom widget to represent TABS in SettingPage
class SettingTabViews extends StatelessWidget {
  const SettingTabViews({super.key});


  /// Notify the user: Docker needs to be restarted because the paths are mounted
  void dockerRestart(BuildContext context) {
    showAppSnackBar(
      context,
      "Please Restart docker or run docker-compose restart",
      duration: Duration(seconds: 2),
      backgroundColor: Colors.redAccent,
    );
  }

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
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__WATCHER_INTERVAL', value),
              ),

              SettingText(
                label: "PREFS__WATCHER_PATH",
                value: provider.getValue('WATCHER_PATH'),
                onSubmitted: (value) async {
                  await provider.setEnv('PREFS__WATCHER_PATH', value);
                  if (!context.mounted) return;
                  dockerRestart(context);
                },
              ),

              SettingText(
                label: "PREFS__WATCHER_DESTINATION_PATH",
                value: provider.getValue('WATCHER_DESTINATION_PATH'),
                onSubmitted: (value) async {
                  await provider.setEnv(
                    'PREFS__WATCHER_DESTINATION_PATH',
                    value,
                  );
                  if (!context.mounted) return;
                  dockerRestart(context);
                },
              ),

              SettingText(
                label: "PREFS__TORRENT_ARCHIVE_PATH",
                value: provider.getValue('TORRENT_ARCHIVE_PATH'),
                onSubmitted: (value) async {
                  await provider.setEnv('PREFS__TORRENT_ARCHIVE_PATH', value);
                  if (!context.mounted) return;
                  dockerRestart(context);
                },
              ),

              SettingText(
                label: "PREFS__CACHE_PATH",
                value: provider.getValue('CACHE_PATH'),
                onSubmitted: (value) async {
                  await provider.setEnv('PREFS__CACHE_PATH', value);
                  if (!context.mounted) return;
                  dockerRestart(context);
                },
              ),

              SettingText(
                label: "PREFS__SCAN_PATH",
                value: provider.getValue('SCAN_PATH'),
                onSubmitted: (value) async {
                  await provider.setEnv('PREFS__SCAN_PATH', value);
                  if (!context.mounted) return;
                  dockerRestart(context);
                },
              ),

              SettingText(
                label: "PREFS__TORRENT_COMMENT",
                value: provider.getValue('TORRENT_COMMENT'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__TORRENT_COMMENT', value),
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
                label: "Inserisce un trailer YouTube ( solo se esiste) ",
                value: provider.getValue('YOUTUBE_CHANNEL_ENABLE'),
                onSubmitted: (value) async => await provider.setEnv(
                  'PREFS__YOUTUBE_CHANNEL_ENABLE',
                  value,
                ),
              ),

              SettingText(
                label: "Confronto il tuo torrent con uno presente nel tracker",
                value: provider.getValue('DUPLICATE_ON'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__DUPLICATE_ON', value),
              ),

              SettingText(
                label: "PREFS__SIZE_TH",
                value: provider.getValue('SIZE_TH'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__SIZE_TH', value),
                hint: "es. 100",
              ),

              SettingText(
                label: "Skippa ogni duplicato senza chiedere conferma",
                value: provider.getValue('SKIP_DUPLICATE'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__SKIP_DUPLICATE', value),
              ),

              SettingText(
                label: "Skippa in caso di Tmdb_id non trovato ( verificare..)",
                value: provider.getValue('SKIP_TMDB'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__SKIP_TMDB', value),
              ),

              SettingText(
                label: "Ridimensiona automaticamente ogni screenshot",
                value: provider.getValue('SKIP_TMDB'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__RESIZE_SCSHOT', value),
              ),

              SettingText(
                label: "Rende 'anonimo' l'utente durante l'upload",
                value: provider.getValue('ANON'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__ANON', value),
              ),

              SettingText(
                label: "Salva nella cache locale l'url di ogni screenshot",
                value: provider.getValue('CACHE_SCR'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__CACHE_SCR', value),
              ),

              SettingText(
                label: "Salva nella cache locale TMDB ID e titolo",
                value: provider.getValue('CACHE_DBONLINE'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__CACHE_DBONLINE', value),
              ),

              SettingText(
                label: "Ogni torrent è una personal release",
                value: provider.getValue('PERSONAL_RELEASE'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__PERSONAL_RELEASE', value),
              ),

              SettingText(
                label: "Aggiungi un gif webp agli screenshot",
                value: provider.getValue('WEBP_ENABLED'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__WEBP_ENABLED', value),
              ),
              SettingText(
                label: "PREFS__YOUTUBE_FAV_CHANNEL_ID",
                value: provider.getValue('YOUTUBE_FAV_CHANNEL_ID'),
                onSubmitted: (value) async => await provider.setEnv(
                  'PREFS__YOUTUBE_FAV_CHANNEL_ID',
                  value,
                ),
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
                label: "Imposta il numero di screenshot desiderato",
                value: provider.getValue('NUMBER_OF_SCREENSHOTS'),
                onSubmitted: (value) async => await provider.setEnv(
                  'PREFS__NUMBER_OF_SCREENSHOTS',
                  value,
                ),
              ),

              SettingText(
                label: "PREFS__PASSIMA_PRIORITY",
                value: provider.getValue('PASSIMA_PRIORITY'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__PASSIMA_PRIORITY', value),
              ),

              SettingText(
                label: "PREFS__COMPRESS_SCSHOT",
                value: provider.getValue('COMPRESS_SCSHOT'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__COMPRESS_SCSHOT', value),
              ),

              SettingText(
                label: "PREFS__PTSCREENS_PRIORITY",
                value: provider.getValue('PTSCREENS_PRIORITY'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__PTSCREENS_PRIORITY', value),
              ),

              SettingText(
                label: "PREFS__LENSDUMP_PRIORITY",
                value: provider.getValue('LENSDUMP_PRIORITY'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__LENSDUMP_PRIORITY', value),
              ),

              SettingText(
                label: "PREFS__FREE_IMAGE_PRIORITY",
                value: provider.getValue('FREE_IMAGE_PRIORITY'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__FREE_IMAGE_PRIORITY', value),
              ),

              SettingText(
                label: "PREFS__IMGBB_PRIORITY",
                value: provider.getValue('IMGBB_PRIORITY'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__IMGBB_PRIORITY', value),
              ),

              SettingText(
                label: "PREFS__IMGFI_PRIORITY",
                value: provider.getValue('IMGFI_PRIORITY'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__IMGFI_PRIORITY', value),
              ),
              SettingText(
                label: "PREFS__IMARIDE_PRIORITY",
                value: provider.getValue('IMARIDE_PRIORITY'),
                onSubmitted: (value) async =>
                    await provider.setEnv('PREFS__IMARIDE_PRIORITY', value),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
