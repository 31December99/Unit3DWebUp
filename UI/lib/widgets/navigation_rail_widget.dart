import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';

/// Separate widget uses NavigationRail to build a lateral menù
/// The user can click on a specific icon to navigate to the selected page
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
    return NavigationRail(
      selectedIndex: selectedIndex,
      onDestinationSelected: onSelect,
      labelType: NavigationRailLabelType.selected,
      destinations: [

        NavigationRailDestination(
          icon: SvgPicture.asset('lib/assets/home-svgrepo-com.svg', width: 20),
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
    );
  }
}
