import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:UI/models/models.dart';

/// Class to communicate with the backend API
///
/// General:
/// - [getPosterUrls]: build a PosterItem object
///
/// Tracker:
/// - [fetchFilteredItem]: Filter title by word
///
/// Local content:
/// - [fetchSettingFromBackend]: Get the settings
///
class ApiService {
  /// Get Scan Urls
  static List<PosterItem> getScanUrls(Map<String, dynamic>? result) {
    if (result == null) return [];

    final String source = result['source'] as String;
    final rawResults = result['results'];
    if (rawResults == null) return [];
    final List<Map<String, dynamic>> results = rawResults is List
        ? rawResults.cast<Map<String, dynamic>>()
        : [rawResults as Map<String, dynamic>];

    /// Create a list of PosterItem items
    return results.map((map) {
      return PosterItem(
        posterUrl:
            "https://image.tmdb.org/t/p/original/${map['backdrop_path']}",
        displayName: map['display_name'] as String?,
        source: source,
        tmdbId: map['tmdb_id'].toString(),
        tvdbId: map['tvdb_id'].toString(),
        imdbId: map['imdb_id_from_tvdb'].toString(),
        jobId: map['job_id'].toString(),
        jobListId: map['job_id_list'],
        status: map['status'].toString(),
        screenshots: map['screen_shots'],
      );
    }).toList();
  }

  static List<PosterItem> getPosterUrls(Map<String, dynamic>? result) {
    if (result == null) return [];

    final String source = result['source'] as String;
    final String jobId = result['job_id'] as String? ?? 'n/a';
    final List<dynamic>? results = result['results'] as List<dynamic>?;

    if (results == null || results.isEmpty) return [];

    /// Create a list of PosterItem items
    return results.map((item) {
      final map = item as Map<String, dynamic>;
      return PosterItem(
        posterUrl: map['meta']['poster'],
        displayName: map['name'] as String?,
        source: source,
        tmdbId: map['tmdb_id'].toString(),
        jobId: jobId,
      );
    }).toList();
  }

