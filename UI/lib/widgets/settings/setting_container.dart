import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/settings/setting_tab_views.dart';

/// Main class for the SettingPage
class Setting extends StatefulWidget {
  const Setting({super.key});

  @override
  State<Setting> createState() => _SettingState();
}

class _SettingState extends State<Setting> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();

    /// Load the setting page as soon as the widget is built
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final settingProvider = context.read<SettingProvider>();
      settingProvider.readSetting();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(15),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: DefaultTabController(
              length: 3,
              child: Column(
                children: [
                  const TabBar(
                    tabs: [
                      Tab(icon: Icon(Icons.folder), text: "Percorso"),
                      Tab(icon: Icon(Icons.tune), text: "Preferenze"),
                      Tab(icon: Icon(Icons.settings), text: "Opzioni"),
                    ],
                  ),
                  Expanded(child: SettingTabViews()),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
