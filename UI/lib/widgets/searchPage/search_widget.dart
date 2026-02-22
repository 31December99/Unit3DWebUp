import 'package:url_launcher/url_launcher.dart';
import 'package:UI/widgets/searchPage/search.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/widgets.dart';
import 'package:UI/models/models.dart';
import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

/// Search
/// This page comes with a textbox and icon buttons
class Search extends StatefulWidget {
  const Search({super.key});

  @override
  State<Search> createState() => _SearchState();
}

class _SearchState extends State<Search> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void notifyTheUser(BuildContext context, String errorMessage) {
    showAppSnackBar(
      context,
      errorMessage,
      duration: const Duration(seconds: 2),
      backgroundColor: Colors.redAccent,
    );
  }

  @override
  Widget build(BuildContext context) {
    final posterProvider = context.read<PosterProvider>();
    final logProvider = context.read<LogProvider>();

    final scanPath = context.select<SettingProvider, String>(
      (p) => p.getValue('SCAN_PATH'),
    );

    return Container(
      padding: const EdgeInsets.all(12),
      child: Column(
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              const Text(
                'UNIT3D',
                style: TextStyle(
                  fontFamily: 'WhiteRabbit',
                  fontSize: 20,
                  color: Color(0xFFF30420),
                  letterSpacing: 1,
                ),
              ),

              const SizedBox(width: 1),

              const Text(
                'web',
                style: TextStyle(
                  fontFamily: 'Orbitron',
                  fontSize: 20,
                  color: Color(0xFFFF6B35), //Color(0xFFF35F04),

                  letterSpacing: 1,
                ),
              ),

              const SizedBox(width: 1),

              const Text(
                'UP',
                style: TextStyle(
                  fontFamily: 'WhiteRabbit',
                  fontSize: 20,
                  color: Color(0xFFF30420),
                  letterSpacing: 1,
                ),
              ),

              Align(
                alignment: Alignment.bottomCenter,
                heightFactor: 0.8,
                child: Ctooltip(
                  message: "Carica tutto su tracker!",
                  child: IconButton(
                    onPressed: () {
                      final jobListId =
                          posterProvider.posterItems.first.jobListId;

                      final String notifyString =
                          'Uploading job list $jobListId Please wait...';

                      logProvider.add(notifyString, LogLevel.info);
                      showAppSnackBar(context, notifyString);

                      posterProvider.uploadList(jobListId!);
                    },
                    icon: SvgPicture.asset(
                      'lib/assets/upload-svgrepo-com.svg',
                      width: 25,
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 30),

              SizedBox(
                width: MediaQuery.of(context).size.width * 0.25,
                child: SearchTextField(
                  controller: _controller,
                  onSubmitted: (value) {
                    if (posterProvider.posterItems.isEmpty) return;

                    final jobListId =
                        posterProvider.posterItems.first.jobListId;

                    final String notifyString =
                        "Searching text... in jobList $jobListId";

                    logProvider.add(notifyString, LogLevel.info);
                    showAppSnackBar(context, notifyString);

                    posterProvider.searchPoster(value);
                  },
                  onClickScan: () async {
                    final String notifyString = "Reloading $scanPath ";

                    logProvider.add(notifyString, LogLevel.info);
                    showAppSnackBar(context, notifyString);

                    final String? error = await posterProvider.scan(
                      _controller.text,
                    );

                    if (error != null && error.isNotEmpty && context.mounted) {
                      notifyTheUser(context, error);
                    }
                  },
                  onClickTracker: (value) {
                    final String notifyString =
                        "Searching... '$value' in tracker";

                    logProvider.add(notifyString, LogLevel.info);
                    showAppSnackBar(context, notifyString);

                    posterProvider.searchPoster(value);
                  },
                  onClickClear: () {
                    final String notifyString =
                        "Deleting... job list '${posterProvider.posterItems[0].jobListId}'";

                    logProvider.add(notifyString, LogLevel.info);
                    showAppSnackBar(context, notifyString);

                    posterProvider.clearPosterItems();
                  },
                ),
              ),

              const SizedBox(width: 20),

              InkWell(
                onTap: () async {
                  final Uri url = Uri.parse(
                    'https://github.com/31december1999/',
                  );

                  if (await canLaunchUrl(url)) {
                    await launchUrl(url);
                  }
                },
                child: const Text(
                  "GitHub",
                  style: TextStyle(
                    color: Colors.blueAccent,
                    decoration: TextDecoration.underline,
                    fontWeight: FontWeight.w500,
                    fontSize: 12,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),

          const AddPoster(),
        ],
      ),
    );
  }
}
