import 'package:flutter/material.dart';
import 'package:UI/widgets/settings/setting_container.dart';

/// Main class for the SettingPage
class SettingPage extends StatelessWidget {
  const SettingPage({super.key});

  @override
  Widget build(BuildContext context) {
    final ButtonStyle style = ElevatedButton.styleFrom(
      textStyle: const TextStyle(fontSize: 20),
    );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(padding: EdgeInsets.all(16.0)),

        Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [const SizedBox(width: 8)],
                ),
                const SizedBox(height: 8),
                const Expanded(child: Setting()),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
