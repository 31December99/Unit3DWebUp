import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

class NavigationRailMenu extends StatelessWidget {
  final int selectedIndex;
  final Function(int) onSelect;

  const NavigationRailMenu({
    super.key,
    required this.selectedIndex,
    required this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(20),
      child: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              Color(0xFF0A192B),
              Color(0xFF030E17),
              Color(0xFF230505),
            ],
          ),
        ),
        child: NavigationRail(
          backgroundColor: Colors.transparent,
          selectedIndex: selectedIndex,
          onDestinationSelected: onSelect,
          labelType: NavigationRailLabelType.selected,
          groupAlignment: -0.89,
          useIndicator: true,
          indicatorColor: Colors.white.withValues(alpha: 0.15),
          indicatorShape: const CircleBorder(),

          selectedLabelTextStyle: const TextStyle(
            color: Colors.white,
            fontFamily: "Orbitron",
          ),
          destinations: [
            NavigationRailDestination(
              icon: SvgPicture.asset(
                'lib/assets/homebutton_99695.svg',
                width: 40,
              ),
              selectedIcon: SvgPicture.asset(
                'lib/assets/homebutton_99695.svg',
                width: 40,
              ),
              label: const Text('HOME'),
            ),
            NavigationRailDestination(
              icon: SvgPicture.asset(
                'lib/assets/settingsbutton_99706.svg',
                width: 35,
              ),
              selectedIcon: SvgPicture.asset(
                'lib/assets/settingsbutton_99706.svg',
                width: 35,
              ),
              label: const Text('Settings'),
            ),
            NavigationRailDestination(
              icon: SvgPicture.asset(
                'lib/assets/commentscircularbuttonwithtwoovalspeechbubblesinside_80089.svg',
                width: 35,
              ),
              selectedIcon: SvgPicture.asset(
                'lib/assets/commentscircularbuttonwithtwoovalspeechbubblesinside_80089.svg',
                width: 35,
              ),
              label: const Text('Jobs'),
            ),
          ],
        ),
      ),
    );
  }
}
