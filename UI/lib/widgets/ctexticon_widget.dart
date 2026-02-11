import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

/// Custom widget to represent a clickable icon next to text
class CtextIcon extends StatelessWidget {
  final String label;
  final String svgAsset;
  final double iconWidth;
  final VoidCallback? onIconPressed;
  final double fontSize;
  final String? fontFamily;
  final FontWeight? fontWeight;

  const CtextIcon({
    super.key,
    required this.label,
    required this.svgAsset,
    this.iconWidth = 16,
    this.onIconPressed,
    this.fontSize = 12,
    this.fontFamily,
    this.fontWeight = FontWeight.normal,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        IconButton(
          padding: EdgeInsets.zero,
          constraints: const BoxConstraints(),
          onPressed: onIconPressed ?? () {},
          icon: SvgPicture.asset(svgAsset, width: iconWidth),
        ),
        const SizedBox(width: 4),
        Expanded(
          child: Text(
            label,
            style: TextStyle(
              fontSize: fontSize,
              fontFamily: fontFamily,
              fontWeight: fontWeight,
            ),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ],
    );
  }
}
