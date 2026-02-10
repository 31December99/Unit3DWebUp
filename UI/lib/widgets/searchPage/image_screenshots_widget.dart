import 'package:url_launcher/url_launcher.dart';
import 'package:flutter/material.dart';
import 'package:UI/widgets/widgets.dart';


/// Add a list of screenshot links to the popup window
///
class ImageScreenshots extends StatelessWidget {
  final List<dynamic>? screenshots;

  const ImageScreenshots({super.key, required this.screenshots});

  Future<void> _launchUrl(String url) async {
    final uri = Uri.parse(url);
    if (!await launchUrl(uri, webOnlyWindowName: '_blank')) {
      debugPrint('Could not launch $url');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (screenshots == null || screenshots!.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(8),
        child: Text("Screenshots non disponibili"),
      );
    }

    /// Receive a list of links from the PosterItem
    /// and display them as clickable items
    return Wrap(
      spacing: 8,
      runSpacing: 4,
      // crossAxisAlignment: CrossAxisAlignment.center,
      children: List.generate(screenshots!.length, (index) {
        final url = screenshots![index];
        final title = 'Screenshot ${index + 1} ';

        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 4),
          child: InkWell(
            /// clickable link
            onTap: () => _launchUrl(url),
            child: Ctooltip(
              message: url,
              child: CtextIcon(
                label: title,
                svgAsset:
                    'lib/assets/youtube-video-movie-film-multimedia-social-media-svgrepo-com.svg',
                iconWidth: 15,
                onIconPressed: () {},
              ),
            ),
          ),
        );
      }),
    );
  }
}
