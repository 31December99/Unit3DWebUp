import 'package:flutter/material.dart';

/// Set console color based on backend log field
enum LogLevel { info, progress, warn, error, debug, success }

class LogLine {
  final String message;
  final LogLevel level;
  final DateTime ts;

  LogLine(this.message, this.level) : ts = DateTime.now();
}

Color levelColor(LogLevel level) {
  switch (level) {
    case LogLevel.info:
      return Colors.lightBlueAccent;
    case LogLevel.progress:
      return Colors.brown;
    case LogLevel.warn:
      return Colors.orangeAccent;
    case LogLevel.error:
      return Colors.redAccent;
    case LogLevel.debug:
      return Colors.grey;
    case LogLevel.success:
      return Colors.greenAccent;
  }
}
