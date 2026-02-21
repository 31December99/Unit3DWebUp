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

    // Calcola il numero di poster per riga in base alla larghezza dello schermo
    final screenWidth = MediaQuery.of(context).size.width;
    final crossAxisCount = (screenWidth / 100).floor().clamp(1, 9);
    // minimo 1 poster, massimo 9 per riga

    return GridView.builder(
      padding: const EdgeInsets.all(4),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: crossAxisCount,
        mainAxisSpacing: 8,
        crossAxisSpacing: 8,
        childAspectRatio: 0.65, // <-- aspect ratio dei poster
      ),
      itemCount: posterItems.length,
      itemBuilder: (context, index) {
        final item = posterItems[index];
        return GestureDetector(
          onTap: () => onPosterTap(item),
          child: Column(
            children: [
              Expanded(
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(6), // angoli discreti
                    color: Colors.grey[200], // colore di fallback
                  ),
                  clipBehavior: Clip.hardEdge, // garantisce gli angoli smussati
                  child: Stack(
                    children: [
                      // Create a tooltip to show the current status
                      Ctooltip(
                        message: JobStatus.msg(item.status),
                        child: Image.network(
                          item.posterUrl ?? '',
                          fit: BoxFit.cover,
                          width: double.infinity,
                          height: double.infinity,
                          errorBuilder: (_, __, ___) =>
                              const Center(child: Icon(Icons.broken_image)),
                        ),
                      ),
                      // Status bar
                      // It can show progress, error , success message
                      Align(
                        alignment: Alignment.topCenter,
                        child: ProcessBar(
                          source: item.source == 'remote'
                              ? Colors.blueGrey
                              : Colors.black,
                          process: item.process ?? '',
                          alignment: Alignment.topCenter,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 4),
            ],
          ),
        );
      },
    );
  }
}
