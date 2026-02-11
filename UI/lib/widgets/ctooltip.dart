import 'package:flutter/material.dart';

/// Custom widget to show a message for a fixed amount of time
class Ctooltip extends StatelessWidget {
  final String message;
  final Widget child;
  final TextStyle? textStyle;
  final BoxDecoration? decoration;

  const Ctooltip({
    super.key,
    required this.message,
    required this.child,
    this.textStyle,
    this.decoration,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: message,
      waitDuration: const Duration(milliseconds: 600),
      showDuration: const Duration(seconds: 3),
      textStyle:
          textStyle ??
          const TextStyle(
            color: Color(0xFF251207),
            fontFamily: 'WhiteRabbit',
            fontSize: 12,
            letterSpacing: 0.8,
            fontWeight: FontWeight.normal,
          ),
      decoration:
          decoration ??
          BoxDecoration(
            color: const Color(0xFFCAA8A8).withAlpha(200),
            borderRadius: BorderRadius.circular(4),
          ),
      child: child,
    );
  }
}
