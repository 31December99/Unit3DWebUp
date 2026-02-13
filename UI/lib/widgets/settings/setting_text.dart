import 'package:flutter/material.dart';

/// Custom widget for a TextField in the SettingsPage
class SettingText extends StatefulWidget {
  final String label;
  final String value;
  final ValueChanged<String> onSubmitted;
  final String? hint;

  const SettingText({
    super.key,
    required this.label,
    required this.value,
    required this.onSubmitted,
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
    // Check the previous state !
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

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: Row(
        children: [
          Expanded(flex: 2, child: Text(widget.label)),
          const SizedBox(width: 12),
          Expanded(
            flex: 3,
            child: TextField(
              controller: _controller,
              decoration: InputDecoration(
                hintText: widget.hint,
                border: OutlineInputBorder(),
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 8,
                  vertical: 4,
                ),
              ),
              onSubmitted: widget.onSubmitted,
            ),
          ),
        ],
      ),
    );
  }
}
