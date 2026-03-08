import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:UI/models/models.dart';
import 'package:UI/providers/providers.dart';

///Main class for websocket
class LogProvider extends ChangeNotifier {
  final List<LogLine> _logs = [];

  List<LogLine> get logs => _logs;

  WebSocketChannel? _channel;
  final String url;
  final PosterProvider posterProvider;

  // Add PosterProvider in order to update Posters from the websocket..
  LogProvider({required this.url, required this.posterProvider}) {
    _connect();
  }

  void add(PosterItem msg, LogLevel level) {
    String? message = msg.snackBarStatus ?? msg.snackBarError ?? "Log Error";
    _logs.add(LogLine("Client $message", level));
    notifyListeners();
  }

  void rcv(String msg, LogLevel level) {
    _logs.add(LogLine("Server $msg", level));
    notifyListeners();
  }

  void rcvProgress(
    String msg,
    LogLevel level,
    String jobId,
    String process,
    double progress,
  ) {
    posterProvider.updatePosterProgress(progress, jobId, process);
    notifyListeners();
  }

  void rcvPosterMessage(String message, String jobId) {
    posterProvider.updatePosterLogMessage(message, jobId);
    _logs.add(LogLine("Server $message -> JObID $jobId ", _mapLevel('info')));
    notifyListeners();
  }

  void clear() {
    _logs.clear();
    notifyListeners();
  }

  /// Connect , receive and decode
  /// message = text message
  /// level = message type set the color
  /// job_id = Poster id update the progress ( torrent creation)
  /// progress = % work done from the torrent creation
  /// This provider ( logProvider) is "linked" to PosterProvider ->see main.py (inject it)
  /// PosterProvider manage the poster state
  void _connect() {
    _channel = WebSocketChannel.connect(Uri.parse(url));

    _channel!.stream.listen(
      (data) {
        final decoded = jsonDecode(data);
        if (decoded['type'] == 'log') {
          rcv(decoded['message'], _mapLevel(decoded['level']));
        }

        if (decoded['type'] == 'progress') {
          rcvProgress(
            decoded['message'],
            _mapLevel(decoded['level']),
            decoded['job_id'],
            decoded['process'],
            decoded['progress'],
          );
        }

        if (decoded['type'] == 'posterLogMessage') {
          rcvPosterMessage(decoded['message'], decoded['job_id']);
        }
      },
      onError: (err) => add(
        PosterItem(snackBarError: "WebSocket error: $err"),
        LogLevel.error,
      ),
      onDone: () {
        add(PosterItem(snackBarError: "WebSocket closed"), LogLevel.warn);
        Future.delayed(const Duration(seconds: 10), _connect);
      },
    );
  }

  /// not used
  void _reconnect() async {
    await Future.delayed(const Duration(seconds: 5));
  }

  void send(String msg) {
    _channel?.sink.add(msg);
  }

  @override
  void dispose() {
    _channel?.sink.close();
    super.dispose();
  }

  LogLevel _mapLevel(String level) {
    switch (level) {
      case 'progress':
        return LogLevel.progress;
      case 'info':
        return LogLevel.info;
      case 'warn':
        return LogLevel.warn;
      case 'error':
        return LogLevel.error;
      case 'debug':
        return LogLevel.debug;
      case 'success':
        return LogLevel.success;
      default:
        return LogLevel.info;
    }
  }
}
