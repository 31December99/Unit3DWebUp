import 'package:url_launcher/url_launcher.dart';
import 'package:UI/widgets/searchPage/search.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/widgets.dart';
import 'package:UI/models/models.dart';
import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

/// Search
/// This page comes with a textbox and four icon button
class Search extends StatefulWidget {
  const Search({super.key});

  @override
  State<Search> createState() => _SearchState();
}

class _SearchState extends State<Search> {
  late final TextEditingController _controller;
  bool isChecked = false;

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

  /// Notify the user: TODO: one or more errors
  void notifyTheUser(BuildContext context, errorMessage) {
    showAppSnackBar(
      context,
      errorMessage,
      duration: Duration(seconds: 2),
      backgroundColor: Colors.redAccent,
    );
  }

  @override
  Widget build(BuildContext context) {
    final posterProvider = context.read<PosterProvider>();

    final scanPath = context.select<SettingProvider, String>(
      (p) => p.getValue('SCAN_PATH'),
    );

    final logProvider = context.read<LogProvider>();

    return Container(
      padding: const EdgeInsets.all(1),
      child: Column(
        children: [
          Align(
            alignment: Alignment.topRight,
            child: Padding(
              padding: const EdgeInsets.only(right: 12, bottom: 8),
              child: InkWell(
                onTap: () async {
                  final Uri url = Uri.parse(
                    'https://github.com/tuo-username/tuo-repo',
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
                  ),
                ),
              ),
            ),
          ),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Row(
                children: const [
                  Text(
                    'UNIT3D',
                    style: TextStyle(
                      fontFamily: 'WhiteRabbit',
                      fontSize: 20,
                      color: Color(0xFFF30420),
                      letterSpacing: 1,
                    ),
                  ),
                  SizedBox(width: 4),
                  Text(
                    'WEBUP',
                    style: TextStyle(
                      fontFamily: 'WhiteRabbit',
                      fontSize: 20,
                      color: Colors.white,
                      letterSpacing: 1,
                    ),
                  ),
                ],
              ),

              const SizedBox(width: 25),

              Row(
                children: [
                  Ctooltip(
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

                  const SizedBox(width: 15),

                  InkWell(
                    onTap: () => showAppSnackBar(context, "Filtro: Film"),
                    child: const Text(
                      "Film",
                      style: TextStyle(
                        color: Colors.blueAccent,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),

                  const SizedBox(width: 10),

                  InkWell(
                    onTap: () => showAppSnackBar(context, "Filtro: Serie"),
                    child: const Text(
                      "Serie",
                      style: TextStyle(
                        color: Colors.blueAccent,
                        decoration: TextDecoration.underline,
                      ),
                    ),
                  ),

                  const SizedBox(width: 10),
                ],
              ),

              const SizedBox(width: 30),

              SizedBox(
                width: MediaQuery.of(context).size.width * 0.5,
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
            ],
          ),

          const SizedBox(height: 10),
          const AddPoster(),
        ],
      ),
    );
  }
}
