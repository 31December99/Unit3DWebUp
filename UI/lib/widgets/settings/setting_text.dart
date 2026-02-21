import 'package:UI/models/models.dart';
import 'package:UI/providers/providers.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/widgets/widgets.dart';

/// Custom widget for a TextField in the SettingsPage
class SettingText extends StatefulWidget {
  final String label;
  final String value;
  final String? hint;

  const SettingText({
    super.key,
    required this.label,
    required this.value,
    this.hint,
  });

  @override
  State<SettingText> createState() => _SettingTextState();
}

class _SettingTextState extends State<SettingText> {
  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.value);
  }

  @override
  void didUpdateWidget(covariant SettingText oldWidget) {
    super.didUpdateWidget(oldWidget);

    if (widget.value != oldWidget.value) {
      _controller.text = widget.value;
      _controller.selection = TextSelection.fromPosition(
        TextPosition(offset: _controller.text.length),
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  /// Notify the user: Docker needs to be restarted
  void dockerRestart(BuildContext context) {
    showAppSnackBar(
      context,
      "Please restart the container or run docker-compose restart",
      duration: const Duration(seconds: 2),
      backgroundColor: Colors.redAccent,
    );
  }

  /// Generic success snackbar
  void snackBarStatus(BuildContext context, String? message) {
    showAppSnackBar(
      context,
      message ?? '',
      duration: const Duration(seconds: 2),
      backgroundColor: Colors.greenAccent,
    );
  }

  Future<void> checkDockerStatus(
    BuildContext context,
    PosterItem response,
  ) async {
    if (response.dockerStatus == 'true') {
      snackBarStatus(context, response.snackBarStatus);
      dockerRestart(context);
    } else {
      snackBarStatus(context, response.snackBarStatus);
    }
  }

  @override
  Widget build(BuildContext context) {
    final provider = context.read<SettingProvider>();

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          Expanded(
            flex: 2,
            child: Text(
              style: const TextStyle(color: Colors.white),
              widget.label,
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            flex: 3,
            child: TextField(
              style: const TextStyle(color: Colors.white),
              controller: _controller,
              decoration: InputDecoration(
                hintText: widget.hint,
                border: const OutlineInputBorder(),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 8,
                  vertical: 4,
                ),
              ),
              onSubmitted: (value) async {
                final response = await provider.setEnv(widget.label, value);
                if (!context.mounted) return;
                if (widget.label.contains('PATH')) {
                  await checkDockerStatus(context, response);
                } else {
                  snackBarStatus(context, response.snackBarStatus);
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}
