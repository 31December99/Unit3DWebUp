import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';

/// Shows a popup message at the bottom of the screen
void showAppSnackBar(
  BuildContext context,
  PosterItem notify,
  {Duration duration = const Duration(milliseconds: 700),
  Color backgroundColor = const Color(0xFFBEBF91),
  })

{

  Color color = notify.snackBarStatus != null ? Colors.white70 : Colors.redAccent;
  String? message =  notify.snackBarStatus ?? notify.snackBarError ?? "SnackBar Error";

  backgroundColor = notify.snackBarStatus != null ? Color(0xFF757A6F): Color(
      0xFF2E2C2C);

  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      duration: duration,
      backgroundColor: backgroundColor,
      content: Text(
        message,
        style: TextStyle(
          fontFamily: 'WhiteRabbit',
          fontSize: 12,
          color: color,
          letterSpacing: 0.8,
        ),
      ),
    ),
  );
}
