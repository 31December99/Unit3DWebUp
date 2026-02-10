import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'package:UI/widgets/searchPage/image_screenshots_widget.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/models/models.dart';
import 'package:UI/widgets/widgets.dart';

import '../snack.dart';

/// Show Window when user click a poster only if source is local
///
void showPosterPopup(BuildContext context, PosterItem item) {

  /// List of controllers for the user input
  ///
  /// Accept a new display Name
  final titleController = TextEditingController(text: item.displayName);

  /// Accept the new TMDB ID
  final tmdbController = TextEditingController(text: item.tmdbId);

  /// Accept the new TVDB ID
  final tvdbController = TextEditingController(text: item.tvdbId);

  /// Accept the new IMDB
  final imdbController = TextEditingController(text: item.imdbId);

  /// Accept a new poster Url
  final posterController = TextEditingController(text: item.posterUrl);

  /// Console log provider
  final logProvider = context.read<LogProvider>();

  /// Poster Provider
  final posterProvider = context.read<PosterProvider>();
  final size = MediaQuery.of(context).size;

  /// TODO later
  final bool isMobile = size.width < 600;
  final bool isTablet = size.width >= 600 && size.width < 1024;

  showDialog(
    context: context,
    builder: (_) {
      return Dialog(
        insetPadding: EdgeInsets.symmetric(
          horizontal: isMobile ? 12 : 24,
          vertical: isMobile ? 12 : 24,
        ),
        /// Window Box
        child: ConstrainedBox(
          constraints: BoxConstraints(
            maxWidth: isMobile
                ? size.width
                : isTablet
                ? 600
                : 800,
            maxHeight: size.height * 0.9,
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 20),
                if (posterController.text.isNotEmpty)
                  /// POSTER
                  Center(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      /// Add the poster to the popup window
                      child: Image.network(
                        posterController.text,
                        height: 200,
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) => Container(
                          height: 200,
                          width: double.infinity,
                          color: Colors.grey.shade300,
                          child: const Icon(Icons.broken_image, size: 40),
                        ),
                      ),
                    ),
                  ),
                const SizedBox(height: 20),
                Expanded(
                  child: SingleChildScrollView(
                    child: Column(
                      children: [
                        /// Edit Display Name
                        CtextField(
                          label: "Display Name",
                          controller: titleController,
                          onSubmitted: (_) {
                            final jobId = item.jobId;
                            if (jobId == null || jobId.isEmpty) return;
                            // Send the updated id to the backend
                            posterProvider.updatePosterDname(
                              jobId,
                              'display_name',
                              titleController.text,
                            );
                            // Update the log console
                            final String notifyString =
                                'Edit DisplayName job $jobId';
                            logProvider.add(notifyString, LogLevel.info);
                            // Popup message for the user
                            showAppSnackBar(context, notifyString);
                          },
                        ),
                        const SizedBox(height: 12),
                        /// Edit TMDB ID
                        CtextField(
                          label: "TMDB id",
                          controller: tmdbController,
                          onSubmitted: (_) {
                            final jobId = item.jobId;
                            if (jobId == null || jobId.isEmpty) return;
                            final String notifyString =
                                'Edit TMDB id job $jobId';
                            logProvider.add(notifyString, LogLevel.info);
                            showAppSnackBar(context, notifyString);
                            posterProvider.updatePosterId(
                              jobId,
                              'tmdb_id',
                              tmdbController.text,
                            );
                          },
                        ),
                        const SizedBox(height: 12),
                        /// Edit TVDB ID
                        CtextField(
                          label: "TVDB id",
                          controller: tvdbController,
                          onSubmitted: (_) {
                            final jobId = item.jobId;
                            if (jobId == null || jobId.isEmpty) return;
                            final String notifyString =
                                'Edit TVDB id job $jobId';
                            logProvider.add(notifyString, LogLevel.info);
                            showAppSnackBar(context, notifyString);
                            posterProvider.updateTvdbId(
                              jobId,
                              'tvdb_id',
                              tvdbController.text,
                            );
                          },
                        ),
                        const SizedBox(height: 12),
                        /// Edit IMDB ID
                        CtextField(
                          label: "IMDB id",
                          controller: imdbController,
                          onSubmitted: (_) {
                            final jobId = item.jobId;
                            if (jobId == null || jobId.isEmpty) return;
                            final String notifyString =
                                'Edit IMDB id job $jobId';
                            logProvider.add(notifyString, LogLevel.info);
                            showAppSnackBar(context, notifyString);
                            posterProvider.updateImdbId(
                              jobId,
                              'imdb_id_from_tvdb',
                              imdbController.text,
                            );
                          },
                        ),

                        const SizedBox(height: 12),
                        /// Edit Poster Url
                        CtextField(
                          label: "Poster Url",
                          controller: posterController,
                          onSubmitted: (_) {
                            final jobId = item.jobId;
                            if (jobId == null || jobId.isEmpty) return;
                            final String notifyString =
                                'Edit Poster Url job $jobId';
                            logProvider.add(notifyString, LogLevel.info);
                            showAppSnackBar(context, notifyString);
                            posterProvider.updatePosterUrl(
                              jobId,
                              'backdrop_path',
                              posterController.text,
                            );
                          },
                        ),

                        const SizedBox(height: 12),

                        /// Add the screenshots from the backend
                        // --- Link cliccabili degli screenshot ---
                        // TODO: controlla item.screenshots che non sia vuoto
                        ImageScreenshots(screenshots: item.screenshots),
                        const SizedBox(height: 30),
                        /// Print about JobID e JobListID
                        CtextIcon(
                          label: 'JOB ID: ${item.jobId ?? " "}',
                          svgAsset: 'lib/assets/ladybug-bug-svgrepo-com.svg',
                          iconWidth: 15,
                          /// onIconPressed: () {},
                        ),
                        CtextIcon(
                          label: 'JOBLIST ID: ${item.jobListId ?? " "}',
                          svgAsset: 'lib/assets/ladybug-bug-svgrepo-com.svg',
                          iconWidth: 15,
                          /// onIconPressed: () {},
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 12),

                /// BUTTONS
                /// maketorrent , upload , seed , close
                Wrap(
                  spacing: 8,
                  runSpacing: 4,
                  alignment: WrapAlignment.end,
                  children: [
                    /// MAKE TORRENT
                    TextButton(
                      onPressed: () async {
                        final jobListId = item.jobListId;
                        final jobId = item.jobId;
                        if (jobId == null || jobId.isEmpty) return;
                        final String notifyString =
                            'Make Torrent job $jobId Please wait...';
                        logProvider.add(notifyString, LogLevel.info);
                        showAppSnackBar(context, notifyString);
                        await posterProvider.makeTorrent(jobId, jobListId);
                      },
                      child: const Text(
                        "MAKE TORRENT",
                        style: TextStyle(fontSize: 10),
                      ),
                    ),
                    /// UPLOAD TORRENT
                    TextButton(
                      onPressed: () {
                        final jobId = item.jobId;
                        if (jobId == null || jobId.isEmpty) return;
                        final String notifyString =
                            'Upload Torrent job $jobId Please wait...';
                        logProvider.add(notifyString, LogLevel.info);
                        showAppSnackBar(context, notifyString);
                        posterProvider.uploadTorrent(jobId);
                      },
                      child: const Text(
                        "UPLOAD",
                        style: TextStyle(fontSize: 10),
                      ),
                    ),
                    /// SEED TORRENT
                    TextButton(
                      onPressed: () {
                        final jobId = item.jobId;
                        if (jobId == null || jobId.isEmpty) return;
                        final String notifyString =
                            'Seed Torrent job $jobId Please wait...';
                        logProvider.add(notifyString, LogLevel.info);
                        showAppSnackBar(context, notifyString);
                        posterProvider.seedTorrent(jobId);
                      },
                      child: const Text(
                        "SEED TORRENT",
                        style: TextStyle(fontSize: 10),
                      ),
                    ),
                    /// CLOSE WINDOW
                    TextButton(
                      onPressed: () => Navigator.of(context).pop(),
                      child: const Text("CHIUDI"),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      );
    },
  );
}
