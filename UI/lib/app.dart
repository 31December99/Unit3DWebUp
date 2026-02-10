import 'package:flutter/material.dart';
import 'package:UI/widgets/widgets.dart';
import 'package:UI/pages/pages.dart';

/// The Main Layout
/// Cambio pagina index di NavigationRailMenu
///
class MainLayout extends StatefulWidget {
  const MainLayout({super.key});

  @override
  MainLayoutState createState() => MainLayoutState();
}

/// Mainlayout State
///
/// NavigationRailMenu set the index in pages list
///
/// [pages]: SearchPAge() , SettingPage(), JobsPage()
///
/// [_selectedIndex]: The current page index

class MainLayoutState extends State<MainLayout> {
  int _selectedIndex = 0;

  /// SearchPage -> scan the user path and manage Poster
  /// SettingPage -> get the last setting
  /// JobPage -> write logs to the console window

  final List<Widget> pages = [
    const SearchPage(),
    const SettingPage(),
    const JobsPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Row(
          children: [
            /// a menu that changes its selected index when the user clicks
            /// custom widget based on NavigationRail widget
            NavigationRailMenu(
              selectedIndex: _selectedIndex,
              onSelect: (index) {
                /// remove the focus from Textbox when user change the page
                /// otherwise it could cause a crash
                FocusScope.of(context).unfocus();
                setState(() {
                  _selectedIndex = index;
                });
              },
            ),
            const VerticalDivider(width: 1, thickness: 1),
            Expanded(
              /// Use IndexedStack to save the page state
              /// otherwise the page would be killed
              /// ( removed from the widget tree)
              /// with 'Expanded(child: pages[_selectedIndex])'
              /// https://api.flutter.dev/flutter/widgets/IndexedStack-class.html
              child: IndexedStack(index: _selectedIndex, children: pages),
            ),
          ],
        ),
      ),
    );
  }
}