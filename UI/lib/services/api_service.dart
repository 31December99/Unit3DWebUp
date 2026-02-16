import 'dart:convert';
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

  /// Scan remote path
  static Future<List<PosterItem>> scan() async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/scan'),
      headers: {'Content-Type': 'application/json'},
      //Todo later
      body: jsonEncode({'scan': "nothing"}),
    );

    if (response.statusCode == 200) {
      return getScanUrls(jsonDecode(response.body));
    }

    if (response.statusCode == 403) {
      final result = jsonDecode(response.body);
      return [PosterItem(snackBarError: result['message'])];
    }

    return [PosterItem(snackBarError: response.statusCode.toString())];
  }

  /// Create torrents
  static Future<String?> fetchTorrent(String jobId, String? jobListId) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/maketorrent'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'job_id': jobId, 'job_list_id': jobListId}),
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        print('Errore: ${response.statusCode}');
        return jsonDecode(response.body);
      }
    }
    return null;
  }

  /// Process all ( create torrent and upload from a media list)
  static Future<List<PosterItem>> processList(String jobListId) async {
    if (jobListId.isNotEmpty) {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/processall'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'job_list_id': jobListId}),
      );

      if (response.statusCode == 200) {
        print(jsonDecode(response.body));
        // return getPosterUrls(jsonDecode(response.body));
      } else {
        print('Errore: ${response.statusCode}');
        print(jsonDecode(response.body));

        return [];
      }
    }
    return [];
  }

  /// Upload to tracker
  static Future<List<PosterItem>> uploadTorrent(String jobId) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/upload'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'job_id': jobId}),
      );

      if (response.statusCode == 200) {
        print(jsonDecode(response.body));
        return getPosterUrls(jsonDecode(response.body));
      } else {
        print('Errore: ${response.statusCode}');
        print(jsonDecode(response.body));
        return [];
      }
    }
    return [];
  }

  /// Seed torrents
  static Future<List<PosterItem>> seedTorrent(String jobId) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/seed'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'job_id': jobId}),
      );

      if (response.statusCode == 200) {
        print(jsonDecode(response.body));
      } else {
        print('Errore: ${response.statusCode}');
        print(jsonDecode(response.body));
      }
    }
    return [];
  }

  /// Update TMDB ID
  static Future<List<PosterItem>> fetchPosterId(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/settmdbid'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'job_id': jobId,
          'field_id': fieldId,
          'new_id': newId,
        }),
      );
    }
    return [];
  }

  /// Update TVDB ID
  static Future<List<PosterItem>> fetchTvdbId(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/settvdbid'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'job_id': jobId,
          'field_id': fieldId,
          'new_id': newId,
        }),
      );
    }
    return [];
  }

  /// Update IMDB from TVDB ID
  static Future<List<PosterItem>> fetchImdbId(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/setimdbid'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'job_id': jobId,
          'field_id': fieldId,
          'new_id': newId,
        }),
      );
    }
    return [];
  }

  /// Update poster TMDB Url
  static Future<List<PosterItem>> fetchPosterUrl(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/setposterurl'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'job_id': jobId,
          'field_id': fieldId,
          'new_id': newId,
        }),
      );
    }
    return [];
  }

  /// Update poster Display Name
  static Future<List<PosterItem>> fetchPosterDname(
    String jobId,
    String fieldId,
    String newId,
  ) async {
    if (jobId != '-1') {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/setposterdname'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'job_id': jobId,
          'field_id': fieldId,
          'new_id': newId,
        }),
      );
    }
    return [];
  }

  /// Fetch Filtered Item
  static Future<List<PosterItem>> fetchFilteredItem(String title) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/filter'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'title': title}),
    );

    if (response.statusCode == 200) {
      return getPosterUrls(jsonDecode(response.body));
    } else {
      print('Errore: ${response.statusCode}');
      return [];
    }
  }

  /// Fetch Setting From Backend
  static Future<SettingItem?> fetchSettingFromBackend(String title) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/setting'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'title': title}),
    );

    if (response.statusCode == 200) {
      final decoded = jsonDecode(response.body) as Map<String, dynamic>;
      return SettingItem.fromJson(decoded);
    } else {
      print('Errore: ${response.statusCode}');
      return null;
    }
  }

  /// Edit env variables PREFS__
  static Future<PosterItem> setEnv(String key, String value) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/setenv'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'value': value, 'key': key}),
    );

    if (response.statusCode == 200) {
      final result = jsonDecode(response.body);

      return PosterItem(
        dockerStatus: result['docker'],
        snackBarStatus: result['message'],
      );
    }
    return PosterItem(snackBarError: response.statusCode.toString());
  }

  /// Fetch Filtered Item
  static Future<List<PosterItem>> clearJobListId(String? jobListId) async {
    if (jobListId != null) {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:8000/cjoblist'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'job_list_id': jobListId}),
      );

      if (response.statusCode == 200) {
        return getPosterUrls(jsonDecode(response.body));
      } else {
        print('Errore: ${response.statusCode}');
        return [];
      }
    }
    return []; // joblistId Null. ( from the remote tracker)
  }
}
