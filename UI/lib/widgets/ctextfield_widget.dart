import 'package:flutter/material.dart';

/// Custom widget to draw a text field associated with an event (on Submitted)
class CtextField extends StatelessWidget {
  final String label;
  final TextEditingController controller;
  final void Function(String)? onSubmitted;
  final double fontSize;
  final String? fontFamily;
  final double letterSpacing;

  const CtextField({
    super.key,
    required this.label,
    required this.controller,
    this.onSubmitted,
    this.fontSize = 12,
    this.fontFamily = 'WhiteRabbit',
    this.letterSpacing = 1,
  });

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      style: TextStyle(
        color: Colors.white70,
        fontSize: fontSize,
        fontFamily: fontFamily,
        letterSpacing: letterSpacing,
      ),
      decoration: InputDecoration(
        labelText: label,
        isDense: true,
        contentPadding: const EdgeInsets.symmetric(
          vertical: 15,
          horizontal: 12,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Colors.grey, width: 1),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: Colors.blue, width: 2),
        ),
      ),
      onSubmitted: onSubmitted,
    );
  }
}
