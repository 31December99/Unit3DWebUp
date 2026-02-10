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

  /// SearchPage -> Scanfolder and manage Poster, Last Torrent from the tracker
  /// SettingPage -> Call the /setting endpoint and get the last setting
  /// JobPage -> Console log : websocket msg , short http msg, Scan ecc
  final List<Widget> pages = [SearchPage(), SettingPage(), JobsPage()];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Row(
          children: [
            NavigationRailMenu(
              selectedIndex: _selectedIndex,
              onSelect: (index) {
                // chiudo il focus !
                FocusScope.of(context).unfocus();
                setState(() {
                  _selectedIndex = index;
                });
              },
            ),

            VerticalDivider(width: 1, thickness: 1),
            Expanded(child: pages[_selectedIndex]),
          ],
        ),
      ),
    );
  }
}
