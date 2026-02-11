import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/settings/settings.dart';

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

    Map<String, dynamic>? prefs = setting.userPreferences;

    return TabBarView(
      /// I° TAB Paths
      children: [
        SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [

              SettingText(
                label: "YOUTUBE_FAV_CHANNEL_ID",
                value:
                    prefs?['YOUTUBE_FAV_CHANNEL_ID']?.toString() ??
                    provider.selectedYouTubeFavChannelId,
                onChanged: (value) => provider.youTubeFavChannelId(value),
                hint: "id è parte dell'url del canale",
              ),

              SettingText(
                label: "WATCHER_INTERVAL",
                value:
                    prefs?['WATCHER_INTERVAL']?.toString() ??
                    provider.selectedWatcherInterval,
                onChanged: (value) => provider.watcherInterval(value),
              ),

              SettingText(
                label: "WATCHER_PATH",
                value:
                    prefs?['WATCHER_PATH']?.toString() ??
                    provider.selectedWatcherPath,
                onChanged: (value) => provider.watcherPath(value),
              ),

              SettingText(
                label: "WATCHER_DESTINATION_PATH",
                value:
                    prefs?['WATCHER_DESTINATION_PATH']?.toString() ??
                    provider.selectedWatcherDestinationPath,
                onChanged: (value) => provider.watcherDestinationPath(value),
              ),

              SettingText(
                label: "TORRENT_ARCHIVE_PATH",
                value:
                    prefs?['TORRENT_ARCHIVE_PATH']?.toString() ??
                    provider.selectedTorrentArchivePath,
                onChanged: (value) => provider.torrentArchivePath(value),
              ),

              SettingText(
                label: "CACHE_PATH",
                value:
                    prefs?['CACHE_PATH']?.toString() ??
                    provider.selectedCachePath,
                onChanged: (value) => provider.cachePath(value),
              ),

              SettingText(
                label: "TORRENT_COMMENT",
                value:
                    prefs?['TORRENT_COMMENT']?.toString() ??
                    provider.selectedTorrentComment,
                onChanged: (value) => provider.torrentComment(value),
              ),

              SettingText(
                label: "PATH SCAN n° 1",
                value:
                    prefs?['PATH_SCAN_01']?.toString() ??
                    provider.selectedScanpath01,
                onChanged: (value) => provider.pathScan01(value),
              ),
            ],
          ),
        ),

        /// II° TAB Preference
        SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              SettingSwitch(
                label: "Inserisce un trailer YouTube ( solo se esiste) ",
                value: provider.youtubeChannelEnable,
                onChanged: (_) => provider.youtube(),
              ),

              SettingSwitch(
                label: "Duplicate",
                value: provider.duplicateOn,
                onChanged: (_) => provider.duplicate(),
              ),

              SettingText(
                label: "SIZE_TH",
                value: prefs?['SIZE_TH']?.toString() ?? provider.selectedSizeTh,
                onChanged: (value) => provider.sizeTh(value),
                hint: "es. 100",
              ),

              SettingSwitch(
                label: "Skippa ogni duplicato senza chiedere conferma",
                value: provider.skipDuplicate,
                onChanged: (_) => provider.dpSkip(),
              ),

              SettingSwitch(
                label: "Skippa in caso di Tmdb_id non trovato ( verificare..)",
                value: provider.skipTmdb,
                onChanged: (_) => provider.tmdbSkip(),
              ),

              SettingSwitch(
                label: "Ridimensiona automaticamente ogni screenshot",
                value: provider.resizeScshot,
                onChanged: (_) => provider.rszScshot(),
              ),

              SettingSwitch(
                label: "Rende 'anonimo' l'utente durante l'upload",
                value: provider.anon,
                onChanged: (_) => provider.anonUser(),
              ),

              SettingSwitch(
                label: "Salva nella cache locale l'url di ogni screenshot",
                value: provider.cacheScshot,
                onChanged: (_) => provider.cacheScreenshot(),
              ),

              SettingSwitch(
                label: "Salva nella cache locale TMDB ID e titolo",
                value: provider.cacheDbonline,
                onChanged: (_) => provider.cacheTmdb(),
              ),

              SettingSwitch(
                label: "Ogni torrent è una personal release",
                value: provider.personalRel,
                onChanged: (_) => provider.personalRelease(),
              ),

              SettingSwitch(
                label: "Aggiungi un gif webp agli screenshot",
                value: provider.webp,
                onChanged: (_) => provider.webpScshot(),
              ),
            ],
          ),
        ),

        /// III° TAB Options
        SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              SettingDropdown(
                label: "Imposta il numero di screenshot desiderato",
                items: provider.priorityHostOption,
                selected:
                    prefs?['SCR_SHOT']?.toString() ?? provider.selectedScrShot,
                onChanged: (value) =>
                    value != null ? provider.numScsShot(value) : null,
              ),

              SettingText(
                label: "COMPRESS_SCSHOT",
                value:
                    prefs?['NUM_COMPRESS_SCSHOT']?.toString() ??
                    provider.selectedNumCompressShot,
                onChanged: (value) => provider.numCompressScsShot(value),
              ),

              SettingDropdown(
                label: "PASSIMA_PRIORITY",
                items: provider.priorityHostOption,
                selected:
                    prefs?['PASSIMA_PRIORITY']?.toString() ??
                    provider.selectedPriorityPassima,
                onChanged: (value) =>
                    value != null ? provider.Passima(value) : null,
              ),

              SettingDropdown(
                label: "PTSCREENS_PRIORITY",
                items: provider.priorityHostOption,
                selected:
                    prefs?['PTSCREENS_PRIORITY']?.toString() ??
                    provider.selectedPriorityPtScreens,
                onChanged: (value) =>
                    value != null ? provider.PtScreens(value) : null,
              ),

              SettingDropdown(
                label: "LENSDUMP_PRIORITY",
                items: provider.priorityHostOption,
                selected:
                    prefs?['LENSDUMP_PRIORITY']?.toString() ??
                    provider.selectedPriorityLensDump,
                onChanged: (value) =>
                    value != null ? provider.lensDump(value) : null,
              ),

              SettingDropdown(
                label: "FREE_IMAGE_PRIORITY",
                items: provider.priorityHostOption,
                selected:
                    prefs?['FREE_IMAGE_PRIORITY']?.toString() ??
                    provider.selectedPriorityFreeImage,
                onChanged: (value) =>
                    value != null ? provider.freeImage(value) : null,
              ),

              SettingDropdown(
                label: "IMGBB_PRIORITY",
                items: provider.priorityHostOption,
                selected:
                    prefs?['IMGBB_PRIORITY']?.toString() ??
                    provider.selectedPriorityImgBB,
                onChanged: (value) =>
                    value != null ? provider.imgBB(value) : null,
              ),

              SettingDropdown(
                label: "IMGFI_PRIORITY",
                items: provider.priorityHostOption,
                selected:
                    prefs?['IMGFI_PRIORITY']?.toString() ??
                    provider.selectedPriorityImgfi,
                onChanged: (value) =>
                    value != null ? provider.imgFi(value) : null,
              ),

              SettingDropdown(
                label: "IMARIDE_PRIORITY",
                items: provider.priorityHostOption,
                selected:
                    prefs?['IMARIDE_PRIORITY']?.toString() ??
                    provider.selectedPriorityImaride,
                onChanged: (value) =>
                    value != null ? provider.imaRide(value) : null,
              ),
            ],
          ),
        ),
      ],
    );
  }
}
