import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/searchPage/search.dart';
import 'package:UI/widgets/snack.dart';
import 'package:flutter_svg/svg.dart';
import 'package:UI/widgets/widgets.dart';
import 'package:UI/models/models.dart';

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

  @override
  Widget build(BuildContext context) {
    final posterProvider = context.read<PosterProvider>();
    // final settingProvider = context.watch<SettingProvider>();
    /// context.watch replaced with context.select
    /// Rebuild the widget Settings only if selectedScanpath01 changes
    /// thanks to context.select
    final selectedScanPath = context.select<SettingProvider, String>(
      (p) => p.selectedScanpath01,
    );

    final logProvider = context.read<LogProvider>();

    return Container(
      padding: const EdgeInsets.all(1),
      child: Column(
        children: [
          /// A personal widget with hover function (tooltip)
          Ctooltip(
            message: "Carica tutto su tracker!",
            child: IconButton(
              /// Event button
              onPressed: () {
                /// Every poster has a job_id and a job_list_id
                final jobListId = posterProvider.posterItems[0].jobListId;

                /// Preparare a message for the console log ( the job Page)
                final String notifyString =
                    'Uploading job list $jobListId Please wait...';

                /// Access to console by provider
                /// send message and defines its type
                logProvider.add(notifyString, LogLevel.info);

                /// Kind of message shown at the bottom
                showAppSnackBar(context, notifyString);

                /// Calls the endpoint
                /// Passes the job list id and requests upload to the tracker
                /// The backend reads data from Redis and start processing
                posterProvider.uploadList(jobListId!);
              },

              /// Graphic for icon. See Asset folder
              icon: SvgPicture.asset(
                'lib/assets/upload-svgrepo-com.svg',
                width: 25,
              ),
            ),
          ),

          /// Label
          Text(
            'UNIT3D Up',
            style: const TextStyle(
              fontFamily: 'WhiteRabbit',
              fontSize: 20,
              color: Color(0xFFCF8F4F),
              letterSpacing: 1,
            ),
          ),

          /// SEARCH TEXT BOX
          /// Use a custom widget ( it returns a  customized..TextField)
          /// as textbox
          SearchTextField(
            controller: _controller,
            onSubmitted: (value) {   /// <--- Enter a keyword
              /// As above , get job_list_id, talk to console, run endpoint
              final jobListId = posterProvider.posterItems[0].jobListId;

              /// Console log ( the job Page)
              final String notifyString =
                  "Searching text... in jobList $jobListId";
              logProvider.add(notifyString, LogLevel.info);

              /// Pop pop
              showAppSnackBar(context, notifyString);

              /// Tracker Search in the results
              posterProvider.searchPoster(value);
            },
            // onPressed: () {  ///
            //
            //   /// ...prepare the console message
            //   final String notifyString =
            //       "'Starting scan' ${settingProvider.selectedScanpath01}' Please wait...";
            //
            //   /// Talks to the console
            //   logProvider.add(notifyString, LogLevel.info);
            //
            //   /// Pop message
            //   showAppSnackBar(context, notifyString);
            //   posterProvider.scan(
            //     settingProvider.selectedScanpath01,
            //     _controller.text,
            //   );
            // },
            onClickScan: () {
              /// Scan endpoint
              /// Passes SelectedScanpath01 that is the field from the
              /// setting Page

              // final String notifyString =
              //     "Reloading ${settingProvider.selectedScanpath01}' Please wait...";
              final String notifyString =
                  "Reloading $selectedScanPath' Please wait...";

              logProvider.add(notifyString, LogLevel.info);
              showAppSnackBar(context, notifyString);
              posterProvider.scan(selectedScanPath, _controller.text);

              // posterProvider.scan(
              //   settingProvider.selectedScanpath01,
              //   _controller.text,
              // );
            },
            onClickTracker: (value) {
              /// Tracker endpoint
              /// Passes search value

              final String notifyString = "Searching... '$value' in tracker";
              logProvider.add(notifyString, LogLevel.info);
              showAppSnackBar(context, notifyString);
              posterProvider.searchPoster(value);
            },
            onClickClear: () {
              /// Request to backend to delete job_list_id (Page)
              ///
              final String notifyString =
                  "Deleting... job list '${posterProvider.posterItems[0].jobListId}'";
              logProvider.add(notifyString, LogLevel.info);
              showAppSnackBar(context, notifyString);
              posterProvider.clearPosterItems();
            },
          ),

          const SizedBox(height: 10),
          const AddPoster(),
        ],
      ),
    );
  }
}
