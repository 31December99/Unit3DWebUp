import 'package:flutter/material.dart';
import 'package:UI/widgets/widgets.dart';
import 'package:UI/pages/pages.dart';
import 'package:UI/providers/login_provider.dart';
import 'package:provider/provider.dart';

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

  @override
  Widget build(BuildContext context) {
    final app = context.watch<LoginProvider>();

    final List<Widget> pages = [
      const LoginPage(),
      const SearchPage(),
      const SettingPage(),
      const JobsPage(),
    ];

    if (!app.logged) {
      _selectedIndex = 0;
    } else if (_selectedIndex == 0) {
      _selectedIndex = 1;
    }

    return MaterialApp(
      home: Scaffold(
        body: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Color(0xFF0B0F1A), Color(0xFF2C2D63), Color(0xFFAE3812)],
            ),
          ),
          child: Row(
            children: [
              NavigationRailMenu(
                selectedIndex: _selectedIndex,
                onSelect: (index) {
                  FocusScope.of(context).unfocus();
                  setState(() {
                    _selectedIndex = index;
                  });
                },
              ),
              Expanded(
                child: IndexedStack(index: _selectedIndex, children: pages),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
