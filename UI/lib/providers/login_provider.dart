import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/services/services.dart';

class LoginProvider extends ChangeNotifier {
  LoginProvider();

  /// PosterItem list received from api endpoints
  List<PosterItem> posterItems = [];

  /// PosterItem received from api endpoints
  PosterItem? response;

  /// Login Bool
  bool logged = false;

  /// PosterItem list received from api endpoints
  PosterItem posterItem = PosterItem();

  /// Use different name for PosterItem list for poster Popup
  List<PosterItem> posterPopUpItems = [];

  /// PosterPopUpItem list received from api endpoints
  PosterItem posterPopUpItem = PosterItem();

  /// URL corrente del poster selezionato
  String? selectedPosterUrl;

  /// Assume il valore in string della selezione source in locale o remoto
  // String selectedSource = 'Local';

  /// Switch icon from normal to loading
  bool isLoading = false;

  /// Tramite widget switch seleziona un source in locale o in remoto
  // bool isLocal = false;

  /// ENDPOINTS
  ///
  /// Request to scan the user path
  Future<bool> Login(String username, String pass) async {
    return await ApiService.login(username, pass);
  }
}
