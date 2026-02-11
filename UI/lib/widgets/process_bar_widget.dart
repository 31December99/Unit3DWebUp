import 'package:flutter/material.dart';

/// Class to build a line at the bottom of an image (poster)
/// It shows multiple messages or process statuses
class ProcessBar extends StatelessWidget {
  final Color source;
  final String process;
  final Alignment alignment;

  const ProcessBar({
    super.key,
    required this.source,
    required this.process,
    required this.alignment,
  });

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: alignment,
      child: Container(
        height: 14,
        width: double.infinity,
        color: source,
        alignment: Alignment.center,
        child: Text(
          process,
          style: const TextStyle(
            color: Colors.white,
            fontSize: 9,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
