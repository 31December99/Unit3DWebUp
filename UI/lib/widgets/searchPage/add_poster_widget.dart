import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/searchPage/search.dart';

/// Add a poster to SearchPage for each job_id
///
/// Each poster is an image loaded from a remote tmdb url
///
/// Each poster shows a line at the bottom used to display status messages
/// for example: progress %, errore messages or success messages, source

class AddPoster extends StatelessWidget {
  const AddPoster({super.key});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      /// Consumer of PosterProvider
      /// Listens to PosterProvider and rebuilds when notifyListeners is called
      /// Rebuilds only the widgets inside the Consumer
      /// Using context.watch() would rebuild all
      child: Consumer<PosterProvider>(
        builder: (_, provider, __) {
          if (provider.isLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          // Show 'N/A' if job_list is empty
          if (provider.posterItems.isEmpty) {
            return const Center(child: Text("N/A"));
          }

          // This widget draw the poster
          return ImageNetwork(
            posterItems: provider.posterItems,
            // Popup window to edit TmdbID, TvdbID, displayName, posterUrl
            // and to create, upload or seed torrents
            onPosterTap: (item) =>
                // event tap to show a new popup when source is local
                item.source == 'local' ? showPosterPopup(context, item) : null,
          );
        },
      ),
    );
  }
}
