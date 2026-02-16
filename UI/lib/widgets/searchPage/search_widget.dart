import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/searchPage/search.dart';
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
          (p) => p.getValue('SCAN_PATH')
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
                final jobListId = posterProvider.posterItems.first.jobListId;

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

            /// Enter a keyword
            onSubmitted: (value) {
              // check if the list is empty
              if (posterProvider.posterItems.isEmpty) {
                return;
              }

              /// As above , get job_list_id, talk to console, run endpoint
              final jobListId = posterProvider.posterItems.first.jobListId;

              /// Console log ( the job Page)
              final String notifyString =
                  "Searching text... in jobList $jobListId";

              logProvider.add(notifyString, LogLevel.info);

              /// Pop pop
              showAppSnackBar(context, notifyString);

              /// Tracker Search in the results
              posterProvider.searchPoster(value);
            },

            /// SCAN
            onClickScan: () async {
              /// setting Page
              final String notifyString = "Reloading $scanPath ";

              ///Add notify to console
              logProvider.add(notifyString, LogLevel.info);

              /// popup message
              showAppSnackBar(context, notifyString);

              /// https://dart.dev/tools/diagnostics/use_build_context_synchronously?utm_source=dartdev&utm_medium=redir&utm_id=diagcode&utm_content=use_build_context_synchronously
              final String? error = await posterProvider.scan(
                _controller.text,
              );
              if (error != null) {
                if (error.isNotEmpty) {
                  if (context.mounted) {
                    notifyTheUser(context, error);
                  }
                }
              }
            },

            /// TRACKER
            onClickTracker: (value) {
              /// Passes search value
              final String notifyString = "Searching... '$value' in tracker";
              logProvider.add(notifyString, LogLevel.info);
              showAppSnackBar(context, notifyString);
              posterProvider.searchPoster(value);
            },

            /// DELETE
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
