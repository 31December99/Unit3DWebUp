import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:UI/widgets/widgets.dart';

/// Search bar and icon buttons in SearchPage
///
class SearchTextField extends StatelessWidget {
  final ValueChanged<String>? onChanged;
  final void Function(String)? onSubmitted;
  final ValueChanged<String>? onClickTracker;
  final VoidCallback? onClickScan;
  final VoidCallback? onClickClear;

  final String hint;
  final TextEditingController? controller;

  const SearchTextField({
    super.key,
    this.onChanged,
    this.onSubmitted,
    this.onClickScan,
    this.onClickTracker,
    this.onClickClear,
    this.hint = "Cerca...",
    this.controller,
  });

  @override
  Widget build(BuildContext context) {
    /// Search bar
    return TextField(
      controller: controller,
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: TextStyle(
          color: const Color(0xFF231616).withAlpha(150),
          fontSize: 12,
          fontFamily: 'WhiteRabbit',
          letterSpacing: 0.8,
        ),
        border: const OutlineInputBorder(),
        suffixIcon: Wrap(
          spacing: 4,
          children: [
            /// Icon button Scan
            Ctooltip(
              message: "Ricarica il tuo percorso",
              child: IconButton(
                onPressed: onClickScan,
                icon: SvgPicture.asset(
                  'lib/assets/refresh-svgrepo-com.svg',
                  width: 25,
                ),
              ),
            ),

            /// Icon button Tracker Search
            Ctooltip(
              message: "Cerca nel tracker",
              child: IconButton(
                onPressed: () {
                  if (onClickTracker != null && controller != null) {
                    onClickTracker!(controller!.text);
                  }
                },
                icon: SvgPicture.asset(
                  'lib/assets/network-svgrepo-com.svg',
                  width: 25,
                ),
              ),
            ),

            /// Icon button Delete current page
            Ctooltip(
              message: "Cancella la cache",
              child: IconButton(
                onPressed: onClickClear,
                icon: SvgPicture.asset(
                  'lib/assets/clear-svgrepo-com.svg',
                  width: 20,
                ),
              ),
            ),
          ],
        ),
        suffixIconConstraints: const BoxConstraints(
          minWidth: 96,
          minHeight: 25,
        ),
      ),
      onChanged: onChanged,
      onSubmitted: onSubmitted,
    );
  }
}
