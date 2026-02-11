import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/widgets/jobsPage/jobs.dart';
import 'package:UI/widgets/jobsPage/log.dart';

/// Custom widget to display the console area for logs
class ConsoleLogView extends StatefulWidget {
  final List<LogLine> logs;

  const ConsoleLogView({super.key, required this.logs});

  @override
  State<ConsoleLogView> createState() => _ConsoleLogViewState();
}

class _ConsoleLogViewState extends State<ConsoleLogView> {
  final ScrollController _scroll = ScrollController();

  @override
  void didUpdateWidget(covariant ConsoleLogView oldWidget) {
    super.didUpdateWidget(oldWidget);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scroll.hasClients) {
        _scroll.jumpTo(_scroll.position.minScrollExtent);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    final bool isMobile = size.width < 600;
    final bool isTablet = size.width >= 600 && size.width < 1024;

    final double fontSize = isMobile
        ? 12
        : isTablet
        ? 13
        : 14;

    final EdgeInsets padding = EdgeInsets.symmetric(
      horizontal: isMobile ? 10 : 14,
      vertical: isMobile ? 8 : 12,
    );

    return SizedBox(
      height: size.height * 0.5,
      child: SafeArea(
        top: false,
        left: false,
        right: false,
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: 8),
          decoration: BoxDecoration(
            color: const Color(0xFF050505),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(color: const Color(0xFF2A2A2A)),
          ),
          child: Column(
            children: [
              // hEADER windows console
              ConsoleHeader(title: "ITT TRACKER LOG"),
              const Divider(height: 1, color: Color(0xFF1A1A1A)),
              // Message area
              LogArea(
                logs: widget.logs,
                scrollController: _scroll,
                padding: padding,
                fontSize: fontSize,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
