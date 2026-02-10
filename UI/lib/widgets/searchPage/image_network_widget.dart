import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/widgets/widgets.dart';
import 'package:UI/config/constants.dart';


/// Load an image from the web and display it on the page
class ImageNetwork extends StatelessWidget {

  // Poster Data
  final List<PosterItem> posterItems;
  // Callback for Tap function
  final Function(PosterItem) onPosterTap;

  const ImageNetwork({
    super.key,
    required this.posterItems,
    required this.onPosterTap,
  });

  @override
  Widget build(BuildContext context) {
    if (posterItems.isEmpty) {
      return const Center(child: Text("Nessun poster"));
    }

    return GridView.builder(
      padding: const EdgeInsets.all(4),
      gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
        maxCrossAxisExtent: 160,
        mainAxisSpacing: 8,
        crossAxisSpacing: 8,
        childAspectRatio: .55,
      ),
      itemCount: posterItems.length,
      itemBuilder: (context, index) {
        final item = posterItems[index];
        return GestureDetector(
          onTap: () => onPosterTap(item),
          child: Column(
            children: [
              Expanded(
                child: Stack(
                  children: [
                    // Create a tooltip to show the current status
                    Ctooltip(
                      message: JobStatus.msg(item.status),
                      child: Image.network(
                        item.posterUrl ?? '',
                        fit: BoxFit.cover,
                        width: double.infinity,
                        errorBuilder: (_, __, ___) =>
                            const Center(child: Icon(Icons.broken_image)),
                      ),
                    ),
                    // Build a status bar (process)
                    // It can show progress, error , success message
                    ProcessBar(
                      // Apply color to status bar based on the source value
                      source: item.source == 'remote'
                          ? Colors.blueGrey
                          : Colors.green,
                      process: item.process ?? '',
                      alignment: Alignment.bottomCenter,
                    ),

                    // Linea verde in basso se source == "remote"
                    // Align(
                    //   alignment: Alignment.bottomCenter,
                    //   child: Container(
                    //     height: 4,
                    //     width: 100, //double.infinity,
                    //     color: item.source == 'remote'
                    //         ? Colors.blueGrey
                    //         : Colors.green,
                    //   ),
                    // ),
                  ],
                ),
              ),
              const SizedBox(height: 4),
              Text(
                item.displayName ?? '',
                textAlign: TextAlign.center,
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  fontFamily: 'WhiteRabbit',
                  fontSize: 12,
                  color: Color(0xFF1E1E1D),
                  //letterSpacing: 1,
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
