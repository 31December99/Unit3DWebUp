import 'package:flutter/material.dart';

/// Class represent a dropDownButton in SettingPage
class SettingDropdown extends StatelessWidget {
  final String label;
  final List<String> items;
  final String selected;
  final ValueChanged<String?> onChanged;

  const SettingDropdown({
    super.key,
    required this.label,
    required this.items,
    required this.selected,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        // Dropdown
        Expanded(
          flex: 2,
          child: DropdownButton<String>(
            value: selected,
            isExpanded: true,
            icon: const Icon(Icons.arrow_drop_down),
            underline: Container(height: 2, color: Colors.deepPurpleAccent),
            onChanged: onChanged,
            items: items.map((value) {
              return DropdownMenuItem(value: value, child: Text(value));
            }).toList(),
          ),
        ),

        const SizedBox(width: 12),
        Expanded(
          flex: 3,
          child: Text(
            label,
            style: TextStyle(fontSize: 14, color: Colors.grey[700]),
          ),
        ),
      ],
    );
  }
}
