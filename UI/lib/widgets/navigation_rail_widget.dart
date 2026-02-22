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
              Color(0xFF3A2C63),
            ],
          ),
        ),
        child: NavigationRail(
          backgroundColor: Colors.transparent,
          selectedIndex: selectedIndex,
          onDestinationSelected: onSelect,
          labelType: NavigationRailLabelType.selected,
          groupAlignment: -0.89,
          destinations: [
            NavigationRailDestination(
              icon: SvgPicture.asset(
                'lib/assets/home-svgrepo-com.svg',
                width: 20,
              ),
              selectedIcon: SvgPicture.asset(
                'lib/assets/home-svgrepo-com.svg',
                width: 20,
              ),
              label: const Text('HOME'),
            ),
            NavigationRailDestination(
              icon: SvgPicture.asset(
                'lib/assets/adjust-svgrepo-com.svg',
                width: 35,
              ),
              selectedIcon: SvgPicture.asset(
                'lib/assets/adjust-svgrepo-com.svg',
                width: 35,
              ),
              label: const Text('Settings'),
            ),
            NavigationRailDestination(
              icon: SvgPicture.asset(
                'lib/assets/ladybug-bug-svgrepo-com.svg',
                width: 25,
              ),
              selectedIcon: SvgPicture.asset(
                'lib/assets/ladybug-bug-svgrepo-com.svg',
                width: 25,
              ),
              label: const Text('Jobs'),
            ),
          ],
        ),
      ),
    );
  }
}
