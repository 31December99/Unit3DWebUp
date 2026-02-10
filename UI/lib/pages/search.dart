import 'package:flutter/material.dart';
import 'package:UI/widgets/searchPage/search.dart';

/// The SearchPage
///
/// This page contains a textbox for searching and four icon button
/// - Scan button: request to backend to get a list of Media from the local folder
/// - Tracker button: get the last torrent uploaded on the tracker
/// - Delete: Delete the current job_list (not the files)
/// - Full upload: Starts the process from creating the torrent to seeding
/// for the whole page
///
/// Scan button
///
/// Each scan calls the scan endpoint and the server returns a list of Media
///
/// Each Media object has a job_ID and each page has a Job_list_id
/// You can click on a poster to open a popup window
///
/// Each popup window allows you to:
/// - Create a torrent
/// - Upload a torrent
/// - Seed a torrent
/// - Set a new TMDb ID if the search fails
/// - Set a new TVDb ID if the search fails
/// - Set a new IMDB ID if TVDb returns no result
/// - Change the display name (the name shown on the torrent page on the tracker)
///
/// Tracker button
///
/// It can do three things:
/// - Call the tracker and get the last torrent uploaded
/// - Read the title in the text box and search on the tracker
/// - Filter the results by entering a keyword in the text box + Enter
///
/// Delete button
///
/// Deletes the job_list and the corresponding page
/// Deletion is server side only. It does not delete the files
/// and the backend manages the "database" directly
///
///
/// Full upload
///
/// Above the text box there is an icon button
/// It allows you to upload the page directly to the torrent tracker
///
/// Poster
///
/// At the bottom of each poster there is a status bar
/// It informs you with a short message about the operation you requested
///
///
/// [*]
/// spero di poter separare i widgets per non creare un blocco unico
///
/// La cartella widgets contiene delle sottocartelle per contesto
///
/// Ogni cartella ha un file comune di esportazione che può essere importato
/// per accedere ai widget con un solo import
class SearchPage extends StatelessWidget {
  const SearchPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(padding: EdgeInsets.all(16.0)),

        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,

              /// Search Widget
              children: [const Expanded(child: Search())],
            ),
          ),
        ),
      ],
    );
  }
}
