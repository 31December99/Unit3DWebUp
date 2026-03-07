import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'package:UI/widgets/searchPage/image_screenshots_widget.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/models/models.dart';
import 'package:UI/widgets/widgets.dart';

/// Show Window when user click a poster only if source is local
///
/// Attributes:
/// - item PosterItem: data model representing a poster
///
/// Methods:
/// - showPosterPopup: Get a PosterItem and open a dialog to show input box
void showPosterPopup(BuildContext context, PosterItem item) {
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
        backgroundColor: Colors.transparent,
        insetPadding: EdgeInsets.symmetric(
          horizontal: isMobile ? 12 : 24,
          vertical: isMobile ? 12 : 24,
        ),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        child: Container(
          decoration: BoxDecoration(
            color: Color(0xFF121522),
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: Color(0xFF59182C).withValues(alpha: 0.4),

                /// 0xFF182A59
                blurRadius: 20,
                spreadRadius: 2,
                offset: Offset(0, 8),
              ),
            ],
          ),
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
                    Center(
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(8),
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
                          /// Display Name
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
                              PosterItem notify = PosterItem(
                                snackBarStatus: 'Edit DisplayName job $jobId',
                              );
                              logProvider.add(
                                notify.snackBarStatus,
                                LogLevel.info,
                              );
                              showAppSnackBar(context, notify);
                            },
                          ),
                          const SizedBox(height: 12),

                          /// TMDB ID
                          CtextField(
                            label: "TMDB id",
                            controller: tmdbController,
                            onSubmitted: (_) async {
                              final jobId = item.jobId;
                              if (jobId == null || jobId.isEmpty) return;
                              final message = await posterProvider
                                  .updatePosterId(
                                    jobId,
                                    'tmdb_id',
                                    tmdbController.text,
                                  );
                              logProvider.add(
                                message.snackBarStatus,
                                LogLevel.info,
                              );
                              showAppSnackBar(context, message);
                            },
                          ),
                          const SizedBox(height: 12),

                          /// TVDB ID
                          CtextField(
                            label: "TVDB id",
                            controller: tvdbController,
                            onSubmitted: (_) async {
                              final jobId = item.jobId;
                              if (jobId == null || jobId.isEmpty) return;

                              final message = await posterProvider.updateTvdbId(
                                jobId,
                                'tvdb_id',
                                tvdbController.text,
                              );
                              logProvider.add(
                                message.snackBarStatus,
                                LogLevel.info,
                              );
                              showAppSnackBar(context, message);
                            },
                          ),
                          const SizedBox(height: 12),

                          /// IMDB ID
                          CtextField(
                            label: "IMDB id",
                            controller: imdbController,
                            onSubmitted: (_) async {
                              final jobId = item.jobId;
                              if (jobId == null || jobId.isEmpty) return;
                              final PosterItem message = await posterProvider
                                  .updateImdbId(
                                    jobId,
                                    'imdb_id_from_tvdb',
                                    imdbController.text,
                                  );
                              logProvider.add(
                                message.snackBarStatus,
                                LogLevel.info,
                              );
                              showAppSnackBar(context, message);
                            },
                          ),
                          const SizedBox(height: 12),

                          /// Poster URL
                          CtextField(
                            label: "Poster Url",
                            controller: posterController,
                            onSubmitted: (_) async {
                              final jobId = item.jobId;
                              if (jobId == null || jobId.isEmpty) return;
                              final PosterItem message = await posterProvider
                                  .updatePosterUrl(
                                    jobId,
                                    'backdrop_path',
                                    posterController.text,
                                  );
                              logProvider.add(
                                message.snackBarStatus,
                                LogLevel.info,
                              );
                              showAppSnackBar(context, message);
                            },
                          ),
                          const SizedBox(height: 12),

                          /// Screenshots
                          ImageScreenshots(screenshots: item.screenshots),
                          const SizedBox(height: 30),

                          /// JOB IDs
                          CtextIcon(
                            label: 'JOB ID: ${item.jobId ?? " "}',
                            svgAsset: 'lib/assets/job-search-svgrepo-com.svg',
                            iconWidth: 15,
                          ),
                          CtextIcon(
                            label: 'JOBLIST ID: ${item.jobListId ?? " "}',
                            svgAsset: 'lib/assets/job-search-svgrepo-com.svg',
                            iconWidth: 15,
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),

                  /// BUTTONS
                  Wrap(
                    spacing: 8,
                    runSpacing: 4,
                    alignment: WrapAlignment.end,
                    children: [
                      TextButton(
                        onPressed: () async {
                          final jobListId = item.jobListId;
                          final jobId = item.jobId;
                          if (jobId == null || jobId.isEmpty) return;
                          final PosterItem notifyString = await posterProvider
                              .makeTorrent(jobId, jobListId);
                          showAppSnackBar(context, notifyString);
                          logProvider.add(
                            notifyString.snackBarStatus,
                            LogLevel.info,
                          );
                        },
                        child: const Text(
                          "MAKE TORRENT",
                          style: TextStyle(fontSize: 10),
                        ),
                      ),
                      TextButton(
                        onPressed: () async {
                          final jobId = item.jobId;
                          if (jobId == null || jobId.isEmpty) return;
                          final PosterItem notify = await posterProvider
                              .uploadTorrent(jobId);
                          logProvider.add(notify.snackBarStatus, LogLevel.info);
                          showAppSnackBar(context, notify);
                        },
                        child: const Text(
                          "UPLOAD",
                          style: TextStyle(fontSize: 10),
                        ),
                      ),
                      TextButton(
                        onPressed: () async {
                          final jobId = item.jobId;
                          if (jobId == null || jobId.isEmpty) return;
                          final PosterItem notify = await posterProvider
                              .seedTorrent(jobId);
                          logProvider.add(notify.snackBarStatus, LogLevel.info);
                          showAppSnackBar(context, notify);
                        },

                        child: const Text(
                          "SEED TORRENT",
                          style: TextStyle(fontSize: 10),
                        ),
                      ),
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
        ),
      );
    },
  );
}
