import 'package:flutter/material.dart';

/// Shows a popup message at the bottom of the screen
void showAppSnackBar(
  BuildContext context,
  String message,
  {Duration duration = const Duration(milliseconds: 700),
  Color backgroundColor = const Color(0xFFBEBF91),
  })

{
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      duration: duration,
      backgroundColor: backgroundColor,
      content: Text(
        message,
        style: const TextStyle(
          fontFamily: 'WhiteRabbit',
          fontSize: 12,
          color: Color(0xFF1E1E1D),
          letterSpacing: 0.8,
        ),
      ),
    ),
  );
}
