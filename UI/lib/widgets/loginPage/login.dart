import 'package:flutter/material.dart';
import 'package:UI/models/models.dart';
import 'package:UI/widgets/widgets.dart';
import 'package:UI/providers/login_provider.dart';
import 'package:provider/provider.dart';

class Login extends StatefulWidget {
  const Login({super.key});

  @override
  State<Login> createState() => _LoginState();
}

class _LoginState extends State<Login> {
  late final TextEditingController _userController;
  late final TextEditingController _passwordController;

  bool _obscurePassword = true;

  @override
  void initState() {
    super.initState();

    _userController = TextEditingController();
    _passwordController = TextEditingController();
  }

  @override
  void dispose() {
    _userController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void notifyTheUser(BuildContext context, PosterItem message) {
    showAppSnackBar(
      context,
      message,
      duration: const Duration(seconds: 2),
      backgroundColor: Colors.redAccent,
    );
  }

  void _login() {
    final username = _userController.text.trim();
    final pass = _passwordController.text;
    final app = context.read<LoginProvider>();

    app.Login(username, pass);
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 420),
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.lock_outline, size: 60),

              const SizedBox(height: 16),

              Text("Login", style: Theme.of(context).textTheme.headlineSmall),

              const SizedBox(height: 24),

              TextField(
                controller: _userController,
                keyboardType: TextInputType.name,
                decoration: const InputDecoration(
                  labelText: "User",
                  prefixIcon: Icon(Icons.umbrella),
                  border: OutlineInputBorder(),
                ),
              ),

              const SizedBox(height: 16),

              TextField(
                controller: _passwordController,
                obscureText: _obscurePassword,
                decoration: InputDecoration(
                  labelText: "Password",
                  prefixIcon: const Icon(Icons.lock_outline),
                  border: const OutlineInputBorder(),
                  suffixIcon: IconButton(
                    icon: Icon(
                      _obscurePassword
                          ? Icons.visibility
                          : Icons.visibility_off,
                    ),
                    onPressed: () {
                      setState(() {
                        _obscurePassword = !_obscurePassword;
                      });
                    },
                  ),
                ),
              ),

              const SizedBox(height: 24),

              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  const SizedBox(width: 8),
                  ElevatedButton(
                    onPressed: _login,
                    child: const Text("Login"),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