  static Future<http.Response?> _post(
    String endpoint,
    Map<String, dynamic> body,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/$endpoint'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      );

      return response;
    } on http.ClientException catch (e) {
      print("Backend offline: $e");
      return null;
    } on SocketException catch (e) {
      print("Socket error: $e");
      return null;
    } catch (e) {
      print("Unknown API error: $e");
      return null;
    }
  }

  static Future<List<PosterItem>> scan() async {
    final response = await _post("scan", {'path': "nothing"});
    if (response == null) {
      return [PosterItem(snackBarError: "Backend offline")];
    }

    if (response.statusCode == 200) {
      return getScanUrls(jsonDecode(response.body));
    }

    if (response.statusCode == 403) {
      final result = jsonDecode(response.body);
      return [PosterItem(snackBarStatus: result['message'])];
    }

    return [PosterItem(snackBarStatus: response.statusCode.toString())];
  }

  /// Create torrents
  static Future<PosterItem> fetchTorrent(
    String jobId,
    String? jobListId,
  ) async {
    final response = await _post("maketorrent", {
      'job_id': jobId,
      'job_list_id': jobListId,
    });

    if (response == null) {
      return PosterItem(snackBarError: "Backend offline");
    } else {
      return PosterItem(
        snackBarStatus: 'Make Torrent job $jobId Please wait...',
      );
    }
  }

  /// Process all ( create torrent and upload from a media list)
  static Future<PosterItem> processList(String jobListId) async {
    final response = await _post("processall", {'job_list_id': jobListId});
    if (response == null) {
      return PosterItem(snackBarError: "Backend offline");
    } else {
      return PosterItem(
        snackBarStatus: "Upload ALL job $jobListId Please wait...",
      );
    }
  }

  /// Upload to tracker
  static Future<PosterItem> uploadTorrent(String jobId) async {
    final response = await _post("upload", {'job_id': jobId});
    if (response == null) {
      return PosterItem(snackBarError: "Backend offline");
    } else {
      return PosterItem(
        snackBarStatus: 'Upload Torrent job $jobId Please wait...',
      );
    }
  }

  /// Seed torrents
  static Future<PosterItem> seedTorrent(String jobId) async {
    final response = await _post("seed", {'job_id': jobId});

    if (response != null) {
      if (response.statusCode == 503) {
        return PosterItem(snackBarError: "Torrent client offline");
      }
      if (response.statusCode == 409) {
        return PosterItem(snackBarError: "File torrent is already seeding");
      }
      if (response.statusCode == 404) {
        return PosterItem(snackBarError: "Torrent list is empty");
      } else {
        return PosterItem(
          snackBarStatus: 'Seeding Torrent job $jobId Please wait...',
        );
      }
    } else {
      return PosterItem(snackBarError: "Backend offline");
    }
  }

  static Future<PosterItem> fetchPosterId(
    String jobId,
    String fieldId,
    String newId,
    PosterItem posterItem,
  ) async {
    final response = await _post("settmdbid", {
      'job_id': jobId,
      'field_id': fieldId,
      'new_id': newId,
    });

    if (response == null) {
      posterItem.snackBarStatus = "Backend offline";
      return posterItem;
    }

    if (response.statusCode == 200) {
      posterItem.snackBarStatus = "Update Poster Id job $jobId Please wait...";
    } else {
      posterItem.snackBarStatus = "Request failed (${response.statusCode})";
    }
    return posterItem;
  }

  /// Update TVDB ID
  static Future<PosterItem> fetchTvdbId(
    String jobId,
    String fieldId,
    String newId,
    PosterItem posterItem,
  ) async {
    final response = await _post("settvdbid", {
      'job_id': jobId,
      'field_id': fieldId,
      'new_id': newId,
    });

    if (response == null) {
      posterItem.snackBarStatus = "Backend offline";
      return posterItem;
    }

    if (response.statusCode == 200) {
      posterItem.snackBarStatus = "Update TVDB job $jobId Please wait...";
      return posterItem;
    } else {
      posterItem.snackBarStatus = "Request failed (${response.statusCode})";
    }

    return posterItem;
  }

  /// Update IMDB from TVDB ID
  static Future<PosterItem> fetchImdbId(
    String jobId,
    String fieldId,
    String newId,
    PosterItem posterItem,
  ) async {
    final response = await _post("setimdbid", {
      'job_id': jobId,
      'field_id': fieldId,
      'new_id': newId,
    });

    if (response == null) {
      posterItem.snackBarStatus = "Backend offline";
      return posterItem;
    }

    if (response.statusCode == 200) {
      posterItem.snackBarStatus = "Update IMDB job $jobId Please wait...";
      return posterItem;
    } else {
      posterItem.snackBarStatus = "Request failed (${response.statusCode})";
    }

    return posterItem;
  }

  /// Update poster TMDB Url
  static Future<PosterItem> fetchPosterUrl(
    String jobId,
    String fieldId,
    String newId,
    PosterItem posterItem,
  ) async {
    final response = await _post("setposterurl", {
      'job_id': jobId,
      'field_id': fieldId,
      'new_id': newId,
    });

    if (response == null) {
      posterItem.snackBarStatus = "Backend offline";
      return posterItem;
    }

    if (response.statusCode == 200) {
      posterItem.snackBarStatus = "Update TMDB Url job $jobId Please wait...";
      return posterItem;
    } else {
      posterItem.snackBarStatus = "Request failed (${response.statusCode})";
    }

    return posterItem;
  }

  /// Update poster Display Name
  static Future<PosterItem> fetchPosterDname(
    String jobId,
    String fieldId,
    String newId,
    PosterItem posterItem,
  ) async {
    final response = await _post("setposterdname", {
      'job_id': jobId,
      'field_id': fieldId,
      'new_id': newId,
    });

    if (response == null) {
      posterItem.snackBarStatus = "Backend offline";
      return posterItem;
    }

    if (response.statusCode == 200) {
      posterItem.snackBarStatus =
          "Update Display Name job $jobId Please wait...";
      return posterItem;
    } else {
      posterItem.snackBarStatus = "Request failed (${response.statusCode})";
    }

    return posterItem;
  }

  /// Fetch Filtered Item
  static Future<List<PosterItem>> fetchFilteredItem(String title) async {
    final response = await _post("filter", {'title': title});

    if (response == null) {
      return [PosterItem(snackBarError: "Backend offline")];
    }

    if (response.statusCode == 200) {
      return getPosterUrls(jsonDecode(response.body));
    } else {
      return [
        PosterItem(snackBarError: "Request failed ${response.statusCode}"),
      ];
    }
  }

  /// Fetch Filtered Item
  static Future<PosterItem> clearJobListId(String? jobListId) async {
    final response = await _post("cjoblist", {'job_list_id': jobListId});

    if (response == null) {
      return PosterItem(snackBarError: "Backend offline");
    } else {
      return PosterItem(snackBarError: "Deleted joblist $jobListId");
    }
  }

  /// Fetch Setting From Backend
  static Future<SettingItem?> fetchSettingFromBackend(String title) async {
    try {
      final response = await _post("setting", {'title': title});

      if (response == null) {
        return null;
      }

      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body) as Map<String, dynamic>;
        return SettingItem.fromJson(decoded);
      } else {
        return null;
      }
    } on http.ClientException catch (e) {
      print("Backend offline");
      return null;
    }
  }

  /// Edit env variables PREFS__
  static Future<PosterItem> setEnv(String key, String value) async {
    final response = await _post("setenv", {'value': value, 'key': key});

    if (response == null) {
      return PosterItem(snackBarError: "Backend offline");
    }

    if (response.statusCode == 200) {
      final result = jsonDecode(response.body);
      return PosterItem(
        dockerStatus: result['docker'],
        snackBarStatus: result['message'],
      );
    }
    return PosterItem(snackBarStatus: response.statusCode.toString());
  }
}
