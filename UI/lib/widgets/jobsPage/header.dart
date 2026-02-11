import 'package:flutter/material.dart';

/// Separate class to build the header title in the console window
class ConsoleHeader extends StatelessWidget {
  final String title;
  final Widget? trailing;

  const ConsoleHeader({super.key, required this.title, this.trailing});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 36,
      padding: const EdgeInsets.symmetric(horizontal: 10),
      decoration: const BoxDecoration(
        color: Color(0xFF0A0A0A),
        borderRadius: BorderRadius.vertical(top: Radius.circular(8)),
      ),
      child: Row(
        children: [
          Text(
            title,
            style: const TextStyle(
              fontFamily: 'WhiteRabbit',
              fontSize: 12,
              color: Color(0xFF00FF88),
              letterSpacing: 1,
            ),
          ),
          const Spacer(),
          ?trailing,
        ],
      ),
    );
  }
}
