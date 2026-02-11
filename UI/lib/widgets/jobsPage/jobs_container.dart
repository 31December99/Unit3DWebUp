import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/providers/providers.dart';
import 'package:UI/widgets/jobsPage/jobs.dart';

/// Console window in the Jobs page
class JobsContainer extends StatefulWidget {
  const JobsContainer({super.key});

  @override
  State<JobsContainer> createState() => _JobsState();
}

class _JobsState extends State<JobsContainer> {
  late final TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final logs = context.watch<LogProvider>().logs;

    return SizedBox.expand(child: ConsoleLogView(logs: logs));
  }
}
