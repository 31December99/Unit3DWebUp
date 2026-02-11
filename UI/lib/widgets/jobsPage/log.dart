import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';

/// Separate widget for build log in the console window
class LogArea extends StatelessWidget {
  final List<LogLine> logs;
  final ScrollController scrollController;
  final EdgeInsets padding;
  final double fontSize;

  const LogArea({
    super.key,
    required this.logs,
    required this.scrollController,
    required this.padding,
    required this.fontSize,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: padding,
        child: ListView.builder(
          controller: scrollController,
          reverse: true,
          padding: const EdgeInsets.only(bottom: 16),
          itemCount: logs.length,
          itemBuilder: (context, i) {
            final log = logs[logs.length - 1 - i];

            return Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: RichText(
                text: TextSpan(
                  style: TextStyle(
                    fontFamily: 'WhiteRabbit',
                    fontSize: fontSize,
                    letterSpacing: 0.8,
                    color: const Color(0xFFE5FFE5),
                  ),
                  children: [
                    TextSpan(
                      text: '[${formatTs(log.ts)}] ',
                      style: const TextStyle(color: Colors.grey),
                    ),
                    TextSpan(
                      text: '[${log.level.name.toUpperCase().padRight(5)}] ',
                      style: TextStyle(color: levelColor(log.level)),
                    ),
                    TextSpan(text: log.message),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

/// Timestamp hh:mm:ss
String formatTs(DateTime ts) {
  return '${ts.hour.toString().padLeft(2, '0')}:'
      '${ts.minute.toString().padLeft(2, '0')}:'
      '${ts.second.toString().padLeft(2, '0')}';
}
