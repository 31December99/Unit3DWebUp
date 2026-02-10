import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:UI/providers/providers.dart';
import 'app.dart';

/// Entry point

/// List of providers
/// - [PosterProvider]:   manage poster (le locandine)
/// - [LogProvider]:      manage websocket communication
/// - [SettingProvider]:  manage configuration from the backend
void main() {
  runApp(
    MultiProvider(
      providers: [
        /// Provider for poster and search (PosterProvider)
        ChangeNotifierProvider(create: (_) => PosterProvider()),

        /// manage Websocket and talk to PosterProvider...
        /// LogProvider inside ChangeNotifierProvider
        ChangeNotifierProvider(
          create: (context) => LogProvider(
            //TODO for the moment is hardcoded
            url: 'ws://localhost:8000/ws',
            posterProvider: context.read<PosterProvider>(),
          ),
        ),

        /// Page settings ( the configuration file from the backend)
        ChangeNotifierProvider(create: (_) => SettingProvider()),
      ],

      /// Go
      child: MainLayout(),
    ),
  );
}
