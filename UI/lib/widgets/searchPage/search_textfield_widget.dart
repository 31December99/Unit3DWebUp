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
    return SizedBox(
      height: 50,
      width: 400,
      child: TextField(
        controller: controller,
        style: const TextStyle(
            fontSize: 12,
            color: Colors.white,
            fontFamily: 'Orbitron',
        ),
        decoration: InputDecoration(
          isDense: true,
          contentPadding: const EdgeInsets.symmetric(
            vertical: 8,
            horizontal: 12,
          ),
          hintText: hint,
          hintStyle: const TextStyle(
            color: Colors.white,
            fontSize: 12,
            // fontFamily: 'WhiteRabbit',
            fontFamily: 'Orbitron',
            letterSpacing: 0.8,
          ),
          focusedBorder: OutlineInputBorder(
            // borderSide: BorderSide(color: Colors.transparent),
            borderRadius: BorderRadius.circular(8),
            borderSide: BorderSide(
              color: Colors.white.withValues(alpha: 0.25),
              width: 1,
          ),
          ),
          hoverColor: Colors.transparent,
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: BorderSide(color: Colors.transparent),
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(8),
            borderSide: BorderSide.none,
          ),

          suffixIconConstraints: const BoxConstraints(
            minHeight: 32,
            minWidth: 90,
          ),
          suffixIcon: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Ctooltip(
                message: "Ricarica il tuo percorso",
                child: IconButton(
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(
                    minWidth: 28,
                    minHeight: 28,
                  ),
                  icon: SvgPicture.asset(
                    'lib/assets/refresh-svgrepo-com.svg',
                    width: 21,
                  ),
                  onPressed: onClickScan,
                ),
              ),
              Ctooltip(
                message: "Cerca nel tracker",
                child: IconButton(
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(
                    minWidth: 28,
                    minHeight: 28,
                  ),
                  icon: SvgPicture.asset(
                    'lib/assets/network-share-svgrepo-com.svg',
                    width: 21,
                  ),
                  onPressed: () {
                    if (onClickTracker != null && controller != null) {
                      onClickTracker!(controller!.text);
                    }
                  },
                ),
              ),

              Ctooltip(
                message: "Cancella la cache !",
                child: IconButton(
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(
                    minWidth: 28,
                    minHeight: 28,
                  ),
                  icon: SvgPicture.asset(
                    'lib/assets/clear-svgrepo-com.svg',
                    width: 19,
                  ),
                  onPressed: onClickClear,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
